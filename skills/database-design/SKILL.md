---
name: database-design
description: Designs database schemas, indexing strategies, query optimization, and migration patterns for SQL and NoSQL databases. Use when designing tables, optimizing queries, fixing N+1 problems, planning migrations, or when asked about database performance, normalization, ORMs, or data modeling.
---

# Database Design

### When to Load

- **Trigger**: Schema design, migrations, query optimization, indexing strategies, data modeling, N+1 fixes
- **Skip**: No database work involved in the current task

## Database Design Workflow

Copy this checklist and track progress:

```
Database Design Progress:
- [ ] Step 1: Identify entities and relationships
- [ ] Step 2: Normalize schema (3NF minimum)
- [ ] Step 3: Evaluate denormalization needs
- [ ] Step 4: Design indexes for query patterns
- [ ] Step 5: Write and optimize critical queries
- [ ] Step 6: Plan migration strategy
- [ ] Step 7: Configure connection pooling
- [ ] Step 8: Validate against anti-patterns checklist
```

## Schema Design Principles

### Normalization Forms

```
1NF: Atomic values, no repeating groups
2NF: 1NF + no partial dependencies (all non-key columns depend on full PK)
3NF: 2NF + no transitive dependencies (non-key columns don't depend on other non-key columns)
```

```sql
-- WRONG: Unnormalized
CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  customer_name TEXT,
  customer_email TEXT,        -- duplicated across orders
  product1_name TEXT,         -- repeating groups
  product1_qty INT,
  product2_name TEXT,
  product2_qty INT
);

-- CORRECT: Normalized to 3NF
CREATE TABLE customers (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL
);

CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  customer_id INT REFERENCES customers(id),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE order_items (
  id SERIAL PRIMARY KEY,
  order_id INT REFERENCES orders(id),
  product_id INT REFERENCES products(id),
  quantity INT NOT NULL CHECK (quantity > 0)
);
```

### When to Denormalize

Denormalize only when you have measured proof of performance issues:

```sql
-- Acceptable denormalization: precomputed counter to avoid COUNT(*)
ALTER TABLE posts ADD COLUMN comment_count INT DEFAULT 0;

-- Update via trigger or application code
CREATE FUNCTION update_comment_count() RETURNS TRIGGER AS $$
BEGIN
  IF TG_OP = 'INSERT' THEN
    UPDATE posts SET comment_count = comment_count + 1 WHERE id = NEW.post_id;
  ELSIF TG_OP = 'DELETE' THEN
    UPDATE posts SET comment_count = comment_count - 1 WHERE id = OLD.post_id;
  END IF;
  RETURN NULL;
END;
$$ LANGUAGE plpgsql;
```

## Indexing Strategy

### Index Types and When to Use

```
B-tree (default):  Equality, range, sorting, LIKE 'prefix%'
Hash:              Equality only (rarely better than B-tree)
GIN:               Full-text search, JSONB, arrays
GiST:              Geometry, range types, full-text
BRIN:              Large tables with naturally ordered data (timestamps)
```

### Composite Indexes

```sql
-- Column order matters: leftmost prefix rule
CREATE INDEX idx_users_status_created ON users (status, created_at);

-- This index supports:
--   WHERE status = 'active'                          -- YES
--   WHERE status = 'active' AND created_at > '2024'  -- YES
--   WHERE created_at > '2024'                        -- NO (skips first column)
```

### Partial and Covering Indexes

```sql
-- Partial index: only index rows matching condition
CREATE INDEX idx_orders_pending ON orders (created_at)
  WHERE status = 'pending';  -- smaller index, faster lookups

-- Covering index: include columns to avoid table lookup
CREATE INDEX idx_users_email_covering ON users (email)
  INCLUDE (name, avatar_url);  -- index-only scan for profile lookups
```

### Index Anti-patterns

```sql
-- WRONG: Index on low-cardinality column alone
CREATE INDEX idx_users_active ON users (is_active);  -- boolean = 2 values

-- WRONG: Too many indexes (slows writes)
-- Every INSERT/UPDATE must update ALL indexes

-- CORRECT: Composite index targeting actual queries
CREATE INDEX idx_users_active_created ON users (is_active, created_at DESC)
  WHERE is_active = true;
```

## Query Optimization

### Reading EXPLAIN Plans

```sql
EXPLAIN ANALYZE SELECT u.name, COUNT(o.id)
FROM users u
JOIN orders o ON o.user_id = u.id
WHERE u.status = 'active'
GROUP BY u.name;

-- Key things to look for:
-- Seq Scan         -> missing index (on large tables)
-- Nested Loop      -> fine for small sets, bad for large joins
-- Hash Join         -> good for large equi-joins
-- Sort             -> consider index to avoid sort
-- actual time      -> real execution time
-- rows             -> if estimated vs actual differ wildly, run ANALYZE
```

### N+1 Query Detection and Prevention

```python
# WRONG: N+1 queries (1 query for users + N queries for orders)
users = db.query(User).all()
for user in users:
    orders = db.query(Order).filter(Order.user_id == user.id).all()  # N queries!

# CORRECT: Eager loading with SQLAlchemy
users = db.query(User).options(joinedload(User.orders)).all()

# CORRECT: Batch query
user_ids = [u.id for u in users]
orders = db.query(Order).filter(Order.user_id.in_(user_ids)).all()
orders_by_user = defaultdict(list)
for order in orders:
    orders_by_user[order.user_id].append(order)
```

```javascript
// WRONG: N+1 with Prisma
const users = await prisma.user.findMany();
for (const user of users) {
  const orders = await prisma.order.findMany({ where: { userId: user.id } }); // N+1!
}

// CORRECT: Include relation
const users = await prisma.user.findMany({
  include: { orders: true },
});

// CORRECT: Batch with findMany + in
const userIds = users.map((u) => u.id);
const orders = await prisma.order.findMany({
  where: { userId: { in: userIds } },
});
```

### Pagination

```sql
-- WRONG: OFFSET pagination (rescans all skipped rows)
SELECT * FROM posts ORDER BY created_at DESC LIMIT 20 OFFSET 10000;

-- CORRECT: Cursor-based pagination (keyset)
SELECT * FROM posts
WHERE created_at < '2024-01-15T10:30:00Z'
ORDER BY created_at DESC
LIMIT 20;
```

## Migration Patterns

### Safe Migration Rules

```
1. Never rename a column in one step (add new, migrate data, drop old)
2. Never drop a column that's still read by running code
3. Add columns as nullable or with defaults
4. Create indexes CONCURRENTLY to avoid locking
5. Test rollback before deploying
```

### Zero-Downtime Migration Example

```sql
-- Step 1: Add new column (safe, no lock)
ALTER TABLE users ADD COLUMN display_name TEXT;

-- Step 2: Backfill data (do in batches)
UPDATE users SET display_name = name WHERE display_name IS NULL AND id BETWEEN 1 AND 10000;

-- Step 3: Deploy code that writes to BOTH columns
-- Step 4: Deploy code that reads from new column
-- Step 5: Drop old column (after confirming no reads)
ALTER TABLE users DROP COLUMN name;
```

### Index Creation

```sql
-- WRONG: Blocks writes on the table
CREATE INDEX idx_orders_user ON orders (user_id);

-- CORRECT: Non-blocking (PostgreSQL)
CREATE INDEX CONCURRENTLY idx_orders_user ON orders (user_id);
```

## Connection Pooling

```
Rule of thumb: connections = (CPU cores * 2) + disk spindles
For most apps: 10-20 connections per application instance
```

```python
# SQLAlchemy connection pool
engine = create_engine(
    DATABASE_URL,
    pool_size=10,          # maintained connections
    max_overflow=20,       # extra connections under load
    pool_timeout=30,       # seconds to wait for connection
    pool_recycle=1800,     # recycle connections every 30 min
    pool_pre_ping=True,    # verify connection before use
)
```

```javascript
// Prisma datasource
// In schema.prisma:
// datasource db {
//   provider = "postgresql"
//   url      = env("DATABASE_URL")
// }
// Connection limit via URL: ?connection_limit=10&pool_timeout=30
```

## ORM Best Practices

### Select Only What You Need

```python
# WRONG: Fetches all columns
users = db.query(User).all()

# CORRECT: Select specific columns
users = db.query(User.id, User.name).all()
```

```javascript
// WRONG: Fetches everything
const users = await prisma.user.findMany();

// CORRECT: Select specific fields
const users = await prisma.user.findMany({
  select: { id: true, name: true, email: true },
});
```

### Bulk Operations

```python
# WRONG: Individual inserts in a loop
for item in items:
    db.add(Item(**item))
    db.commit()  # commit per item!

# CORRECT: Bulk insert
db.bulk_insert_mappings(Item, items)
db.commit()
```

```javascript
// WRONG: Sequential creates
for (const item of items) {
  await prisma.item.create({ data: item });
}

// CORRECT: Batch create
await prisma.item.createMany({ data: items });

// CORRECT: Transaction for dependent operations
await prisma.$transaction([
  prisma.user.create({ data: userData }),
  prisma.profile.create({ data: profileData }),
]);
```

## NoSQL Design Patterns

### Document Database (MongoDB)

```javascript
// Design for access patterns, not normalization
// Embed when: 1:1, 1:few, data read together
// Reference when: 1:many, many:many, data grows unbounded

// WRONG: Normalizing in MongoDB like SQL
// users collection: { _id, name }
// addresses collection: { _id, userId, street }  // requires joins

// CORRECT: Embed bounded, co-accessed data
{
  _id: ObjectId("..."),
  name: "Alice",
  addresses: [
    { street: "123 Main St", city: "NYC", type: "home" },
    { street: "456 Work Ave", city: "NYC", type: "work" }
  ]
}

// CORRECT: Reference unbounded or independent data
// user: { _id, name, orderIds: [ObjectId("...")] }
// orders: { _id, userId, items: [...], total: 99.99 }
```

### Key-Value / Redis Patterns

```
# Cache-aside pattern
1. Check cache for key
2. If miss, query database
3. Store result in cache with TTL
4. Return result

# Cache invalidation
- TTL-based: SET key value EX 3600 (1 hour)
- Event-based: Delete key on write
- Write-through: Update cache on every write
```

## Common Anti-Patterns Summary

```
AVOID                              DO INSTEAD
-------------------------------------------------------------------
SELECT *                           SELECT specific columns
OFFSET pagination                  Cursor-based pagination
N+1 queries                        Eager load or batch queries
Indexing every column              Index based on query patterns
UUID v4 as primary key             UUID v7 or BIGSERIAL (better locality)
Storing money as FLOAT             Use DECIMAL / BIGINT (cents)
No foreign keys "for speed"        Use foreign keys (data integrity)
Giant migrations                   Small, reversible steps
No connection pooling              Always pool connections
Premature denormalization          Normalize first, denormalize with data
```
