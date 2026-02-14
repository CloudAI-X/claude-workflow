---
name: security-patterns
description: Implements authentication, authorization, encryption, secrets management, and security hardening patterns. Use when designing auth flows, managing secrets, configuring CORS, implementing rate limiting, or when asked about JWT, OAuth, password hashing, API keys, RBAC, or security best practices.
---

# Security Patterns

### When to Load

- **Trigger**: Auth flows, encryption, secrets management, CORS configuration, input validation, rate limiting
- **Skip**: No security surface involved in the current task

## Security Implementation Workflow

Copy this checklist and track progress:

```
Security Implementation Progress:
- [ ] Step 1: Choose authentication strategy
- [ ] Step 2: Implement authorization model
- [ ] Step 3: Set up password hashing
- [ ] Step 4: Configure secrets management
- [ ] Step 5: Enable encryption (transit + rest)
- [ ] Step 6: Configure CORS
- [ ] Step 7: Add rate limiting
- [ ] Step 8: Validate against anti-patterns checklist
```

## Authentication Patterns

### JWT (JSON Web Tokens)

```typescript
import jwt from "jsonwebtoken";

function generateTokens(user: User) {
  const accessToken = jwt.sign(
    { sub: user.id, role: user.role },
    process.env.JWT_SECRET!,
    { expiresIn: "15m", algorithm: "HS256" },
  );
  const refreshToken = jwt.sign(
    { sub: user.id, tokenVersion: user.tokenVersion },
    process.env.JWT_REFRESH_SECRET!,
    { expiresIn: "7d" },
  );
  return { accessToken, refreshToken };
}

// WRONG: localStorage (XSS vulnerable) | CORRECT: httpOnly cookie for refresh, memory for access
res.cookie("refreshToken", refreshToken, {
  httpOnly: true,
  secure: true,
  sameSite: "strict",
  maxAge: 7 * 24 * 60 * 60 * 1000,
  path: "/api/auth/refresh",
});
```

### JWT Verification Middleware

```typescript
function authenticate(req: Request, res: Response, next: NextFunction) {
  const header = req.headers.authorization;
  if (!header?.startsWith("Bearer ")) {
    return res.status(401).json({ error: "Missing token" });
  }

  try {
    const token = header.slice(7);
    const payload = jwt.verify(token, process.env.JWT_SECRET!) as JwtPayload;
    req.user = { id: payload.sub, role: payload.role };
    next();
  } catch (err) {
    if (err instanceof jwt.TokenExpiredError) {
      return res.status(401).json({ error: "Token expired" });
    }
    return res.status(401).json({ error: "Invalid token" });
  }
}
```

### Session-Based Auth

```typescript
import session from "express-session";
import RedisStore from "connect-redis";

app.use(
  session({
    store: new RedisStore({ client: redisClient }),
    secret: process.env.SESSION_SECRET!,
    resave: false,
    saveUninitialized: false,
    cookie: {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "strict",
      maxAge: 24 * 60 * 60 * 1000, // 24 hours
    },
  }),
);
```

### OAuth 2.0 / OIDC Flow Summary

```
Authorization Code Flow (web apps with backend):
1. Redirect to provider: /authorize?response_type=code&client_id=...&redirect_uri=...&scope=openid email
2. User authenticates, provider redirects back with ?code=AUTHORIZATION_CODE
3. Backend exchanges code for tokens (POST /token with client_secret)
4. Backend receives access_token + id_token, creates session/JWT

PKCE Flow (SPAs, mobile): Same but with code_verifier/code_challenge instead of client_secret
NEVER use Implicit Flow (deprecated, tokens exposed in URL)
```

### API Key Authentication

```typescript
async function authenticateApiKey(
  req: Request,
  res: Response,
  next: NextFunction,
) {
  const apiKey = req.headers["x-api-key"] as string;
  if (!apiKey) return res.status(401).json({ error: "API key required" });

  // WRONG: Direct comparison (timing attack) | CORRECT: Hash-based lookup
  const hashedKey = crypto.createHash("sha256").update(apiKey).digest("hex");
  const keyRecord = await db.apiKey.findUnique({ where: { hash: hashedKey } });
  if (!keyRecord || keyRecord.revokedAt)
    return res.status(401).json({ error: "Invalid API key" });

  req.apiClient = { id: keyRecord.clientId, scopes: keyRecord.scopes };
  next();
}
```

## Authorization Models

### RBAC (Role-Based Access Control)

```typescript
const PERMISSIONS = {
  admin: [
    "users:read",
    "users:write",
    "users:delete",
    "posts:read",
    "posts:write",
    "posts:delete",
  ],
  editor: ["posts:read", "posts:write", "posts:delete", "users:read"],
  viewer: ["posts:read", "users:read"],
} as const;

type Role = keyof typeof PERMISSIONS;

function authorize(...requiredPermissions: string[]) {
  return (req: Request, res: Response, next: NextFunction) => {
    const userPermissions = PERMISSIONS[req.user.role as Role] || [];
    const hasPermission = requiredPermissions.every((p) =>
      (userPermissions as readonly string[]).includes(p),
    );
    if (!hasPermission)
      return res.status(403).json({ error: "Insufficient permissions" });
    next();
  };
}

// Usage: app.delete("/api/users/:id", authenticate, authorize("users:delete"), deleteUser);
```

### Resource-Level Authorization

```typescript
// WRONG: Only checking role, not ownership -- any editor can edit ANY post
// CORRECT: Check ownership or admin role
app.put(
  "/api/posts/:id",
  authenticate,
  authorize("posts:write"),
  async (req, res) => {
    const post = await db.post.findUnique({ where: { id: req.params.id } });
    if (!post) return res.status(404).json({ error: "Not found" });
    if (post.authorId !== req.user.id && req.user.role !== "admin") {
      return res
        .status(403)
        .json({ error: "Not authorized to edit this post" });
    }
    await db.post.update({ where: { id: req.params.id }, data: req.body });
  },
);
```

## Password Handling

```typescript
import bcrypt from "bcrypt";
// WRONG: plaintext or MD5/SHA256 (too fast, brute-forceable)
// CORRECT: bcrypt with appropriate cost factor
const SALT_ROUNDS = 12; // ~250ms on modern hardware

async function hashPassword(password: string): Promise<string> {
  return bcrypt.hash(password, SALT_ROUNDS);
}
async function verifyPassword(
  password: string,
  hash: string,
): Promise<boolean> {
  return bcrypt.compare(password, hash); // constant-time comparison built-in
}

// Registration
await db.user.create({
  data: { email, password: await hashPassword(req.body.password) },
});

// Login -- WRONG: "Invalid password" (reveals email exists) | CORRECT: generic message
const user = await db.user.findUnique({ where: { email } });
if (!user || !(await verifyPassword(req.body.password, user.password))) {
  return res.status(401).json({ error: "Invalid email or password" });
}
```

### Password Policies

```typescript
function validatePassword(password: string): string[] {
  const errors: string[] = [];
  if (password.length < 12) errors.push("Minimum 12 characters");
  if (password.length > 128) errors.push("Maximum 128 characters");

  // Check against breached password lists (haveibeenpwned API or local)
  // Do NOT enforce arbitrary complexity rules (uppercase + number + symbol)
  // NIST 800-63B recommends length over complexity
  return errors;
}
```

## Secrets Management

```python
# WRONG: Hardcoded values in source code
# API_KEY = "some-value-here"

# CORRECT: Environment variables loaded from .env
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")
db_url = os.getenv("DATABASE_URL")

# CORRECT: Secrets manager for production
# AWS: Secrets Manager, Parameter Store
# GCP: Secret Manager
# HashiCorp Vault for self-hosted
```

### Secret Rotation

```
1. Generate new secret value
2. Deploy code that accepts BOTH old and new values
3. Update all consumers to use the new value
4. Verify old value is no longer in use
5. Revoke old value

Never: Rotate in-place without a transition period
```

## Encryption Patterns

### In Transit

```typescript
// Redirect HTTP to HTTPS in production
app.use((req, res, next) => {
  if (
    req.headers["x-forwarded-proto"] !== "https" &&
    process.env.NODE_ENV === "production"
  ) {
    return res.redirect(301, `https://${req.hostname}${req.url}`);
  }
  next();
});
// HSTS header
app.use((req, res, next) => {
  res.setHeader(
    "Strict-Transport-Security",
    "max-age=31536000; includeSubDomains",
  );
  next();
});
```

### At Rest

```typescript
import crypto from "crypto";
const ALGORITHM = "aes-256-gcm";

function encrypt(
  plaintext: string,
  key: Buffer,
): { ciphertext: string; iv: string; tag: string } {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv(ALGORITHM, key, iv);
  let ciphertext =
    cipher.update(plaintext, "utf8", "hex") + cipher.final("hex");
  return {
    ciphertext,
    iv: iv.toString("hex"),
    tag: cipher.getAuthTag().toString("hex"),
  };
}

function decrypt(
  ciphertext: string,
  key: Buffer,
  iv: string,
  tag: string,
): string {
  const decipher = crypto.createDecipheriv(
    ALGORITHM,
    key,
    Buffer.from(iv, "hex"),
  );
  decipher.setAuthTag(Buffer.from(tag, "hex"));
  return decipher.update(ciphertext, "hex", "utf8") + decipher.final("utf8");
}
// Use for PII, sensitive data. Encryption key in secrets manager, NOT in code.
```

## CORS Configuration

```typescript
import cors from "cors";

// WRONG: Allow everything
app.use(cors()); // origin: *, credentials: false

// WRONG: Wildcard with credentials
app.use(cors({ origin: "*", credentials: true })); // browsers reject this

// CORRECT: Explicit allowed origins
const ALLOWED_ORIGINS = [
  "https://myapp.com",
  "https://admin.myapp.com",
  ...(process.env.NODE_ENV !== "production" ? ["http://localhost:3000"] : []),
];

app.use(
  cors({
    origin: (origin, callback) => {
      if (!origin || ALLOWED_ORIGINS.includes(origin)) {
        callback(null, true);
      } else {
        callback(new Error("Not allowed by CORS"));
      }
    },
    credentials: true,
    methods: ["GET", "POST", "PUT", "PATCH", "DELETE"],
    allowedHeaders: ["Content-Type", "Authorization"],
    maxAge: 86400, // cache preflight for 24 hours
  }),
);
```

## Rate Limiting

```typescript
import rateLimit from "express-rate-limit";
import RedisStore from "rate-limit-redis";

// Global rate limit
app.use(
  rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100, // 100 requests per window
    standardHeaders: true, // RateLimit-* headers
    legacyHeaders: false,
    store: new RedisStore({
      sendCommand: (...args) => redisClient.sendCommand(args),
    }),
  }),
);

// Strict limit on auth endpoints
app.use(
  "/api/auth/login",
  rateLimit({
    windowMs: 15 * 60 * 1000,
    max: 5, // 5 login attempts per 15 min
    message: { error: "Too many login attempts. Try again later." },
  }),
);

// Per-API-key rate limiting for developer APIs
app.use(
  "/api/v1/",
  rateLimit({
    windowMs: 60 * 1000, // 1 minute
    max: 60, // 60 requests per minute
    keyGenerator: (req) => req.apiClient?.id || req.ip,
  }),
);
```

## Security Headers

```typescript
import helmet from "helmet";

app.use(helmet()); // Sets many secure headers at once

// Key headers helmet sets:
// X-Content-Type-Options: nosniff
// X-Frame-Options: DENY
// Strict-Transport-Security: max-age=15552000; includeSubDomains
// Content-Security-Policy: default-src 'self'

// Customize CSP for your app
app.use(
  helmet.contentSecurityPolicy({
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", "data:", "https://cdn.example.com"],
      connectSrc: ["'self'", "https://api.example.com"],
    },
  }),
);
```

## Input Validation

```typescript
import { z } from "zod";

// WRONG: Trusting user input directly (SQL injection risk)
app.post("/api/users", (req, res) => {
  db.query(`SELECT * FROM users WHERE email = '${req.body.email}'`);
});

// CORRECT: Validate with schema, use parameterized queries
const CreateUserSchema = z.object({
  email: z.string().email().max(255),
  name: z.string().min(1).max(100).trim(),
  age: z.number().int().min(13).max(150).optional(),
});

app.post("/api/users", async (req, res) => {
  const result = CreateUserSchema.safeParse(req.body);
  if (!result.success) {
    return res.status(400).json({ errors: result.error.flatten() });
  }
  // Use parameterized query (ORM or prepared statement)
  await db.user.create({ data: result.data });
});
```

## Common Anti-Patterns Summary

```
AVOID                              DO INSTEAD
-------------------------------------------------------------------
JWT in localStorage                httpOnly secure cookie (refresh), memory (access)
MD5/SHA for passwords              bcrypt or argon2 with proper cost factor
Hardcoded secrets in code          Environment variables + secrets manager
cors({ origin: '*' })             Explicit allowed origins list
"Invalid password" message         "Invalid email or password" (no enumeration)
No rate limiting on auth           Strict rate limits on login/register
Rolling your own crypto            Use established libraries (jose, bcrypt)
Trusting user input                Validate with zod/joi, parameterized queries
Same API key forever               Rotate keys regularly, support multiple active
No HTTPS redirect                  Force HTTPS + HSTS header
Symmetric JWT for multi-service    Use RS256/ES256 (asymmetric) for distributed
No input length limits             Max length on all string inputs
```
