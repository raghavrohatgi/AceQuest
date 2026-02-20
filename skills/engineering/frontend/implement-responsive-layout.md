# Skill: implement-responsive-layout

## Purpose

Build a responsive layout for an AceQuest screen using Tailwind CSS mobile-first breakpoints. AceQuest is used primarily on mobile devices by students (often low-end Android phones), so mobile layout is always the primary concern — desktop is an enhancement.

Target device coverage:
- Mobile: 375px–639px (iPhone SE, budget Android)
- Tablet: 640px–1023px (iPad mini, mid-range tablets)
- Desktop: 1024px+ (school computer labs, teacher dashboards)

## Used By

Frontend Engineer Agent

## Inputs

| Input | Type | Description |
| --- | --- | --- |
| `screen_name` | string | Name of the screen/page (e.g. `GamePlay`, `StudentDashboard`) |
| `layout_description` | string | Natural language description of the layout and content areas |
| `breakpoints_needed` | list | Which breakpoints are relevant: `mobile`, `tablet`, `desktop` |
| `content_areas` | list | Named zones in the layout (e.g. `header`, `question`, `options`, `timer`) |

## Procedure / Template

### Step 1 — Design mobile layout first

Never start with desktop. Define the mobile layout as the base (no Tailwind prefix). Only then layer on `sm:`, `md:`, `lg:` overrides.

Mobile defaults for AceQuest screens:
- Full viewport width: `w-full`
- Single column: `flex flex-col` or `grid grid-cols-1`
- No horizontal padding on the outermost container (let child sections manage their own padding)
- Safe area insets on iOS: `pb-safe` (requires `tailwindcss-safe-area` plugin) or `pb-20` for fixed bottom nav

```typescript
// WRONG — starts from desktop thinking
<div className="grid grid-cols-3 gap-6 max-w-6xl mx-auto px-8">

// CORRECT — mobile-first
<div className="flex flex-col gap-4 px-4 md:grid md:grid-cols-2 md:gap-6 md:max-w-4xl md:mx-auto md:px-8">
```

### Step 2 — Apply AceQuest standard breakpoints

| Tailwind prefix | Min-width | Target devices |
| --- | --- | --- |
| (none) | 0px | All phones |
| `sm:` | 640px | Large phones, small tablets |
| `md:` | 768px | iPad, tablet landscape |
| `lg:` | 1024px | Laptops, desktop browsers |
| `xl:` | 1280px | Large monitors, teacher dashboards |

AceQuest standard layout container widths:
```
mobile:  full-bleed (no max-width)
sm:      full-bleed (still edge-to-edge)
md:      max-w-2xl  centered (48rem / 768px content area for game screens)
lg:      max-w-4xl  centered (56rem / 896px for content-heavy screens)
xl:      max-w-5xl  centered (64rem / 1024px for admin/teacher dashboards)
```

Reusable container component:
```typescript
// /src/components/layout/Container.tsx
import { cn } from '@/lib/utils';

interface ContainerProps {
  children: React.ReactNode;
  size?: 'game' | 'content' | 'dashboard';
  className?: string;
}

const sizeClasses = {
  game:      'max-w-2xl',   // game play screens
  content:   'max-w-4xl',   // content-heavy screens
  dashboard: 'max-w-5xl',   // teacher / parent dashboards
};

export function Container({ children, size = 'content', className }: ContainerProps): JSX.Element {
  return (
    <div className={cn('w-full mx-auto px-4 md:px-6 lg:px-8', sizeClasses[size], className)}>
      {children}
    </div>
  );
}
```

### Step 3 — Choose the right layout primitive

**CSS Grid** — for page-level layouts with named areas:
```typescript
// Two-column layout: sidebar + main on desktop, stacked on mobile
<div className="grid grid-cols-1 lg:grid-cols-[280px_1fr] gap-6">
  <aside>...</aside>
  <main>...</main>
</div>
```

**Flexbox** — for component-level layouts (row of buttons, card header, etc.):
```typescript
// Option row: stacked on mobile, horizontal on desktop
<div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
  <span>Score</span>
  <span>Timer</span>
</div>
```

**Do not mix** grid and flex at the same DOM level — choose one per element.

### Step 4 — Game Play screen layout pattern

AceQuest's most critical layout. The question area must be fully visible without scrolling on a 375px screen.

```typescript
// /src/app/game/[sessionId]/page.tsx (layout structure)
export default function GamePlayPage(): JSX.Element {
  return (
    // Full-screen viewport, no scroll on mobile
    <div className="min-h-screen bg-gradient-to-b from-purple-50 to-white flex flex-col">

      {/* Header: timer + score — fixed height */}
      <header className="flex-shrink-0 px-4 py-3 flex items-center justify-between
                         border-b border-gray-100 bg-white/80 backdrop-blur-sm
                         sticky top-0 z-10">
        <GameTimer />
        <ScoreBadge />
      </header>

      {/* Scrollable main area — takes remaining space */}
      <main className="flex-1 overflow-y-auto px-4 py-6
                       md:px-0 md:py-10">
        <Container size="game">
          {/* Question number + progress */}
          <div className="mb-4">
            <ProgressBar />
          </div>

          {/* Question card */}
          <QuestionCard className="mb-6" />

          {/* Options — 2-column grid on tablet+ for faster scanning */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <OptionButton />
            <OptionButton />
            <OptionButton />
            <OptionButton />
          </div>
        </Container>
      </main>

      {/* Fixed bottom CTA on mobile, inline on desktop */}
      <div className="flex-shrink-0 px-4 py-4 border-t border-gray-100 bg-white
                      md:hidden">
        <SubmitButton className="w-full" />
      </div>
    </div>
  );
}
```

### Step 5 — Enforce minimum touch targets

All interactive elements on mobile must be at minimum 44×44px (Apple HIG / WCAG 2.5.5).

```typescript
// Tailwind classes that guarantee 44px minimum
className="min-h-[44px] min-w-[44px]"
// OR use the Tailwind spacing scale equivalents:
className="min-h-11 min-w-11"   // 11 × 4 = 44px ✓

// For icon buttons, pad generously:
<button className="p-3 rounded-full hover:bg-gray-100 min-h-11 min-w-11
                   flex items-center justify-center">
  <ChevronRightIcon className="w-5 h-5" aria-hidden="true" />
</button>
```

Never reduce touch targets below 44px, even for visual compactness. Add negative margin if spacing is a concern rather than reducing the hit area.

### Step 6 — Test at canonical viewports

Test at these widths before marking complete:

| Width | Device it represents | What to check |
| --- | --- | --- |
| 375px | iPhone SE, budget Android | No horizontal scroll, touch targets hit, nothing clipped |
| 390px | iPhone 14 | Most common iOS screen |
| 768px | iPad portrait | Column transitions, card widths |
| 1024px | iPad landscape / small laptop | Grid transitions, sidebar visible |
| 1280px | Standard laptop | Full desktop layout, max-width applied |

Use browser DevTools responsive mode. Also test in landscape orientation at 375×667px (iPhone SE landscape).

### Step 7 — Verify no horizontal overflow

The most common mobile layout bug. Check with:
```css
/* Temporary debug helper — add to global.css while testing, remove before commit */
* {
  outline: 1px solid red !important;
}
```

Or use Tailwind's `overflow-x-hidden` on the root `<html>` element as a safety net:
```typescript
// app/layout.tsx
<html className="overflow-x-hidden">
```

Causes of horizontal overflow to check:
- Fixed-width elements wider than viewport (`w-[500px]` on mobile)
- Long unbroken strings (URLs, code blocks) — add `break-words` or `overflow-wrap: break-word`
- Negative margins without overflow clipping
- Transformed elements that extend outside the document flow

### Step 8 — Cumulative Layout Shift (CLS) prevention

CLS happens when elements load and push other content. For AceQuest:
- Always set explicit dimensions on images (`width` + `height` attributes or `aspect-ratio`)
- Reserve space for dynamic content (e.g. progress bar) with a fixed height
- Use `min-h-[...]` on skeleton loaders to match actual content height
- Avoid injecting content above existing content after load

Target: CLS < 0.1 (Core Web Vitals "Good" threshold)

## Output

A responsive layout component or page file with:
- Mobile-first Tailwind CSS classes
- Correct use of Grid (page level) and Flexbox (component level)
- Touch targets ≥ 44px on all interactive elements
- Explicit container max-widths at each breakpoint
- No horizontal overflow at any viewport width

## Quality Checks

Before marking this task complete, verify all of the following:

- [ ] No horizontal scroll at 375px viewport width
- [ ] All touch targets are at minimum `min-h-11 min-w-11` (44px)
- [ ] Text is readable without zooming at 375px (minimum 16px font for body)
- [ ] Layout uses Tailwind mobile-first (no prefix = mobile, `md:` and above = enhancements)
- [ ] Page-level grid, component-level flex — not mixed at the same DOM level
- [ ] Container has appropriate `max-w-*` at desktop breakpoints
- [ ] Images have explicit width/height or fixed aspect ratio
- [ ] CLS is 0 or near-zero (no layout shifts after initial render)
- [ ] Tested at 375px, 768px, and 1280px viewports in DevTools
- [ ] No magic pixel values (`w-[347px]`) — use spacing scale or named sizes

## Example

**Scenario:** Game Play screen layout — full-screen on mobile, centered card on tablet/desktop.

**Screen:** `/src/app/game/[sessionId]/page.tsx`

**Layout requirements:**
- Mobile (375px): Full viewport, sticky header with timer/score, scrollable question + options, fixed bottom submit button
- Tablet (768px): Centered in `max-w-2xl`, submit button moves inline below options (no fixed bottom bar)
- Desktop (1024px+): Same as tablet but wider question card, options become 2-column grid

**Key layout decisions:**
- `flex flex-col min-h-screen` on root — prevents content collapse on short viewports
- `sticky top-0` header — stays visible as student scrolls to read long questions
- `md:hidden` on fixed bottom button — disappears on tablet where inline submit is shown instead
- `grid grid-cols-1 sm:grid-cols-2` on options — 2-column on tablet+ reduces scroll distance
- Container `size="game"` (`max-w-2xl`) — narrow enough to read comfortably on tablet

See Step 4 for the full implementation of this layout.
