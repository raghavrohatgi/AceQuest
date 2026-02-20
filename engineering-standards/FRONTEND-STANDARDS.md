# AceQuest Frontend Coding Standards
## React/Next.js Best Practices

---

## Tech Stack

- **Framework:** Next.js 14+ (React 18+)
- **Language:** TypeScript (strict mode)
- **Styling:** Tailwind CSS
- **State Management:** React Query + Zustand
- **UI Components:** Radix UI + custom components
- **Forms:** React Hook Form + Zod validation
- **Testing:** Vitest + React Testing Library + Playwright

---

## Project Structure

```
/app                          # Next.js 14 App Router
  /(auth)                     # Route groups
    /login
    /signup
  /(dashboard)
    /student
    /parent
    /teacher
  /api                        # API routes
  layout.tsx                  # Root layout
  page.tsx                    # Home page

/components
  /ui                         # Base UI components (Button, Input, etc.)
  /features                   # Feature-specific components
    /assessment
    /gamification
    /dashboard
  /layouts                    # Layout components
  /forms                      # Form components

/lib
  /api                        # API client functions
  /hooks                      # Custom React hooks
  /utils                      # Utility functions
  /types                      # TypeScript types
  /constants                  # Constants and configs

/styles
  globals.css                 # Global styles + Tailwind

/public
  /images
  /icons
  /fonts
```

---

## TypeScript Standards

### Always Use TypeScript

```typescript
// ✅ GOOD - Explicit types
interface StudentProps {
  id: string;
  name: string;
  grade: number;
  onComplete: (score: number) => void;
}

export function StudentCard({ id, name, grade, onComplete }: StudentProps) {
  // Component logic
}

// ❌ BAD - Any type
export function StudentCard(props: any) {
  // Don't use 'any'
}
```

### Strict Type Checking

Enable in `tsconfig.json`:
```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true
  }
}
```

### Type Exports

```typescript
// ✅ GOOD - Export types separately
export type { StudentProps, AssessmentResult, QuestionType };
export { StudentCard };

// Define shared types in /lib/types
export interface Assessment {
  id: string;
  title: string;
  questions: Question[];
  timeLimit?: number;
}
```

---

## Component Standards

### Functional Components Only

```typescript
// ✅ GOOD - Functional component with TypeScript
interface ButtonProps {
  variant?: 'primary' | 'secondary';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
  onClick?: () => void;
}

export function Button({
  variant = 'primary',
  size = 'md',
  children,
  onClick
}: ButtonProps) {
  return (
    <button
      className={cn(baseStyles, variantStyles[variant], sizeStyles[size])}
      onClick={onClick}
    >
      {children}
    </button>
  );
}

// ❌ BAD - Class components
class Button extends React.Component { }
```

### Component Naming

- PascalCase for component files and exports
- Use descriptive names that indicate purpose
- Prefix containers with "Container" if needed

```typescript
// ✅ GOOD
StudentDashboard.tsx
AssessmentCard.tsx
QuestionList.tsx

// ❌ BAD
student.tsx
Card.tsx
List.tsx
```

### File Organization

One component per file (except for small, tightly related components):

```typescript
// StudentCard.tsx
export function StudentCard() { }
export function StudentCardSkeleton() { } // Related loading state OK
export function StudentCardError() { } // Related error state OK

// But split if components are substantial
// StudentCard.tsx
// StudentCardDetails.tsx
// StudentCardActions.tsx
```

---

## React Hooks Standards

### Custom Hooks

- Prefix with "use"
- Extract complex logic
- Return objects for multiple values

```typescript
// ✅ GOOD - Custom hook
export function useAssessment(assessmentId: string) {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState<Assessment | null>(null);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    fetchAssessment(assessmentId)
      .then(setData)
      .catch(setError)
      .finally(() => setLoading(false));
  }, [assessmentId]);

  return { data, loading, error };
}

// Usage
const { data: assessment, loading, error } = useAssessment(id);
```

### Hook Rules

1. Only call hooks at the top level
2. Only call hooks in React functions
3. Dependencies array must be complete

```typescript
// ✅ GOOD - Complete dependencies
useEffect(() => {
  if (userId) {
    fetchUserData(userId);
  }
}, [userId]); // userId is in dependencies

// ❌ BAD - Missing dependencies
useEffect(() => {
  fetchUserData(userId);
}, []); // userId should be in dependencies
```

---

## State Management

### Local State (useState)

Use for component-specific state:

```typescript
// ✅ GOOD - Local state
function QuestionForm() {
  const [answer, setAnswer] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Component logic
}
```

### Server State (React Query)

Use for API data:

```typescript
// ✅ GOOD - React Query for server state
import { useQuery, useMutation } from '@tanstack/react-query';

function StudentDashboard() {
  const { data: progress, isLoading } = useQuery({
    queryKey: ['student', 'progress', studentId],
    queryFn: () => fetchStudentProgress(studentId),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });

  const updateProgressMutation = useMutation({
    mutationFn: updateProgress,
    onSuccess: () => {
      queryClient.invalidateQueries(['student', 'progress']);
    },
  });

  return (
    // Component JSX
  );
}
```

### Global State (Zustand)

Use sparingly for true global state:

```typescript
// ✅ GOOD - Zustand for global UI state
import { create } from 'zustand';

interface UIStore {
  sidebarOpen: boolean;
  toggleSidebar: () => void;
}

export const useUIStore = create<UIStore>((set) => ({
  sidebarOpen: false,
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
}));
```

---

## Styling Standards

### Tailwind CSS

Use Tailwind utility classes:

```typescript
// ✅ GOOD - Tailwind utilities
<button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700
                   transition-colors disabled:opacity-50">
  Submit
</button>

// Use cn() helper for conditional classes
import { cn } from '@/lib/utils';

<div className={cn(
  'base-classes',
  isActive && 'active-classes',
  variant === 'primary' && 'primary-classes'
)}>
```

### Component Variants

Use cva (class-variance-authority) for complex variants:

```typescript
import { cva, type VariantProps } from 'class-variance-authority';

const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-md font-medium transition-colors',
  {
    variants: {
      variant: {
        primary: 'bg-blue-600 text-white hover:bg-blue-700',
        secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300',
        ghost: 'hover:bg-gray-100',
      },
      size: {
        sm: 'h-8 px-3 text-sm',
        md: 'h-10 px-4',
        lg: 'h-12 px-6 text-lg',
      },
    },
    defaultVariants: {
      variant: 'primary',
      size: 'md',
    },
  }
);

interface ButtonProps extends VariantProps<typeof buttonVariants> {
  children: React.ReactNode;
}

export function Button({ variant, size, children }: ButtonProps) {
  return <button className={buttonVariants({ variant, size })}>{children}</button>;
}
```

### No Inline Styles

```typescript
// ✅ GOOD - Tailwind classes
<div className="mt-4 text-lg font-bold" />

// ❌ BAD - Inline styles
<div style={{ marginTop: '16px', fontSize: '18px', fontWeight: 'bold' }} />
```

---

## Form Handling

### React Hook Form + Zod

```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

// ✅ GOOD - Schema-based validation
const loginSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});

type LoginFormData = z.infer<typeof loginSchema>;

export function LoginForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = async (data: LoginFormData) => {
    await loginUser(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('email')} />
      {errors.email && <span>{errors.email.message}</span>}

      <input type="password" {...register('password')} />
      {errors.password && <span>{errors.password.message}</span>}

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Logging in...' : 'Login'}
      </button>
    </form>
  );
}
```

---

## Error Handling

### Error Boundaries

```typescript
// ✅ GOOD - Error boundary for graceful failures
'use client'; // Required for error boundaries in Next.js 14

export function ErrorBoundary({ error, reset }: {
  error: Error;
  reset: () => void;
}) {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h2>Something went wrong!</h2>
      <p>{error.message}</p>
      <button onClick={reset}>Try again</button>
    </div>
  );
}
```

### API Error Handling

```typescript
// ✅ GOOD - Structured error handling
async function fetchAssessment(id: string): Promise<Assessment> {
  try {
    const response = await fetch(`/api/assessments/${id}`);

    if (!response.ok) {
      throw new APIError(
        `Failed to fetch assessment: ${response.statusText}`,
        response.status
      );
    }

    return response.json();
  } catch (error) {
    if (error instanceof APIError) {
      throw error;
    }
    throw new APIError('Network error occurred', 500);
  }
}
```

---

## Performance Optimization

### Code Splitting

```typescript
// ✅ GOOD - Dynamic imports for large components
import dynamic from 'next/dynamic';

const AssessmentEditor = dynamic(
  () => import('@/components/features/assessment/AssessmentEditor'),
  {
    loading: () => <AssessmentEditorSkeleton />,
    ssr: false // Client-side only if needed
  }
);
```

### Memoization

```typescript
import { memo, useMemo, useCallback } from 'react';

// ✅ GOOD - Memoize expensive computations
function StudentDashboard({ studentId }: { studentId: string }) {
  const stats = useMemo(() =>
    calculateComplexStats(studentData),
    [studentData]
  );

  const handleSubmit = useCallback(() => {
    submitAssessment(studentId);
  }, [studentId]);

  return (
    // JSX
  );
}

// ✅ GOOD - Memo for pure components
export const StudentCard = memo(function StudentCard({ student }: Props) {
  return (
    // JSX
  );
});
```

### Image Optimization

```typescript
// ✅ GOOD - Next.js Image component
import Image from 'next/image';

<Image
  src="/images/badge.png"
  alt="Achievement badge"
  width={100}
  height={100}
  priority={false} // Use priority for above-fold images
  placeholder="blur" // Optional blur placeholder
/>
```

---

## Accessibility (A11y)

### WCAG 2.1 AA Compliance

```typescript
// ✅ GOOD - Accessible button
<button
  type="button"
  aria-label="Submit assessment"
  aria-describedby="submit-help"
  disabled={isSubmitting}
  className="..."
>
  Submit
</button>
<p id="submit-help" className="sr-only">
  Submits your answers and calculates your score
</p>

// ✅ GOOD - Accessible form
<form>
  <label htmlFor="student-name" className="block mb-2">
    Student Name
  </label>
  <input
    id="student-name"
    type="text"
    aria-required="true"
    aria-invalid={!!errors.name}
    aria-describedby="name-error"
  />
  {errors.name && (
    <span id="name-error" role="alert" className="text-red-600">
      {errors.name.message}
    </span>
  )}
</form>
```

### Keyboard Navigation

```typescript
// ✅ GOOD - Keyboard support
function Modal({ isOpen, onClose }: ModalProps) {
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
      return () => document.removeEventListener('keydown', handleEscape);
    }
  }, [isOpen, onClose]);

  return (
    // Modal JSX with focus trap
  );
}
```

---

## Testing Standards

### Unit Tests (Vitest)

```typescript
// StudentCard.test.tsx
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { StudentCard } from './StudentCard';

describe('StudentCard', () => {
  it('renders student name', () => {
    render(<StudentCard name="Alice" grade={5} />);
    expect(screen.getByText('Alice')).toBeInTheDocument();
  });

  it('displays grade level', () => {
    render(<StudentCard name="Alice" grade={5} />);
    expect(screen.getByText(/Grade 5/i)).toBeInTheDocument();
  });
});
```

### Integration Tests (React Testing Library)

```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

describe('LoginForm', () => {
  it('submits form with valid data', async () => {
    const onSubmit = vi.fn();
    render(<LoginForm onSubmit={onSubmit} />);

    await userEvent.type(screen.getByLabelText(/email/i), 'test@example.com');
    await userEvent.type(screen.getByLabelText(/password/i), 'password123');

    fireEvent.click(screen.getByRole('button', { name: /login/i }));

    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'password123',
      });
    });
  });
});
```

---

## Code Quality

### ESLint Configuration

```json
{
  "extends": [
    "next/core-web-vitals",
    "plugin:@typescript-eslint/recommended",
    "prettier"
  ],
  "rules": {
    "react/jsx-no-target-blank": "error",
    "react-hooks/rules-of-hooks": "error",
    "react-hooks/exhaustive-deps": "warn",
    "@typescript-eslint/no-unused-vars": "error",
    "@typescript-eslint/no-explicit-any": "error"
  }
}
```

### Prettier Configuration

```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false
}
```

---

## Documentation

### Component Documentation

```typescript
/**
 * StudentCard displays a student's basic information and progress
 *
 * @param props - Component props
 * @param props.student - Student object containing name, grade, and id
 * @param props.onSelect - Callback when card is clicked
 * @param props.showProgress - Whether to display progress bar (default: true)
 *
 * @example
 * ```tsx
 * <StudentCard
 *   student={{ id: '1', name: 'Alice', grade: 5 }}
 *   onSelect={(id) => navigate(`/student/${id}`)}
 *   showProgress={true}
 * />
 * ```
 */
export function StudentCard({ student, onSelect, showProgress = true }: Props) {
  // Implementation
}
```

---

## Common Patterns

### Loading States

```typescript
// ✅ GOOD - Skeleton loading
function StudentDashboard() {
  const { data, isLoading } = useQuery(['student']);

  if (isLoading) {
    return <StudentDashboardSkeleton />;
  }

  return <div>{/* Actual content */}</div>;
}
```

### Empty States

```typescript
// ✅ GOOD - Meaningful empty state
function AssessmentList({ assessments }: Props) {
  if (assessments.length === 0) {
    return (
      <EmptyState
        icon={<BookIcon />}
        title="No assessments yet"
        description="Start your first assessment to begin your learning quest!"
        action={
          <Button onClick={() => navigate('/assessments/new')}>
            Start First Assessment
          </Button>
        }
      />
    );
  }

  return (
    // List rendering
  );
}
```

---

## Key Takeaways

1. ✅ Always use TypeScript with strict mode
2. ✅ Functional components only
3. ✅ Use React Query for server state
4. ✅ Tailwind for all styling
5. ✅ Accessibility is mandatory (WCAG 2.1 AA)
6. ✅ Test all components
7. ✅ Optimize for performance (code splitting, memoization)
8. ✅ Document complex components
9. ✅ Handle errors gracefully
10. ✅ Follow consistent file structure

---

**When in doubt, prioritize: Accessibility > Performance > Developer Experience**
