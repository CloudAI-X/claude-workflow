---
name: designing-apis
description: Designs REST and GraphQL APIs including endpoints, error handling, versioning, and documentation. Use when creating new APIs, designing endpoints, reviewing API contracts, or when asked about REST, GraphQL, or API patterns.
---

# Designing APIs

### When to Load

- **Trigger**: Designing REST or GraphQL endpoints, API contracts, versioning, request/response formats
- **Skip**: Internal-only code with no API surface

## API Design Workflow

Copy this checklist and track progress:

```
API Design Progress:
- [ ] Step 1: Define resources and relationships
- [ ] Step 2: Design endpoint structure
- [ ] Step 3: Define request/response formats
- [ ] Step 4: Plan error handling
- [ ] Step 5: Add authentication/authorization
- [ ] Step 6: Document with OpenAPI spec
- [ ] Step 7: Validate design against checklist
```

## REST API Design

### URL Structure

```
# Resource-based URLs (nouns, not verbs)
GET    /users              # List users
GET    /users/:id          # Get user
POST   /users              # Create user
PUT    /users/:id          # Replace user
PATCH  /users/:id          # Update user
DELETE /users/:id          # Delete user

# Nested resources
GET    /users/:id/orders   # User's orders
POST   /users/:id/orders   # Create order for user

# Query parameters for filtering/pagination
GET    /users?role=admin&status=active
GET    /users?page=2&limit=20&sort=-createdAt
```

### HTTP Status Codes

| Code | Meaning           | Use Case                   |
| ---- | ----------------- | -------------------------- |
| 200  | OK                | Successful GET, PUT, PATCH |
| 201  | Created           | Successful POST            |
| 204  | No Content        | Successful DELETE          |
| 400  | Bad Request       | Invalid input              |
| 401  | Unauthorized      | Missing/invalid auth       |
| 403  | Forbidden         | Valid auth, no permission  |
| 404  | Not Found         | Resource doesn't exist     |
| 409  | Conflict          | Duplicate, state conflict  |
| 422  | Unprocessable     | Validation failed          |
| 429  | Too Many Requests | Rate limited               |
| 500  | Internal Error    | Server error               |

### Response Formats

**Success Response:**

```json
{
  "data": {
    "id": "123",
    "type": "user",
    "attributes": {
      "name": "John Doe",
      "email": "john@example.com"
    }
  },
  "meta": {
    "requestId": "abc-123"
  }
}
```

**List Response with Pagination:**

```json
{
  "data": [...],
  "meta": {
    "total": 100,
    "page": 1,
    "limit": 20,
    "totalPages": 5
  },
  "links": {
    "self": "/users?page=1",
    "next": "/users?page=2",
    "last": "/users?page=5"
  }
}
```

**Error Response:**

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "email",
        "message": "Must be a valid email address"
      }
    ]
  },
  "meta": {
    "requestId": "abc-123"
  }
}
```

## API Versioning

**URL Versioning (Recommended):**

```
/api/v1/users
/api/v2/users
```

**Header Versioning:**

```
Accept: application/vnd.api+json; version=1
```

## Authentication Patterns

**JWT Bearer Token:**

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

**API Key:**

```
X-API-Key: your-api-key
```

## Rate Limiting Headers

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1609459200
Retry-After: 60
```

## GraphQL Patterns

**Schema Design:**

```graphql
type Query {
  user(id: ID!): User
  users(filter: UserFilter, pagination: Pagination): UserConnection!
}

type Mutation {
  createUser(input: CreateUserInput!): UserPayload!
  updateUser(id: ID!, input: UpdateUserInput!): UserPayload!
}

type User {
  id: ID!
  name: String!
  email: String!
  orders(first: Int, after: String): OrderConnection!
}

input CreateUserInput {
  name: String!
  email: String!
}

type UserPayload {
  user: User
  errors: [Error!]
}
```

## OpenAPI Specification Template

See [OPENAPI-TEMPLATE.md](OPENAPI-TEMPLATE.md) for the full OpenAPI 3.0 specification template.

## API Design Validation

After completing the design, validate against this checklist:

```
Validation Checklist:
- [ ] All endpoints use nouns, not verbs
- [ ] HTTP methods match operations correctly
- [ ] Consistent response format across endpoints
- [ ] Error responses include actionable details
- [ ] Pagination implemented for list endpoints
- [ ] Authentication defined for protected endpoints
- [ ] Rate limiting headers documented
- [ ] OpenAPI spec is complete and valid
```

If validation fails, return to the relevant design step and address the issues.

## Security Checklist

- [ ] HTTPS only
- [ ] Authentication on all endpoints
- [ ] Authorization checks
- [ ] Input validation
- [ ] Rate limiting
- [ ] Request size limits
- [ ] CORS properly configured
- [ ] No sensitive data in URLs
- [ ] Audit logging
