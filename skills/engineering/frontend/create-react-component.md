# Skill: create-react-component

## Purpose

Full lifecycle for building a new React component in the AceQuest frontend — TypeScript props interface, implementation with Tailwind CSS and CVA variants, ARIA accessibility attributes, loading/error/empty state handling, barrel export, Vitest + React Testing Library unit tests, and a Storybook story with all variants.

This skill ensures every component is production-ready from day one: typed, accessible, tested, and documented in Storybook so the team can visually verify all states without running the full app.

## Used By

Frontend Engineer Agent

## Inputs

| Input | Type | Description |
| --- | --- | --- |
| `component_name` | string | PascalCase name (e.g. `QuestionCard`, `ScoreBoard`) |
| `props` | list | Each prop: `{ name, type, required, description, default? }` |
| `behaviour_description` | string | What the component does, how it responds to interaction |
| `design_spec_reference` | string | Figma URL or design spec section name |
| `category` | string | Subfolder: `ui`, `game`, `layout`, `forms`, `feedback` |

## Procedure / Template

### Step 1 — Define the TypeScript props interface

Create a dedicated props interface with JSDoc on every prop. Place at the top of the component file.

```typescript
/**
 * Props for the QuestionCard component.
 * Displays a single game question with selectable answer options.
 */
export interface QuestionCardProps {
  /** The question text to display */
  question: string;
  /** Array of answer options — exactly 4 for MCQ */
  options: string[];
  /** Index of the currently selected option, or null if nothing selected */
  selectedOption: number | null;
  /** Called when the user selects an option */
  onSelect: (index: number) => void;
  /** Visual state after answer submission */
  state?: 'idle' | 'correct' | 'incorrect' | 'revealed';
  /** Index of the correct answer — required when state is 'revealed' or 'correct'/'incorrect' */
  correctIndex?: number;
  /** Whether the card is in a loading state */
  isLoading?: boolean;
  /** Optional CSS class overrides */
  className?: string;
}
```

Rules:
- No `any`. No `object`. No untyped `React.FC` — use explicit return type `: JSX.Element`.
- Optional props must have `?` and a sensible default in destructuring.
- Union types for finite states (e.g. `'idle' | 'correct' | 'incorrect'`), never raw strings.

### Step 2 — Create the component file

File path: `/src/components/[category]/ComponentName.tsx`

Example: `/src/components/game/QuestionCard.tsx`

Directory structure:
```
src/components/game/
  QuestionCard.tsx
  QuestionCard.test.tsx
  QuestionCard.stories.tsx
```

### Step 3 — Implement with React + Tailwind CSS using CVA

Use `cva` (class-variance-authority) for any component with visual variants. This keeps className logic readable and type-safe.

```typescript
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils'; // Tailwind merge utility

const optionVariants = cva(
  // Base classes applied to all options
  [
    'flex items-center gap-3 w-full px-4 py-3 rounded-lg border-2 text-left',
    'transition-colors duration-150 cursor-pointer',
    'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-purple-500 focus-visible:ring-offset-2',
    'disabled:cursor-not-allowed disabled:opacity-50',
  ],
  {
    variants: {
      state: {
        idle:      'border-gray-200 bg-white hover:border-purple-400 hover:bg-purple-50',
        selected:  'border-purple-500 bg-purple-50',
        correct:   'border-green-500 bg-green-50 text-green-800',
        incorrect: 'border-red-500 bg-red-50 text-red-800',
        revealed:  'border-gray-200 bg-gray-50',
      },
    },
    defaultVariants: {
      state: 'idle',
    },
  }
);

type OptionVariants = VariantProps<typeof optionVariants>;
```

Full component implementation:

```typescript
import React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';
import { Skeleton } from '@/components/ui/Skeleton';

const optionVariants = cva(
  [
    'flex items-center gap-3 w-full px-4 py-3 rounded-lg border-2 text-left',
    'transition-colors duration-150',
    'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-purple-500 focus-visible:ring-offset-2',
    'disabled:cursor-not-allowed disabled:opacity-50',
  ],
  {
    variants: {
      state: {
        idle:      'border-gray-200 bg-white hover:border-purple-400 hover:bg-purple-50 cursor-pointer',
        selected:  'border-purple-500 bg-purple-50 cursor-pointer',
        correct:   'border-green-500 bg-green-50 text-green-800',
        incorrect: 'border-red-500 bg-red-50 text-red-800',
        revealed:  'border-green-500 bg-green-50',
      },
    },
    defaultVariants: { state: 'idle' },
  }
);

const OPTION_LABELS = ['A', 'B', 'C', 'D'] as const;

export interface QuestionCardProps {
  /** The question text to display */
  question: string;
  /** Array of answer options — exactly 4 for MCQ */
  options: string[];
  /** Index of the currently selected option, or null if nothing selected */
  selectedOption: number | null;
  /** Called when the user selects an option */
  onSelect: (index: number) => void;
  /** Visual state after answer submission */
  state?: 'idle' | 'correct' | 'incorrect' | 'revealed';
  /** Index of the correct answer — required when state is 'revealed' */
  correctIndex?: number;
  /** Whether the card is loading question data */
  isLoading?: boolean;
  /** Optional CSS class overrides */
  className?: string;
}

export function QuestionCard({
  question,
  options,
  selectedOption,
  onSelect,
  state = 'idle',
  correctIndex,
  isLoading = false,
  className,
}: QuestionCardProps): JSX.Element {
  const isAnswered = state !== 'idle';

  function getOptionState(index: number): VariantProps<typeof optionVariants>['state'] {
    if (state === 'correct' || state === 'incorrect') {
      if (index === selectedOption) return state;
      if (state === 'incorrect' && index === correctIndex) return 'revealed';
    }
    if (state === 'revealed' && index === correctIndex) return 'revealed';
    if (index === selectedOption) return 'selected';
    return 'idle';
  }

  if (isLoading) {
    return (
      <div
        className={cn('rounded-2xl bg-white shadow-md p-6 space-y-4', className)}
        aria-busy="true"
        aria-label="Loading question"
      >
        <Skeleton className="h-6 w-3/4" />
        <div className="space-y-3 mt-4">
          {Array.from({ length: 4 }).map((_, i) => (
            <Skeleton key={i} className="h-12 w-full rounded-lg" />
          ))}
        </div>
      </div>
    );
  }

  if (!question || options.length === 0) {
    return (
      <div
        className={cn('rounded-2xl bg-white shadow-md p-6 text-center text-gray-500', className)}
        role="status"
      >
        No question available.
      </div>
    );
  }

  return (
    <div
      className={cn('rounded-2xl bg-white shadow-md p-6 space-y-4', className)}
      role="group"
      aria-labelledby="question-text"
    >
      <p
        id="question-text"
        className="text-lg font-semibold text-gray-900 leading-snug"
      >
        {question}
      </p>

      <div
        role="radiogroup"
        aria-labelledby="question-text"
        aria-required="true"
        className="space-y-3"
      >
        {options.map((option, index) => {
          const optionState = getOptionState(index);
          const isSelected = index === selectedOption;
          const label = OPTION_LABELS[index];

          return (
            <button
              key={index}
              role="radio"
              aria-checked={isSelected}
              aria-label={`Option ${label}: ${option}`}
              disabled={isAnswered}
              onClick={() => !isAnswered && onSelect(index)}
              className={optionVariants({ state: optionState })}
            >
              <span
                className="flex-shrink-0 w-7 h-7 rounded-full border-2 border-current
                           flex items-center justify-center text-sm font-bold"
                aria-hidden="true"
              >
                {label}
              </span>
              <span className="flex-1 text-sm font-medium">{option}</span>
            </button>
          );
        })}
      </div>

      {state !== 'idle' && (
        <div
          aria-live="polite"
          aria-atomic="true"
          className={cn(
            'text-sm font-medium mt-2',
            state === 'correct' ? 'text-green-700' : 'text-red-700'
          )}
        >
          {state === 'correct' && 'Correct! Well done.'}
          {state === 'incorrect' && 'Not quite. The correct answer is highlighted above.'}
          {state === 'revealed' && 'Time up! The correct answer is highlighted.'}
        </div>
      )}
    </div>
  );
}
```

### Step 4 — Add ARIA attributes

Rules:
- Use semantic HTML first. `<button>` not `<div onClick>`.
- `role="radiogroup"` + `role="radio"` + `aria-checked` for MCQ option groups.
- `aria-live="polite"` for feedback text injected after answer submission.
- `aria-busy="true"` on loading container.
- `aria-label` on icon-only buttons.
- `aria-describedby` to link error messages to form inputs.
- Do not add `role="button"` to actual `<button>` elements — it is redundant.

### Step 5 — Handle loading, error, and empty states

Every component must handle three additional states:

| State | Trigger | Render |
| --- | --- | --- |
| Loading | `isLoading={true}` | Skeleton placeholders matching the shape of loaded content |
| Error | `error` prop or error boundary | Friendly error message + retry action if applicable |
| Empty | No data (empty array, null) | Descriptive empty state message, not a blank screen |

### Step 6 — Export from barrel file

Add the export to the category barrel file:

```typescript
// /src/components/game/index.ts
export { QuestionCard } from './QuestionCard';
export type { QuestionCardProps } from './QuestionCard';
```

Then re-export from the top-level components barrel if needed:
```typescript
// /src/components/index.ts
export * from './game';
```

### Step 7 — Write Vitest + RTL unit tests

File: `/src/components/game/QuestionCard.test.tsx`

```typescript
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
import { QuestionCard } from './QuestionCard';

expect.extend(toHaveNoViolations);

const defaultProps = {
  question: 'What is the SI unit of force?',
  options: ['Joule', 'Newton', 'Pascal', 'Watt'],
  selectedOption: null,
  onSelect: vi.fn(),
};

describe('QuestionCard', () => {
  // Render
  it('renders the question text', () => {
    render(<QuestionCard {...defaultProps} />);
    expect(screen.getByText('What is the SI unit of force?')).toBeInTheDocument();
  });

  it('renders all 4 options', () => {
    render(<QuestionCard {...defaultProps} />);
    expect(screen.getAllByRole('radio')).toHaveLength(4);
  });

  // Interaction
  it('calls onSelect with the correct index when an option is clicked', () => {
    const onSelect = vi.fn();
    render(<QuestionCard {...defaultProps} onSelect={onSelect} />);
    fireEvent.click(screen.getByRole('radio', { name: /Option B: Newton/i }));
    expect(onSelect).toHaveBeenCalledWith(1);
  });

  it('does not call onSelect when already answered', () => {
    const onSelect = vi.fn();
    render(
      <QuestionCard {...defaultProps} onSelect={onSelect} state="correct" selectedOption={1} />
    );
    fireEvent.click(screen.getByRole('radio', { name: /Option A/i }));
    expect(onSelect).not.toHaveBeenCalled();
  });

  it('shows selected state on the chosen option', () => {
    render(<QuestionCard {...defaultProps} selectedOption={1} />);
    expect(screen.getByRole('radio', { name: /Option B: Newton/i }))
      .toHaveAttribute('aria-checked', 'true');
  });

  // States
  it('renders skeleton when isLoading is true', () => {
    render(<QuestionCard {...defaultProps} isLoading />);
    expect(screen.getByLabelText('Loading question')).toBeInTheDocument();
    expect(screen.queryByRole('radio')).not.toBeInTheDocument();
  });

  it('renders empty state message when no question provided', () => {
    render(<QuestionCard {...defaultProps} question="" options={[]} />);
    expect(screen.getByText('No question available.')).toBeInTheDocument();
  });

  it('shows correct feedback after correct answer', () => {
    render(
      <QuestionCard {...defaultProps} state="correct" selectedOption={1} correctIndex={1} />
    );
    expect(screen.getByText('Correct! Well done.')).toBeInTheDocument();
  });

  it('shows incorrect feedback and highlights correct answer', () => {
    render(
      <QuestionCard {...defaultProps} state="incorrect" selectedOption={0} correctIndex={1} />
    );
    expect(screen.getByText(/Not quite/i)).toBeInTheDocument();
  });

  // Accessibility
  it('has no axe violations in idle state', async () => {
    const { container } = render(<QuestionCard {...defaultProps} />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('has no axe violations in answered state', async () => {
    const { container } = render(
      <QuestionCard {...defaultProps} state="correct" selectedOption={1} correctIndex={1} />
    );
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
```

### Step 8 — Write Storybook story

File: `/src/components/game/QuestionCard.stories.tsx`

```typescript
import type { Meta, StoryObj } from '@storybook/react';
import { fn } from '@storybook/test';
import { QuestionCard } from './QuestionCard';

const meta: Meta<typeof QuestionCard> = {
  title: 'Game/QuestionCard',
  component: QuestionCard,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component:
          'Displays a single MCQ question with options. Handles idle, selected, correct, incorrect, and revealed states.',
      },
    },
  },
  tags: ['autodocs'],
  argTypes: {
    state: {
      control: 'select',
      options: ['idle', 'correct', 'incorrect', 'revealed'],
    },
    selectedOption: { control: { type: 'number', min: 0, max: 3 } },
    correctIndex: { control: { type: 'number', min: 0, max: 3 } },
  },
  args: {
    onSelect: fn(),
    question: 'What is the SI unit of force?',
    options: ['Joule', 'Newton', 'Pascal', 'Watt'],
    selectedOption: null,
    state: 'idle',
  },
};

export default meta;
type Story = StoryObj<typeof QuestionCard>;

export const Default: Story = {};

export const OptionSelected: Story = {
  args: { selectedOption: 1 },
};

export const CorrectAnswer: Story = {
  args: { state: 'correct', selectedOption: 1, correctIndex: 1 },
};

export const IncorrectAnswer: Story = {
  args: { state: 'incorrect', selectedOption: 0, correctIndex: 1 },
};

export const TimeRevealed: Story = {
  args: { state: 'revealed', selectedOption: null, correctIndex: 1 },
};

export const Loading: Story = {
  args: { isLoading: true },
};

export const Empty: Story = {
  args: { question: '', options: [] },
};

export const LongQuestion: Story = {
  args: {
    question:
      'Arjun cycles from his house to school every day. If his school is 4.5 km away and he cycles at 12 km/h, how many minutes does it take him to reach school?',
    options: ['20.5 minutes', '22.5 minutes', '25 minutes', '18 minutes'],
  },
};
```

## Output

| File | Description |
| --- | --- |
| `/src/components/[category]/ComponentName.tsx` | Component implementation with TypeScript props, CVA variants, ARIA, and all states |
| `/src/components/[category]/ComponentName.test.tsx` | Vitest + RTL tests covering render, interaction, states, and accessibility |
| `/src/components/[category]/ComponentName.stories.tsx` | Storybook story with all variant stories and autodocs |
| `/src/components/[category]/index.ts` | Updated barrel export |

## Quality Checks

Before marking this task complete, verify all of the following:

- [ ] No `any` types anywhere in the component or props interface
- [ ] Every prop has a JSDoc comment in the interface
- [ ] Component handles `isLoading`, error/empty, and all content states
- [ ] All interactive elements are `<button>` or `<a>`, never `<div onClick>`
- [ ] `aria-live="polite"` is used for dynamic content injected after interaction
- [ ] Icon-only buttons have `aria-label`
- [ ] `focus-visible:ring-2 ring-purple-500` (or equivalent) is applied — never `outline-none` without custom focus
- [ ] CVA is used for any component with 2+ visual variants
- [ ] Barrel export is updated
- [ ] Test file covers: renders correctly, all user interactions, all prop-driven states, at least one `axe` accessibility check
- [ ] Storybook story has a story for every visual state
- [ ] Run `pnpm type-check` — 0 TypeScript errors
- [ ] Run `pnpm test ComponentName` — all tests pass

## Example

**Scenario:** Create a `QuestionCard` component for the game play screen.

**Inputs:**
- `component_name`: `QuestionCard`
- `category`: `game`
- `props`: question (string), options (string[]), selectedOption (number | null), onSelect (function), state ('idle'|'correct'|'incorrect'|'revealed'), correctIndex (number, optional), isLoading (boolean, optional)
- `behaviour_description`: Displays a question and four answer options as radio-group buttons. Clicking an option calls `onSelect`. Once `state` changes from `idle`, options are disabled. Correct/incorrect options are highlighted using colour + icon cues, not colour alone (to support colour-blind users).
- `design_spec_reference`: Figma > Game Flow > Question Card (all states)

**Files produced:**
- `/src/components/game/QuestionCard.tsx` — see Step 3 above for full implementation
- `/src/components/game/QuestionCard.test.tsx` — see Step 7 above
- `/src/components/game/QuestionCard.stories.tsx` — see Step 8 above
