# Project Conventions

> Discovered patterns and conventions in this codebase.

## Component Patterns

### Standard Component Structure
```tsx
// Imports
import { useState } from 'react';

// Types
interface Props {
  // ...
}

// Component
export function ComponentName({ prop }: Props) {
  // Hooks first
  // Derived state
  // Handlers
  // Render
}
```

### Hook Patterns
```tsx
export function useCustomHook() {
  // State
  // Effects
  // Callbacks
  // Return
}
```

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Component | PascalCase | `UserProfile.tsx` |
| Hook | useCamelCase | `useUserData.ts` |
| Utility | camelCase | `formatDate.ts` |
| Constant | UPPER_SNAKE | `API_BASE_URL` |
| Type/Interface | PascalCase | `UserData` |

## File Organization

<!-- Document how files are organized -->

## API Patterns

<!-- Document API call patterns -->

## State Management Patterns

<!-- Document state management approach -->

## Testing Patterns

<!-- Document testing conventions -->

## Styling Conventions

<!-- Document styling approach -->
