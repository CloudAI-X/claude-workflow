---
name: web-design-guidelines
description: Review UI code for Web Interface Guidelines compliance. Use when asked to "review my UI", "check accessibility", "audit design", "review UX", "check my site against best practices", or "web interface guidelines".
---

# Web Interface Guidelines

### When to Load

- **Trigger**: UI audit, accessibility checks, responsive design review, UX best practices evaluation
- **Skip**: Backend-only work with no UI components

Self-contained guidelines for reviewing web interfaces. Apply these rules when auditing UI code.

## Output Format

Report findings as: `file:line — [RULE_ID] description`

Example: `src/Button.tsx:12 — [A11Y-01] Missing aria-label on icon button`

## 1. Accessibility (A11Y)

### A11Y-01: Semantic HTML

- Use `<button>` for actions, `<a>` for navigation, `<input>` for data entry
- Never use `<div onClick>` or `<span onClick>` for interactive elements
- Use `<nav>`, `<main>`, `<aside>`, `<header>`, `<footer>` for landmarks

### A11Y-02: ARIA Labels

- All interactive elements need accessible names
- Icon-only buttons MUST have `aria-label`
- Form inputs MUST have associated `<label>` or `aria-label`
- Images need `alt` text (decorative images: `alt=""`)

### A11Y-03: Keyboard Navigation

- All interactive elements must be reachable via Tab
- Custom components need proper `role`, `tabIndex`, and key handlers
- Focus must be visible (never `outline: none` without replacement)
- Modal/dialog must trap focus and return focus on close

### A11Y-04: Color & Contrast

- Text contrast ratio: 4.5:1 minimum (3:1 for large text)
- Never use color alone to convey meaning (add icons, text, patterns)
- Ensure UI is usable at 200% zoom

### A11Y-05: Screen Readers

- Dynamic content changes need `aria-live` regions
- Loading states need `aria-busy="true"`
- Error messages linked to inputs via `aria-describedby`

## 2. Performance (PERF)

### PERF-01: Image Optimization

- Use `next/image` or responsive images with `srcset`
- Specify `width` and `height` to prevent layout shift
- Lazy load below-fold images: `loading="lazy"`
- Use WebP/AVIF with fallback

### PERF-02: Bundle Size

- No full library imports: `import { Button } from 'lib'` not `import lib`
- Tree-shake CSS: use CSS modules or Tailwind purge
- Lazy load routes and heavy components: `React.lazy()` or dynamic imports

### PERF-03: Rendering

- Avoid layout thrashing: don't read then write DOM in loops
- Use `will-change` sparingly (only for known animations)
- Prefer CSS animations over JS animations
- Use `transform` and `opacity` for 60fps animations (compositor-only)

### PERF-04: Core Web Vitals

- **LCP** < 2.5s: Optimize largest image/text, preload critical resources
- **FID/INP** < 200ms: No long tasks on main thread, defer non-critical JS
- **CLS** < 0.1: Set dimensions on images/embeds, no injected content above fold

## 3. Responsive Design (RD)

### RD-01: Mobile First

- Base styles for mobile, then `@media (min-width)` for larger screens
- Touch targets minimum 44x44px
- No horizontal scroll on any viewport

### RD-02: Fluid Layout

- Use `rem`/`em` for typography, not `px`
- Use `clamp()` for fluid typography: `font-size: clamp(1rem, 2.5vw, 2rem)`
- Flex/Grid over fixed widths
- Max content width: `max-width: 65ch` for readability

### RD-03: Breakpoints

- Don't target devices, target content breakpoints
- Common: 640px (sm), 768px (md), 1024px (lg), 1280px (xl)
- Test at 320px, 375px, 768px, 1024px, 1440px, 1920px

## 4. Component Patterns (CP)

### CP-01: Forms

- Show validation errors inline, next to the field
- Use `type="email"`, `type="tel"`, `inputmode="numeric"` for mobile keyboards
- Disable submit button during submission (prevent double-submit)
- Preserve form state on error (don't clear fields)

### CP-02: Loading States

- Show skeleton screens over spinners for content areas
- Indicate progress for long operations (progress bar > spinner)
- Disable interactive elements during loading
- Set `aria-busy="true"` on loading containers

### CP-03: Error States

- Always show actionable error messages ("Try again" button, not just "Error")
- Don't show technical errors to users (log internally, show friendly message)
- Error boundaries for React component trees
- Retry logic for network failures

### CP-04: Empty States

- Never show blank pages — provide helpful empty states
- Include call-to-action: "No items yet. Create your first item."
- Use illustrations sparingly (they add bundle weight)

### CP-05: Modals & Dialogs

- Use `<dialog>` element or proper `role="dialog"`
- Trap focus within modal
- Close on Escape key and backdrop click
- Return focus to trigger element on close
- Prevent body scroll while open

## 5. CSS Practices (CSS)

### CSS-01: Specificity

- Prefer class selectors over ID or element selectors
- Avoid `!important` (use specificity or cascade layers)
- Use CSS custom properties for theming
- One direction for spacing: prefer `margin-bottom` over `margin-top`

### CSS-02: Layout

- Use Flexbox for 1D layout, Grid for 2D layout
- Avoid `position: absolute` for layout (use for overlays only)
- Use `gap` over margins between flex/grid children
- Use `min-height: 100dvh` (not `100vh`) for full-height layouts

### CSS-03: Dark Mode

- Use `prefers-color-scheme` media query
- Define all colors as CSS custom properties
- Test both modes — check contrast in both
- Don't just invert colors — design intentionally for dark mode

## 6. Security (SEC)

### SEC-01: Content Security

- Never use `dangerouslySetInnerHTML` without sanitization
- Sanitize user-generated content before rendering
- Use `rel="noopener noreferrer"` on external links with `target="_blank"`

### SEC-02: Forms & Input

- CSRF protection on all forms
- Rate limit form submissions
- Validate on both client AND server

## 7. Internationalization (I18N)

### I18N-01: Text

- Don't hardcode strings — use i18n library or constants
- Support RTL layouts: use `logical properties` (`margin-inline-start` over `margin-left`)
- Don't truncate text — designs must accommodate 40% text expansion
- Use `lang` attribute on `<html>` tag

## Review Checklist

When auditing a file, check in this order (CRITICAL first):

1. **CRITICAL**: A11Y-01, A11Y-02, SEC-01 — Semantic HTML, ARIA, XSS prevention
2. **HIGH**: PERF-04, A11Y-03, CP-01 — Core Web Vitals, keyboard, forms
3. **MEDIUM**: RD-01, CSS-02, CP-02, CP-03 — Responsive, layout, loading/errors
4. **LOW**: CSS-03, I18N-01, CP-04 — Dark mode, i18n, empty states
