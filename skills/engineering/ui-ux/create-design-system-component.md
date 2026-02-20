# Skill: Create Design System Component

## Purpose
Define the standard procedure for creating reusable, accessible, documented design system components in AceQuest's component library. Each component must support the three age-band variants, follow Tailwind conventions, expose a clear TypeScript API, and include Storybook stories and Vitest tests.

## Used By
- UI/UX Designer Agent
- Frontend Engineer Agent

## Inputs
| Field | Type | Description |
|-------|------|-------------|
| `componentName` | string | PascalCase component name, e.g. `BadgeCard`, `ScorePill` |
| `componentType` | `"atom" \| "molecule" \| "organism"` | Atomic design level |
| `variants` | string[] | Visual variants, e.g. `["common", "rare", "epic", "legendary"]` |
| `states` | string[] | Interaction states, e.g. `["default", "hover", "active", "disabled"]` |
| `ageBandAware` | boolean | Whether the component changes appearance per age band |

## Procedure / Template

### Step 1 — Define the Component API (TypeScript Interface)

```typescript
// src/components/ui/BadgeCard/BadgeCard.types.ts
import { AgeBand } from "@/hooks/useBand";

export type BadgeRarity = "COMMON" | "RARE" | "EPIC" | "LEGENDARY";

export interface BadgeCardProps {
  /** Badge slug used as the image filename */
  slug: string;
  /** Display name of the badge */
  name: string;
  /** Badge rarity tier — affects colour and animation */
  rarity: BadgeRarity;
  /** XP reward associated with the badge */
  xpReward: number;
  /** Whether the badge was just unlocked (triggers animation) */
  isNew?: boolean;
  /** Override automatic age-band detection */
  band?: AgeBand;
  /** Callback when the badge card is clicked/tapped */
  onClick?: () => void;
  /** Additional CSS classes */
  className?: string;
}
```

### Step 2 — Implement the Component

```tsx
// src/components/ui/BadgeCard/BadgeCard.tsx
"use client";

import Image from "next/image";
import { forwardRef } from "react";
import { cn } from "@/lib/utils";
import { useBand } from "@/hooks/useBand";
import { BadgeCardProps, BadgeRarity } from "./BadgeCard.types";
import { rarityConfig } from "./BadgeCard.config";

export const BadgeCard = forwardRef<HTMLDivElement, BadgeCardProps>(
  ({ slug, name, rarity, xpReward, isNew = false, band: bandOverride, onClick, className }, ref) => {
    const detectedBand = useBand();
    const band = bandOverride ?? detectedBand;
    const config = rarityConfig[rarity];
    const iconSize = band === "band-1" ? 64 : band === "band-2" ? 48 : 36;

    return (
      <div
        ref={ref}
        role={onClick ? "button" : "listitem"}
        tabIndex={onClick ? 0 : undefined}
        aria-label={`${name} badge — ${rarity.toLowerCase()} rarity, ${xpReward} XP${isNew ? " — just unlocked!" : ""}`}
        onClick={onClick}
        onKeyDown={(e) => {
          if (onClick && (e.key === "Enter" || e.key === " ")) {
            e.preventDefault();
            onClick();
          }
        }}
        className={cn(
          "flex items-center gap-3 rounded-xl border-2 p-3 transition-all",
          "focus:outline-none focus:ring-4 focus:ring-quest-purple focus:ring-offset-2",
          onClick && "cursor-pointer hover:scale-102 active:scale-98",
          config.borderColor,
          config.bgColor,
          isNew && "animate-badge-unlock",
          className
        )}
      >
        {/* Badge Icon */}
        <div className={cn("relative flex-shrink-0", config.glowClass)}>
          <Image
            src={`/badges/${slug}.svg`}
            alt=""                          // decorative — card aria-label is descriptive
            width={iconSize}
            height={iconSize}
            className="rounded-full"
          />
          {isNew && (
            <span
              aria-hidden="true"
              className="absolute -top-1 -right-1 text-xs bg-quest-gold text-white rounded-full w-4 h-4 flex items-center justify-center"
            >
              !
            </span>
          )}
        </div>

        {/* Badge Info */}
        <div className="flex flex-col min-w-0">
          <span className={cn("font-semibold truncate", band === "band-1" ? "text-base" : "text-sm")}>
            {name}
          </span>
          <span className={cn("text-xs", config.rarityTextColor)}>
            {rarity.charAt(0) + rarity.slice(1).toLowerCase()} • {xpReward} XP
          </span>
        </div>
      </div>
    );
  }
);
BadgeCard.displayName = "BadgeCard";
```

### Step 3 — Configuration Map

```typescript
// src/components/ui/BadgeCard/BadgeCard.config.ts
import { BadgeRarity } from "./BadgeCard.types";

interface RarityConfig {
  borderColor: string;
  bgColor: string;
  rarityTextColor: string;
  glowClass: string;
}

export const rarityConfig: Record<BadgeRarity, RarityConfig> = {
  COMMON: {
    borderColor: "border-gray-200",
    bgColor: "bg-white",
    rarityTextColor: "text-gray-500",
    glowClass: "",
  },
  RARE: {
    borderColor: "border-quest-purple",
    bgColor: "bg-purple-50",
    rarityTextColor: "text-quest-purple",
    glowClass: "",
  },
  EPIC: {
    borderColor: "border-orange-400",
    bgColor: "bg-orange-50",
    rarityTextColor: "text-orange-600",
    glowClass: "",
  },
  LEGENDARY: {
    borderColor: "border-quest-gold",
    bgColor: "bg-yellow-50",
    rarityTextColor: "text-quest-gold",
    glowClass: "drop-shadow-[0_0_8px_rgba(217,119,6,0.6)]",
  },
};
```

### Step 4 — Tailwind Animation Extension

```typescript
// tailwind.config.ts  (excerpt)
module.exports = {
  theme: {
    extend: {
      keyframes: {
        "badge-unlock": {
          "0%":   { opacity: "0", transform: "scale(0.6) translateY(20px)" },
          "70%":  { transform: "scale(1.1) translateY(-4px)" },
          "100%": { opacity: "1", transform: "scale(1) translateY(0)" },
        },
      },
      animation: {
        "badge-unlock": "badge-unlock 500ms ease-out forwards",
      },
    },
  },
};
```

### Step 5 — Barrel Export

```typescript
// src/components/ui/BadgeCard/index.ts
export { BadgeCard } from "./BadgeCard";
export type { BadgeCardProps, BadgeRarity } from "./BadgeCard.types";
```

### Step 6 — Storybook Stories

```tsx
// src/components/ui/BadgeCard/BadgeCard.stories.tsx
import type { Meta, StoryObj } from "@storybook/react";
import { BadgeCard } from "./BadgeCard";

const meta: Meta<typeof BadgeCard> = {
  title: "UI / BadgeCard",
  component: BadgeCard,
  tags: ["autodocs"],
  argTypes: {
    rarity: { control: "select", options: ["COMMON", "RARE", "EPIC", "LEGENDARY"] },
    band: { control: "select", options: ["band-1", "band-2", "band-3"] },
  },
};
export default meta;
type Story = StoryObj<typeof BadgeCard>;

export const Default: Story = {
  args: { slug: "first-quiz", name: "First Quiz!", rarity: "COMMON", xpReward: 50 },
};

export const Legendary: Story = {
  args: { slug: "perfect-ten", name: "Perfect 10", rarity: "LEGENDARY", xpReward: 500, isNew: true },
};

export const AllRarities: Story = {
  render: () => (
    <div className="flex flex-col gap-4 p-4 max-w-xs">
      {(["COMMON", "RARE", "EPIC", "LEGENDARY"] as const).map((rarity) => (
        <BadgeCard key={rarity} slug="first-quiz" name={rarity} rarity={rarity} xpReward={100} />
      ))}
    </div>
  ),
};

export const Band1Large: Story = {
  args: { slug: "quiz-master", name: "Quiz Master", rarity: "RARE", xpReward: 200, band: "band-1" },
};
```

### Step 7 — Vitest Tests

```tsx
// src/components/ui/BadgeCard/BadgeCard.test.tsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect, vi } from "vitest";
import { BadgeCard } from "./BadgeCard";

describe("BadgeCard", () => {
  it("renders badge name and rarity", () => {
    render(<BadgeCard slug="first-quiz" name="First Quiz!" rarity="COMMON" xpReward={50} />);
    expect(screen.getByText("First Quiz!")).toBeInTheDocument();
    expect(screen.getByText(/common/i)).toBeInTheDocument();
  });

  it("has descriptive aria-label including rarity and XP", () => {
    render(<BadgeCard slug="quiz-master" name="Quiz Master" rarity="LEGENDARY" xpReward={500} isNew />);
    expect(screen.getByRole("listitem")).toHaveAccessibleName(
      /Quiz Master badge — legendary rarity, 500 XP — just unlocked!/i
    );
  });

  it("is keyboard activatable when onClick is provided", async () => {
    const user = userEvent.setup();
    const handleClick = vi.fn();
    render(
      <BadgeCard slug="first-quiz" name="First Quiz!" rarity="COMMON" xpReward={50} onClick={handleClick} />
    );
    const card = screen.getByRole("button");
    await user.tab();
    await user.keyboard("{Enter}");
    expect(handleClick).toHaveBeenCalledOnce();
  });
});
```

## Output
- `src/components/ui/<ComponentName>/` directory with:
  - `<ComponentName>.tsx` — implementation
  - `<ComponentName>.types.ts` — TypeScript interface
  - `<ComponentName>.config.ts` — variant/config map
  - `<ComponentName>.stories.tsx` — Storybook stories
  - `<ComponentName>.test.tsx` — Vitest tests
  - `index.ts` — barrel export

## Quality Checks
- [ ] Component uses `forwardRef` to allow ref forwarding
- [ ] All interactive variants have `role`, `tabIndex`, `aria-label`, keyboard handler
- [ ] Config map used for all visual variants — no inline conditional classes
- [ ] Storybook stories cover: all variants, all states, all age bands
- [ ] `displayName` set on `forwardRef` components
- [ ] Tests cover accessibility attributes and keyboard interaction
- [ ] `@media (prefers-reduced-motion)` respected for unlock animations
- [ ] Component is exported from `src/components/ui/index.ts` barrel
