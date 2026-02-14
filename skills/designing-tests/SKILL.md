---
name: designing-tests
description: Designs and implements testing strategies for any codebase. Use when adding tests, improving coverage, setting up testing infrastructure, debugging test failures, or when asked about unit tests, integration tests, or E2E testing.
---

# Designing Tests

### When to Load

- **Trigger**: Adding tests, test strategy planning, improving coverage, setting up testing infrastructure
- **Skip**: Non-test code changes where testing is not part of the task

## Test Implementation Workflow

Copy this checklist and track progress:

```
Test Implementation Progress:
- [ ] Step 1: Identify what to test
- [ ] Step 2: Select appropriate test type
- [ ] Step 3: Write tests following templates
- [ ] Step 4: Run tests and verify passing
- [ ] Step 5: Check coverage meets targets
- [ ] Step 6: Fix any failing tests
```

## Testing Pyramid

Apply the testing pyramid for balanced coverage:

```
        /\
       /  \     E2E Tests (10%)
      /----\    - Critical user journeys
     /      \   - Slow but comprehensive
    /--------\  Integration Tests (20%)
   /          \ - Component interactions
  /------------\ - API contracts
 /              \ Unit Tests (70%)
/________________\ - Fast, isolated
                   - Business logic focus
```

## Framework Selection

### JavaScript/TypeScript

| Type        | Recommended     | Alternative      |
| ----------- | --------------- | ---------------- |
| Unit        | Vitest          | Jest             |
| Integration | Vitest + MSW    | Jest + SuperTest |
| E2E         | Playwright      | Cypress          |
| Component   | Testing Library | Enzyme           |

### Python

| Type        | Recommended                 | Alternative       |
| ----------- | --------------------------- | ----------------- |
| Unit        | pytest                      | unittest          |
| Integration | pytest + httpx              | pytest + requests |
| E2E         | Playwright                  | Selenium          |
| API         | pytest + FastAPI TestClient | -                 |

### Go

| Type        | Recommended        |
| ----------- | ------------------ |
| Unit        | testing + testify  |
| Integration | testing + httptest |
| E2E         | testing + chromedp |

## Test Structure Templates

### Unit Test

```javascript
describe("[Unit] ComponentName", () => {
  describe("methodName", () => {
    it("should [expected behavior] when [condition]", () => {
      // Arrange
      const input = createTestInput();

      // Act
      const result = methodName(input);

      // Assert
      expect(result).toEqual(expectedOutput);
    });

    it("should throw error when [invalid condition]", () => {
      expect(() => methodName(invalidInput)).toThrow(ExpectedError);
    });
  });
});
```

### Integration Test

```javascript
describe("[Integration] API /users", () => {
  beforeAll(async () => {
    await setupTestDatabase();
  });

  afterAll(async () => {
    await teardownTestDatabase();
  });

  it("should create user and return 201", async () => {
    const response = await request(app)
      .post("/users")
      .send({ name: "Test", email: "test@example.com" });

    expect(response.status).toBe(201);
    expect(response.body.id).toBeDefined();
  });
});
```

### E2E Test

```javascript
describe("[E2E] User Registration Flow", () => {
  it("should complete registration successfully", async ({ page }) => {
    await page.goto("/register");

    await page.fill('[data-testid="email"]', "new@example.com");
    await page.fill('[data-testid="password"]', "SecurePass123!");
    await page.click('[data-testid="submit"]');

    await expect(page.locator(".welcome-message")).toBeVisible();
    await expect(page).toHaveURL("/dashboard");
  });
});
```

## Coverage Strategy

### What to Cover

- ✅ Business logic (100%)
- ✅ Edge cases and error handling (90%+)
- ✅ API contracts (100%)
- ✅ Critical user paths (E2E)
- ⚠️ UI components (snapshot + interaction)
- ❌ Third-party library internals
- ❌ Simple getters/setters

### Coverage Thresholds

```json
{
  "coverageThreshold": {
    "global": {
      "branches": 80,
      "functions": 80,
      "lines": 80,
      "statements": 80
    },
    "src/core/": {
      "branches": 95,
      "functions": 95
    }
  }
}
```

## Test Data Management

### Factories/Builders

```javascript
// factories/user.js
export const userFactory = (overrides = {}) => ({
  id: faker.string.uuid(),
  name: faker.person.fullName(),
  email: faker.internet.email(),
  createdAt: new Date(),
  ...overrides,
});

// Usage
const admin = userFactory({ role: "admin" });
```

### Fixtures

```javascript
// fixtures/users.json
{
  "validUser": { "name": "Test", "email": "test@example.com" },
  "invalidUser": { "name": "", "email": "invalid" }
}
```

## Mocking Strategy

### When to Mock

- ✅ External APIs and services
- ✅ Database in unit tests
- ✅ Time/Date for determinism
- ✅ Random values
- ❌ Internal modules (usually)
- ❌ The code under test

### Mock Examples

```javascript
// API mocking with MSW
import { http, HttpResponse } from "msw";

export const handlers = [
  http.get("/api/users", () => {
    return HttpResponse.json([{ id: 1, name: "John" }]);
  }),
];

// Time mocking
vi.useFakeTimers();
vi.setSystemTime(new Date("2024-01-01"));
```

## Test Validation Loop

After writing tests, run this validation:

```
Test Validation:
- [ ] All tests pass: `npm test`
- [ ] Coverage meets thresholds: `npm test -- --coverage`
- [ ] No flaky tests (run multiple times)
- [ ] Tests are independent (order doesn't matter)
- [ ] Test names clearly describe behavior
```

If any tests fail, fix them before proceeding. If coverage is below target, add more tests for uncovered code paths.

```bash
# Run tests
npm test

# Run with coverage
npm test -- --coverage

# Run specific test file
npm test -- path/to/test.spec.ts

# Run in watch mode during development
npm test -- --watch
```
