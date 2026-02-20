# Skill: Add Form with Validation

## Purpose
Define how to build accessible, validated forms in AceQuest's Next.js 14 frontend using React Hook Form and Zod. All forms must display inline errors, support keyboard navigation, use AceQuest's design-system components, and provide optimistic feedback suitable for K-8 students (clear, encouraging error messages in simple English/Hindi).

## Used By
- Frontend Engineer Agent
- Full-Stack Engineer Agent
- UI/UX Agent

## Inputs
| Field | Type | Description |
| --- | --- | --- |
| `formName` | string | Descriptive name, e.g. `LoginForm`, `QuizAnswerForm` |
| `fields` | object[] | Form fields with name, label, type, and validation rules |
| `submitAction` | string | Server Action or API endpoint that handles submission |
| `successRoute` | string | Next.js route to navigate to on success |
| `ageGroup` | `"5-7" \ | "8-10" \ | "11-13"` | Affects error message complexity and label style |

## Procedure / Template

### Step 1 — Define the Zod Schema (shared with backend)

```typescript
// src/lib/schemas/auth.schema.ts
import { z } from "zod";

export const LoginSchema = z.object({
  email: z
    .string()
    .min(1, "Please enter your email address")
    .email("That doesn't look like an email — check for a '@' symbol"),
  password: z
    .string()
    .min(8, "Password must be at least 8 characters")
    .max(128, "Password is too long"),
});

export type LoginFormValues = z.infer<typeof LoginSchema>;
```

### Step 2 — Create the Form Component

```tsx
// src/components/forms/LoginForm.tsx
"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { LoginSchema, LoginFormValues } from "@/lib/schemas/auth.schema";
import { TextInput } from "@/components/ui/TextInput";
import { Button } from "@/components/ui/Button";
import { FormError } from "@/components/ui/FormError";
import { login } from "@/lib/actions/auth.actions";

export function LoginForm() {
  const router = useRouter();
  const [serverError, setServerError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginFormValues>({
    resolver: zodResolver(LoginSchema),
    mode: "onBlur",   // validate on blur, not on every keystroke
  });

  const onSubmit = async (data: LoginFormValues) => {
    setServerError(null);
    try {
      await login(data);
      router.push("/dashboard");
    } catch (err: any) {
      setServerError(err.message ?? "Something went wrong. Please try again.");
    }
  };

  return (
    <form
      onSubmit={handleSubmit(onSubmit)}
      noValidate
      aria-label="Log in to AceQuest"
      className="flex flex-col gap-6 w-full max-w-sm"
    >
      <h1 className="text-2xl font-bold text-quest-navy">Welcome back!</h1>

      {serverError && (
        <FormError role="alert" aria-live="assertive">
          {serverError}
        </FormError>
      )}

      <TextInput
        id="email"
        label="Email address"
        type="email"
        autoComplete="email"
        error={errors.email?.message}
        {...register("email")}
      />

      <TextInput
        id="password"
        label="Password"
        type="password"
        autoComplete="current-password"
        error={errors.password?.message}
        {...register("password")}
      />

      <Button type="submit" loading={isSubmitting} disabled={isSubmitting}>
        {isSubmitting ? "Logging in…" : "Log in"}
      </Button>
    </form>
  );
}
```

### Step 3 — Reusable TextInput Component

```tsx
// src/components/ui/TextInput.tsx
import { forwardRef, InputHTMLAttributes } from "react";
import { cn } from "@/lib/utils";

interface TextInputProps extends InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: string;
  hint?: string;
}

export const TextInput = forwardRef<HTMLInputElement, TextInputProps>(
  ({ id, label, error, hint, className, ...props }, ref) => {
    const errorId = error ? `${id}-error` : undefined;
    const hintId = hint ? `${id}-hint` : undefined;

    return (
      <div className="flex flex-col gap-1">
        <label htmlFor={id} className="text-sm font-medium text-quest-navy">
          {label}
        </label>

        {hint && (
          <p id={hintId} className="text-xs text-gray-500">
            {hint}
          </p>
        )}

        <input
          ref={ref}
          id={id}
          aria-describedby={[hintId, errorId].filter(Boolean).join(" ") || undefined}
          aria-invalid={!!error}
          className={cn(
            "rounded-lg border px-3 py-2 text-sm transition-colors",
            "focus:outline-none focus:ring-2 focus:ring-quest-purple focus:border-transparent",
            error
              ? "border-red-500 bg-red-50 focus:ring-red-500"
              : "border-gray-300 bg-white hover:border-quest-purple",
            className
          )}
          {...props}
        />

        {error && (
          <p
            id={errorId}
            role="alert"
            aria-live="polite"
            className="text-xs text-red-600 flex items-center gap-1"
          >
            <span aria-hidden>⚠️</span> {error}
          </p>
        )}
      </div>
    );
  }
);
TextInput.displayName = "TextInput";
```

### Step 4 — Server Action

```typescript
// src/lib/actions/auth.actions.ts
"use server";

import { LoginSchema } from "@/lib/schemas/auth.schema";

export async function login(formData: unknown) {
  const parsed = LoginSchema.safeParse(formData);
  if (!parsed.success) {
    throw new Error(parsed.error.errors[0].message);
  }

  const res = await fetch(`${process.env.API_BASE_URL}/api/v1/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(parsed.data),
  });

  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.meta?.message ?? "Login failed");
  }

  const { data } = await res.json();
  // Store accessToken in secure cookie via Set-Cookie header
  return data;
}
```

### Step 5 — Student-Facing Error Messages by Age Group

```typescript
// src/lib/validationMessages.ts
export const ageGroupMessages = {
  "5-7": {
    required: "Oops! We need this.",
    email: "That doesn't look like an email! Look for the '@' sign.",
    minLength: (n: number) => `Make it longer — at least ${n} letters!`,
  },
  "8-10": {
    required: "This field is required.",
    email: "Please enter a valid email address.",
    minLength: (n: number) => `Must be at least ${n} characters.`,
  },
  "11-13": {
    required: "Required.",
    email: "Invalid email format.",
    minLength: (n: number) => `Minimum ${n} characters.`,
  },
};
```

## Output
- `src/lib/schemas/<domain>.schema.ts` — Zod schema shared with backend
- `src/components/forms/<FormName>.tsx` — form component
- `src/components/ui/TextInput.tsx` — reusable input with accessibility
- `src/lib/actions/<domain>.actions.ts` — Next.js Server Action

## Quality Checks
- [ ] `noValidate` on `<form>` prevents browser-native validation competing with Zod
- [ ] `aria-invalid` set on inputs with errors
- [ ] Error messages linked via `aria-describedby` referencing the error element's `id`
- [ ] Error element has `role="alert"` and `aria-live="polite"` for screen readers
- [ ] Submit button is disabled and shows loading state during async submission
- [ ] Server errors are displayed distinctly from field errors
- [ ] Form uses `autoComplete` attributes for browser autofill support
- [ ] Zod schema is the single source of truth — imported on both client and server
- [ ] Error messages are age-appropriate for the target grade band
- [ ] Vitest test: schema rejects invalid data; renders inline error messages

## Example

```
Student enters "notanemail" in the email field and clicks Log In.

→ Field border turns red
→ Error message appears: "That doesn't look like an email — check for a '@' symbol"
→ aria-live region announces the error to screen readers
→ Submit button remains clickable (onBlur validation, not on submit lock)
→ Server is NOT called — validation is client-side first
```
