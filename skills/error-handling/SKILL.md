---
name: error-handling
description: Implements error handling patterns, structured logging, retry strategies, circuit breakers, and graceful degradation. Use when designing error handling, setting up logging, implementing retries, adding error tracking, or when asked about error boundaries, log aggregation, alerting, or resilience patterns.
---

# Error Handling & Observability

### When to Load

- **Trigger**: Try/catch patterns, retry logic, error responses, circuit breakers, structured logging
- **Skip**: No error handling or observability involved in the current task

## Error Handling Workflow

Copy this checklist and track progress:

```
Error Handling Progress:
- [ ] Step 1: Define error taxonomy (categories and severity)
- [ ] Step 2: Implement error handling by layer
- [ ] Step 3: Set up structured logging
- [ ] Step 4: Add retry and circuit breaker patterns
- [ ] Step 5: Configure error tracking service
- [ ] Step 6: Define user-facing error messages
- [ ] Step 7: Validate against anti-patterns checklist
```

## Error Handling Patterns by Language

### JavaScript / TypeScript

```typescript
// Custom error hierarchy
class AppError extends Error {
  constructor(
    message: string,
    public statusCode: number = 500,
    public code: string = "INTERNAL_ERROR",
    public isOperational: boolean = true,
  ) {
    super(message);
    this.name = this.constructor.name;
  }
}
class NotFoundError extends AppError {
  constructor(resource: string, id: string) {
    super(`${resource} with id ${id} not found`, 404, "NOT_FOUND");
  }
}
class ValidationError extends AppError {
  constructor(public errors: Record<string, string[]>) {
    super("Validation failed", 400, "VALIDATION_ERROR");
  }
}

// WRONG: Swallowing errors silently
try {
  await saveUser(data);
} catch (e) {
  // nothing here -- bug hides forever
}

// WRONG: Catching and re-throwing without context
try {
  await saveUser(data);
} catch (e) {
  throw e; // pointless try/catch
}

// CORRECT: Add context, handle or propagate
try {
  await saveUser(data);
} catch (error) {
  if (error instanceof ValidationError) {
    return res.status(400).json({ errors: error.errors });
  }
  logger.error("Failed to save user", { error, userId: data.id });
  throw new AppError("Unable to save user", 500, "USER_SAVE_FAILED");
}
```

### Express Global Error Handler

```typescript
// Centralized error handler middleware (must have 4 params)
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  if (err instanceof AppError) {
    logger.warn("Operational error", {
      code: err.code,
      statusCode: err.statusCode,
      path: req.path,
    });
    return res.status(err.statusCode).json({
      error: { code: err.code, message: err.message },
    });
  }

  // Unexpected errors -- these are bugs
  logger.error("Unexpected error", {
    error: err.message,
    stack: err.stack,
    path: req.path,
  });
  res.status(500).json({
    error: { code: "INTERNAL_ERROR", message: "An unexpected error occurred" },
  });
});
```

### Python

```python
# Custom exception hierarchy
class AppError(Exception):
    def __init__(self, message: str, code: str = "INTERNAL_ERROR", status: int = 500):
        self.message = message
        self.code = code
        self.status = status
        super().__init__(message)

class NotFoundError(AppError):
    def __init__(self, resource: str, id: str):
        super().__init__(f"{resource} {id} not found", "NOT_FOUND", 404)

class ValidationError(AppError):
    def __init__(self, errors: dict[str, list[str]]):
        self.errors = errors
        super().__init__("Validation failed", "VALIDATION_ERROR", 400)

# WRONG: Bare except
try:
    result = process(data)
except:  # catches SystemExit, KeyboardInterrupt too!
    pass

# CORRECT: Specific exceptions, proper logging
try:
    result = process(data)
except ValidationError as e:
    logger.warning("Validation failed", extra={"errors": e.errors})
    raise
except DatabaseError as e:
    logger.error("Database error during processing", exc_info=True)
    raise AppError("Processing failed", "PROCESS_FAILED") from e
```

### Go

```go
// Define sentinel errors and custom types
var (
    ErrNotFound     = errors.New("resource not found")
    ErrUnauthorized = errors.New("unauthorized")
)

type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation: %s - %s", e.Field, e.Message)
}

// WRONG: Ignoring errors
data, _ := json.Marshal(user)  // error silently dropped

// WRONG: Only returning error string
if err != nil {
    return fmt.Errorf("failed: %s", err.Error())  // loses error chain
}

// CORRECT: Wrap errors with context
if err != nil {
    return fmt.Errorf("saving user %s: %w", user.ID, err)  // %w preserves chain
}

// CORRECT: Check error types
if errors.Is(err, ErrNotFound) {
    http.Error(w, "Not found", http.StatusNotFound)
    return
}
var valErr *ValidationError
if errors.As(err, &valErr) {
    http.Error(w, valErr.Error(), http.StatusBadRequest)
    return
}
```

## Structured Logging

### JSON Log Format

```typescript
// WRONG: Unstructured string logs
console.log(`User ${userId} created order ${orderId} at ${new Date()}`);
// Impossible to parse, filter, or aggregate

// CORRECT: Structured JSON logs
import pino from "pino";

const logger = pino({
  level: process.env.LOG_LEVEL || "info",
  formatters: {
    level: (label) => ({ level: label }),
  },
  redact: ["req.headers.authorization", "password", "ssn"],
});
logger.info({
  event: "order_created",
  userId: "123",
  orderId: "456",
  amount: 99.99,
  currency: "USD",
});
// Output: {"level":"info","event":"order_created","userId":"123","orderId":"456",...}
```

### Correlation IDs

```typescript
// Middleware to propagate correlation ID across requests
import { randomUUID } from "crypto";
import { AsyncLocalStorage } from "async_hooks";

const asyncStorage = new AsyncLocalStorage<{ correlationId: string }>();

app.use((req, res, next) => {
  const correlationId =
    (req.headers["x-correlation-id"] as string) || randomUUID();
  res.setHeader("x-correlation-id", correlationId);

  asyncStorage.run({ correlationId }, () => next());
});

// Logger automatically includes correlation ID
function getLogger() {
  const store = asyncStorage.getStore();
  return logger.child({ correlationId: store?.correlationId });
}

// Usage in any handler or service
const log = getLogger();
log.info({ event: "payment_processed", amount: 50 });
// Output includes correlationId automatically
```

### Log Levels Guide

```
TRACE: Extremely detailed (loop iterations, variable values)  -- dev only
DEBUG: Diagnostic info (function entry/exit, state changes)   -- dev/staging
INFO:  Normal operations (request handled, job completed)     -- all envs
WARN:  Unexpected but recoverable (retry succeeded, fallback used)
ERROR: Operation failed (unhandled exception, service down)
FATAL: Application cannot continue (missing config, DB unreachable)

Production default: INFO
Never log: passwords, tokens, PII, credit cards, full request bodies
```

## Error Boundaries and Graceful Degradation

### React Error Boundary

```tsx
class ErrorBoundary extends React.Component<
  { fallback: React.ReactNode; children: React.ReactNode },
  { hasError: boolean; error?: Error }
> {
  state = { hasError: false, error: undefined };
  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }
  componentDidCatch(error: Error, info: React.ErrorInfo) {
    logger.error("React error boundary caught error", {
      error: error.message,
      componentStack: info.componentStack,
    });
  }
  render() {
    return this.state.hasError ? this.props.fallback : this.props.children;
  }
}

// Usage: wrap sections independently
<ErrorBoundary fallback={<p>Dashboard unavailable</p>}>
  <Dashboard />
</ErrorBoundary>
<ErrorBoundary fallback={<p>Sidebar unavailable</p>}>
  <Sidebar />
</ErrorBoundary>
```

### Service Degradation

```typescript
// Graceful degradation: serve stale data when service is down
async function getProductRecommendations(userId: string) {
  try {
    return await recommendationService.get(userId);
  } catch (error) {
    logger.warn("Recommendation service unavailable, using fallback", {
      userId,
      error: error.message,
    });
    return getCachedRecommendations(userId) || getDefaultRecommendations();
  }
}
```

## Retry Patterns

### Exponential Backoff

```typescript
async function withRetry<T>(
  fn: () => Promise<T>,
  options: {
    maxRetries?: number;
    baseDelay?: number;
    maxDelay?: number;
    retryOn?: (error: Error) => boolean;
  } = {},
): Promise<T> {
  const {
    maxRetries = 3,
    baseDelay = 1000,
    maxDelay = 30000,
    retryOn,
  } = options;
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (attempt === maxRetries) throw error;
      if (retryOn && !retryOn(error as Error)) throw error;

      const delay = Math.min(
        baseDelay * 2 ** attempt + Math.random() * 1000,
        maxDelay,
      );
      logger.warn("Retrying operation", { attempt: attempt + 1, delay });
      await new Promise((r) => setTimeout(r, delay));
    }
  }
  throw new Error("Unreachable");
}

// Usage: retry only on transient errors
const data = await withRetry(() => fetch("https://api.example.com/data"), {
  retryOn: (err) => err.message.includes("ECONNRESET"),
});
```

### Circuit Breaker

```typescript
class CircuitBreaker {
  private failures = 0;
  private lastFailure = 0;
  private state: "closed" | "open" | "half-open" = "closed";

  constructor(
    private threshold: number = 5,
    private resetTimeout: number = 60000,
  ) {}

  async execute<T>(fn: () => Promise<T>, fallback?: () => T): Promise<T> {
    if (this.state === "open") {
      if (Date.now() - this.lastFailure > this.resetTimeout) {
        this.state = "half-open";
      } else {
        if (fallback) return fallback();
        throw new Error("Circuit breaker is open");
      }
    }

    try {
      const result = await fn();
      this.failures = 0;
      this.state = "closed";
      return result;
    } catch (error) {
      this.failures++;
      this.lastFailure = Date.now();
      if (this.failures >= this.threshold) this.state = "open";
      if (fallback) return fallback();
      throw error;
    }
  }
}

// Usage: trips open after 5 failures, resets after 30s
const paymentCircuit = new CircuitBreaker(5, 30000);
const result = await paymentCircuit.execute(
  () => paymentService.charge(amount),
  () => ({ queued: true, message: "Payment will be processed shortly" }),
);
```

## Error Tracking Integration

### Sentry Setup

```typescript
import * as Sentry from "@sentry/node";

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: process.env.NODE_ENV === "production" ? 0.1 : 1.0,
  beforeSend(event) {
    // Scrub sensitive data
    if (event.request?.headers) delete event.request.headers["authorization"];
    return event;
  },
});

Sentry.setUser({ id: user.id, email: user.email });
Sentry.captureException(error, {
  tags: { subsystem: "payment", provider: "stripe" },
  extra: { orderId, amount },
});
```

## User-Facing vs Internal Errors

```typescript
// Map internal errors to user-friendly messages
const USER_MESSAGES: Record<string, string> = {
  VALIDATION_ERROR: "Please check your input and try again.",
  NOT_FOUND: "The requested resource could not be found.",
  RATE_LIMITED: "Too many requests. Please wait a moment.",
  PAYMENT_FAILED: "Payment could not be processed. Please try another method.",
  INTERNAL_ERROR: "Something went wrong. Please try again later.",
};

function toUserResponse(error: AppError) {
  return {
    error: {
      code: error.code,
      message: USER_MESSAGES[error.code] || USER_MESSAGES["INTERNAL_ERROR"],
    },
  };
}

// WRONG: Exposing internal details to users
res.status(500).json({
  error: 'QueryFailedError: relation "users" does not exist',
  stack: error.stack,
});

// CORRECT: Generic message to user, full details in logs
logger.error("Database query failed", {
  error: error.message,
  stack: error.stack,
  query,
});
res.status(500).json(toUserResponse(new AppError("DB error", 500)));
```

## Common Anti-Patterns Summary

```
AVOID                              DO INSTEAD
-------------------------------------------------------------------
Empty catch blocks                 Log and handle or re-throw
Bare `except:` in Python           Catch specific exceptions
console.log for production         Structured logger (pino, winston)
Logging passwords/tokens           Redact sensitive fields
Retry without backoff              Exponential backoff with jitter
Retry on all errors                Only retry transient/network errors
No circuit breaker                 Circuit breaker for external calls
Exposing stack traces to users     Generic user messages, detailed logs
No correlation IDs                 Propagate correlation ID across services
One giant try/catch                Granular error handling per operation
Logging inside tight loops         Log summaries/aggregates
No error boundaries in React       Wrap independent sections separately
```
