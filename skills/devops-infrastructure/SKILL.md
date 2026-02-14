---
name: devops-infrastructure
description: Guides Docker, CI/CD pipelines, deployment strategies, infrastructure as code, and observability setup. Use when writing Dockerfiles, configuring GitHub Actions, planning deployments, setting up monitoring, or when asked about containers, pipelines, Terraform, or production infrastructure.
---

# DevOps & Infrastructure

### When to Load

- **Trigger**: Docker, CI/CD pipelines, deployment configuration, monitoring, infrastructure as code
- **Skip**: Application logic only with no infrastructure or deployment concerns

## DevOps Workflow

Copy this checklist and track progress:

```
DevOps Setup Progress:
- [ ] Step 1: Containerize application (Dockerfile)
- [ ] Step 2: Set up CI/CD pipeline
- [ ] Step 3: Define deployment strategy
- [ ] Step 4: Configure monitoring & alerting
- [ ] Step 5: Set up environment management
- [ ] Step 6: Document runbooks
- [ ] Step 7: Validate against anti-patterns checklist
```

## Docker Best Practices

### Multi-Stage Build

```dockerfile
# WRONG: Single stage, bloated image
FROM node:20
WORKDIR /app
COPY . .
RUN npm install
RUN npm run build
CMD ["node", "dist/index.js"]
# Result: 1.2GB image with devDependencies and source code

# CORRECT: Multi-stage build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
RUN addgroup -g 1001 appgroup && adduser -u 1001 -G appgroup -s /bin/sh -D appuser
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./
USER appuser
EXPOSE 3000
CMD ["node", "dist/index.js"]
# Result: ~150MB image, no devDependencies, non-root user
```

### Python Multi-Stage

```dockerfile
FROM python:3.12-slim AS builder
WORKDIR /app
RUN pip install uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
COPY . .

FROM python:3.12-slim AS runner
WORKDIR /app
RUN useradd -r -s /bin/false appuser
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src ./src
ENV PATH="/app/.venv/bin:$PATH"
USER appuser
CMD ["python", "-m", "src.main"]
```

### Layer Caching

```dockerfile
# WRONG: Cache busted on every code change
COPY . .
RUN npm ci

# CORRECT: Dependencies cached separately
COPY package*.json ./
RUN npm ci                  # cached unless package.json changes
COPY . .                    # only source code changes bust this layer
```

### .dockerignore

```
node_modules
.git
.env
*.md
.vscode
coverage
dist
__pycache__
.pytest_cache
*.pyc
```

### Security

```dockerfile
# Always pin versions
FROM node:20.11.0-alpine   # NOT node:latest

# Don't run as root
USER appuser

# Read-only filesystem where possible
# docker run --read-only --tmpfs /tmp myapp

# Scan images
# docker scout cves myimage:latest
# trivy image myimage:latest
```

## CI/CD Pipeline Design

### GitHub Actions Structure

```yaml
name: CI/CD
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: "npm"
      - run: npm ci
      - run: npm run lint

  test:
    runs-on: ubuntu-latest
    needs: lint
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: testdb
        ports: ["5432:5432"]
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: "npm"
      - run: npm ci
      - run: npm test

  build:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/build-push-action@v5
        with:
          push: ${{ github.event_name == 'push' }}
          tags: ghcr.io/${{ github.repository }}:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy:
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main'
    environment: production
    steps:
      - run: echo "Deploy to production"
```

### Caching Strategies

```yaml
# Node modules
- uses: actions/setup-node@v4
  with:
    cache: "npm"

# Python with uv
- name: Cache uv
  uses: actions/cache@v4
  with:
    path: ~/.cache/uv
    key: uv-${{ runner.os }}-${{ hashFiles('uv.lock') }}

# Docker layer caching
- uses: docker/build-push-action@v5
  with:
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

## Deployment Strategies

### Blue-Green Deployment

```
1. Run two identical environments: Blue (live) and Green (idle)
2. Deploy new version to Green
3. Run smoke tests on Green
4. Switch load balancer to Green
5. Green is now live, Blue is idle
6. Rollback: switch back to Blue

Pros: Instant rollback, zero downtime
Cons: 2x infrastructure cost during deploy
```

### Canary Deployment

```
1. Deploy new version to small subset (5% of traffic)
2. Monitor error rates and latency
3. Gradually increase: 5% -> 25% -> 50% -> 100%
4. Rollback: route all traffic back to old version

Pros: Limited blast radius, real-world testing
Cons: More complex routing, longer rollout
```

### Rolling Deployment

```
1. Replace instances one at a time
2. Each new instance passes health checks before next starts
3. Continue until all instances updated

Pros: No extra infrastructure, gradual rollout
Cons: Mixed versions during deploy, slower rollback
```

### Feature Flags

```typescript
// Simple feature flag implementation
const features = {
  NEW_CHECKOUT: process.env.FF_NEW_CHECKOUT === "true",
  DARK_MODE: process.env.FF_DARK_MODE === "true",
};

function getCheckoutFlow(user: User) {
  if (features.NEW_CHECKOUT && user.betaGroup) {
    return newCheckoutFlow(user);
  }
  return legacyCheckoutFlow(user);
}

// Use a proper service for production: LaunchDarkly, Unleash, Flagsmith
```

## Infrastructure as Code

### Terraform Basics

```hcl
# main.tf
terraform {
  required_version = ">= 1.5"
  backend "s3" {
    bucket = "myapp-terraform-state"
    key    = "prod/terraform.tfstate"
    region = "us-east-1"
  }
}

resource "aws_instance" "web" {
  ami           = var.ami_id
  instance_type = var.instance_type
  tags = {
    Name        = "web-${var.environment}"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

# variables.tf
variable "environment" {
  type    = string
  default = "dev"
}

variable "instance_type" {
  type    = string
  default = "t3.micro"
}
```

### Terraform Rules

```
1. Always use remote state (S3, GCS, Terraform Cloud)
2. Lock state files to prevent concurrent modifications
3. Use variables and modules for reusability
4. Tag all resources with environment and ManagedBy
5. Run `terraform plan` before `terraform apply`
6. Never edit infrastructure manually (all changes via code)
7. Use workspaces or separate state files per environment
```

## Monitoring & Observability

### The Three Pillars

```
METRICS: Numeric measurements over time
  - Request rate, error rate, latency (RED method)
  - CPU, memory, disk, network (USE method)
  - Business metrics (signups, purchases)
  Tools: Prometheus, Datadog, CloudWatch

LOGS: Discrete events with context
  - Structured JSON format
  - Correlation IDs across services
  - Log levels: DEBUG, INFO, WARN, ERROR
  Tools: ELK Stack, Loki, CloudWatch Logs

TRACES: Request flow across services
  - Distributed tracing with span context
  - Latency breakdown per service
  - Dependency mapping
  Tools: Jaeger, Zipkin, Datadog APM
```

### Health Check Endpoint

```typescript
// Express health check
app.get("/health", async (req, res) => {
  const checks = {
    uptime: process.uptime(),
    timestamp: Date.now(),
    database: "unknown",
    redis: "unknown",
  };

  try {
    await db.query("SELECT 1");
    checks.database = "healthy";
  } catch (e) {
    checks.database = "unhealthy";
  }

  try {
    await redis.ping();
    checks.redis = "healthy";
  } catch (e) {
    checks.redis = "unhealthy";
  }

  const isHealthy = checks.database === "healthy";
  res.status(isHealthy ? 200 : 503).json(checks);
});
```

### Alerting Rules

```
Good alerts:
- Error rate > 1% for 5 minutes (actionable)
- P99 latency > 2s for 10 minutes (meaningful)
- Disk usage > 80% (preventive)

Bad alerts:
- CPU spike for 30 seconds (too noisy)
- Any single 500 error (too sensitive)
- "Something might be wrong" (not actionable)

Alert fatigue is real. Every alert should require human action.
```

## Environment Management

### Dev/Staging/Prod Parity

```yaml
# docker-compose.yml for local development
services:
  app:
    build: .
    env_file: .env
    ports: ["3000:3000"]
    depends_on:
      postgres:
        condition: service_healthy

  postgres:
    image: postgres:16
    environment:
      POSTGRES_DB: myapp
    healthcheck:
      test: ["CMD-SHELL", "pg_isready"]
      interval: 5s
    volumes:
      - pgdata:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]

volumes:
  pgdata:
```

### Environment Variables

```
# .env.example (committed to git, no real values)
DATABASE_URL=postgresql://user:placeholder@localhost:5432/myapp
REDIS_URL=redis://localhost:6379
LOG_LEVEL=debug
API_KEY=your-key-here

# .env (never committed, listed in .gitignore)
# Contains real values for local development
```

## Common Anti-Patterns Summary

```
AVOID                              DO INSTEAD
-------------------------------------------------------------------
FROM node:latest                   Pin exact versions (node:20.11.0-alpine)
Running as root in container       Create and use non-root user
No .dockerignore                   Exclude .git, node_modules, .env
Single CI job does everything      Separate lint, test, build, deploy stages
Manual deployment                  Automated pipeline with approvals
No health checks                   Liveness + readiness probes
Alerts on every error              Alert on error RATE thresholds
Same config in all environments    Per-environment configuration
No rollback plan                   Test rollback before every deploy
Logs as unstructured strings       Structured JSON logs with correlation IDs
```
