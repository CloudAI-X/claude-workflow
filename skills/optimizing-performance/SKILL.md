---
name: optimizing-performance
description: Analyzes and optimizes application performance across frontend, backend, and database layers. Use when diagnosing slowness, improving load times, optimizing queries, reducing bundle size, or when asked about performance issues.
---

# Optimizing Performance

### When to Load

- **Trigger**: Diagnosing slowness, profiling, caching strategies, reducing load times, bundle size optimization
- **Skip**: Correctness-focused work where performance is not a concern

## Performance Optimization Workflow

Copy this checklist and track progress:

```
Performance Optimization Progress:
- [ ] Step 1: Measure baseline performance
- [ ] Step 2: Identify bottlenecks
- [ ] Step 3: Apply targeted optimizations
- [ ] Step 4: Measure again and compare
- [ ] Step 5: Repeat if targets not met
```

**Critical Rule**: Never optimize without data. Always profile before and after changes.

## Step 1: Measure Baseline

### Profiling Commands

```bash
# Node.js profiling
node --prof app.js
node --prof-process isolate*.log > profile.txt

# Python profiling
python -m cProfile -o profile.stats app.py
python -m pstats profile.stats

# Web performance
lighthouse https://example.com --output=json
```

## Step 2: Identify Bottlenecks

### Common Bottleneck Categories

| Category | Symptoms                         | Tools                           |
| -------- | -------------------------------- | ------------------------------- |
| CPU      | High CPU usage, slow computation | Profiler, flame graphs          |
| Memory   | High RAM, GC pauses, OOM         | Heap snapshots, memory profiler |
| I/O      | Slow disk/network, waiting       | strace, network inspector       |
| Database | Slow queries, lock contention    | Query analyzer, EXPLAIN         |

## Step 3: Apply Optimizations

### Frontend Optimizations

**Bundle Size:**

```javascript
// ❌ Import entire library
import _ from "lodash";

// ✅ Import only needed functions
import debounce from "lodash/debounce";

// ✅ Use dynamic imports for code splitting
const HeavyComponent = lazy(() => import("./HeavyComponent"));
```

**Rendering:**

```javascript
// ❌ Render on every parent update
function Child({ data }) {
  return <ExpensiveComponent data={data} />;
}

// ✅ Memoize when props don't change
const Child = memo(function Child({ data }) {
  return <ExpensiveComponent data={data} />;
});

// ✅ Use useMemo for expensive computations
const processed = useMemo(() => expensiveCalc(data), [data]);
```

**Images:**

```html
<!-- ❌ Unoptimized -->
<img src="large-image.jpg" />

<!-- ✅ Optimized -->
<img
  src="image.webp"
  srcset="image-300.webp 300w, image-600.webp 600w"
  sizes="(max-width: 600px) 300px, 600px"
  loading="lazy"
  decoding="async"
/>
```

### Backend Optimizations

**Database Queries:**

```sql
-- ❌ N+1 Query Problem
SELECT * FROM users;
-- Then for each user:
SELECT * FROM orders WHERE user_id = ?;

-- ✅ Single query with JOIN
SELECT u.*, o.*
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;

-- ✅ Or use pagination
SELECT * FROM users LIMIT 100 OFFSET 0;
```

**Caching Strategy:**

```javascript
// Multi-layer caching
const getUser = async (id) => {
  // L1: In-memory cache (fastest)
  let user = memoryCache.get(`user:${id}`);
  if (user) return user;

  // L2: Redis cache (fast)
  user = await redis.get(`user:${id}`);
  if (user) {
    memoryCache.set(`user:${id}`, user, 60);
    return JSON.parse(user);
  }

  // L3: Database (slow)
  user = await db.users.findById(id);
  await redis.setex(`user:${id}`, 3600, JSON.stringify(user));
  memoryCache.set(`user:${id}`, user, 60);

  return user;
};
```

**Async Processing:**

```javascript
// ❌ Blocking operation
app.post("/upload", async (req, res) => {
  await processVideo(req.file); // Takes 5 minutes
  res.send("Done");
});

// ✅ Queue for background processing
app.post("/upload", async (req, res) => {
  const jobId = await queue.add("processVideo", { file: req.file });
  res.send({ jobId, status: "processing" });
});
```

### Algorithm Optimizations

```javascript
// ❌ O(n²) - nested loops
function findDuplicates(arr) {
  const duplicates = [];
  for (let i = 0; i < arr.length; i++) {
    for (let j = i + 1; j < arr.length; j++) {
      if (arr[i] === arr[j]) duplicates.push(arr[i]);
    }
  }
  return duplicates;
}

// ✅ O(n) - hash map
function findDuplicates(arr) {
  const seen = new Set();
  const duplicates = new Set();
  for (const item of arr) {
    if (seen.has(item)) duplicates.add(item);
    seen.add(item);
  }
  return [...duplicates];
}
```

## Step 4: Measure Again

After applying optimizations, re-run profiling and compare:

```
Comparison Checklist:
- [ ] Run same profiling tools as baseline
- [ ] Compare metrics before vs after
- [ ] Verify no regressions in other areas
- [ ] Document improvement percentages
```

## Performance Targets

### Web Vitals

| Metric | Good    | Needs Work | Poor    |
| ------ | ------- | ---------- | ------- |
| LCP    | < 2.5s  | 2.5-4s     | > 4s    |
| FID    | < 100ms | 100-300ms  | > 300ms |
| CLS    | < 0.1   | 0.1-0.25   | > 0.25  |
| TTFB   | < 800ms | 800ms-1.8s | > 1.8s  |

### API Performance

| Metric      | Target  |
| ----------- | ------- |
| P50 Latency | < 100ms |
| P95 Latency | < 500ms |
| P99 Latency | < 1s    |
| Error Rate  | < 0.1%  |

## Validation

After optimization, validate results:

```
Performance Validation:
- [ ] Metrics improved from baseline
- [ ] No functionality regressions
- [ ] No new errors introduced
- [ ] Changes are sustainable (not one-time fixes)
- [ ] Performance gains documented
```

If targets not met, return to Step 2 and identify remaining bottlenecks.
