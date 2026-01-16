# Core Memoization Patterns

Fundamental React optimization with useMemo, useCallback, and React.memo.

---

## useMemo for Expensive Computations

```typescript
import { useMemo } from 'react';

export const DataDisplay: React.FC<{ items: Item[], searchTerm: string }> = ({
    items,
    searchTerm,
}) => {
    // ✅ CORRECT - Memoized, only recalculates when dependencies change
    const filteredItems = useMemo(() => {
        return items
            .filter(item => item.name.toLowerCase().includes(searchTerm.toLowerCase()))
            .sort((a, b) => a.name.localeCompare(b.name));
    }, [items, searchTerm]);

    return <List items={filteredItems} />;
};
```

**When to use useMemo:**

- Filtering/sorting large arrays
- Complex calculations
- Transforming data structures
- Expensive computations (loops, recursion)

**When NOT to use useMemo:**

- Simple string concatenation
- Basic arithmetic
- Premature optimization (profile first!)

---

## useCallback for Event Handlers

### The Problem

```typescript
// ❌ AVOID - Creates new function on every render
export const Parent: React.FC = () => {
    const handleClick = (id: string) => {
        console.log('Clicked:', id);
    };

    // Child re-renders every time Parent renders
    // because handleClick is a new function reference each time
    return <Child onClick={handleClick} />;
};
```

### The Solution

```typescript
import { useCallback } from 'react';

export const Parent: React.FC = () => {
    // ✅ CORRECT - Stable function reference
    const handleClick = useCallback((id: string) => {
        console.log('Clicked:', id);
    }, []); // Empty deps = function never changes

    // Child only re-renders when props actually change
    return <Child onClick={handleClick} />;
};
```

**When to use useCallback:**

- Functions passed as props to children
- Functions used as dependencies in useEffect
- Functions passed to memoized components
- Event handlers in lists

**When NOT to use useCallback:**

- Event handlers not passed to children
- Simple inline handlers: `onClick={() => doSomething()}`

---

## React.memo for Component Memoization

### Basic Usage

```typescript
import React from 'react';

interface ExpensiveComponentProps {
    data: ComplexData;
    onAction: () => void;
}

// ✅ Wrap expensive components in React.memo
export const ExpensiveComponent = React.memo<ExpensiveComponentProps>(
    function ExpensiveComponent({ data, onAction }) {
        // Complex rendering logic
        return <ComplexVisualization data={data} />;
    }
);
```

**When to use React.memo:**

- Component renders frequently
- Component has expensive rendering
- Props don't change often
- Component is a list item

**When NOT to use React.memo:**

- Props change frequently anyway
- Rendering is already fast
- Premature optimization

---

## Preventing Component Re-initialization

### The Problem

```typescript
// ❌ AVOID - Component recreated on every render
export const Parent: React.FC = () => {
    // New component definition each render!
    const ChildComponent = () => <div>Child</div>;

    return <ChildComponent />;  // Unmounts and remounts every render
};
```

### The Solution

```typescript
// ✅ CORRECT - Define outside or use useMemo
const ChildComponent: React.FC = () => <div>Child</div>;

export const Parent: React.FC = () => {
    return <ChildComponent />;  // Stable component
};

// ✅ OR if dynamic, use useMemo
export const Parent: React.FC<{ config: Config }> = ({ config }) => {
    const DynamicComponent = useMemo(() => {
        return () => <div>{config.title}</div>;
    }, [config.title]);

    return <DynamicComponent />;
};
```

---

## Debounced Search

### Using use-debounce Hook

```typescript
import { useState } from 'react';
import { useDebounce } from 'use-debounce';
import { useSuspenseQuery } from '@tanstack/react-query';

export const SearchComponent: React.FC = () => {
    const [searchTerm, setSearchTerm] = useState('');

    // Debounce for 300ms
    const [debouncedSearchTerm] = useDebounce(searchTerm, 300);

    // Query uses debounced value
    const { data } = useSuspenseQuery({
        queryKey: ['search', debouncedSearchTerm],
        queryFn: () => api.search(debouncedSearchTerm),
        enabled: debouncedSearchTerm.length > 0,
    });

    return (
        <input
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder='Search...'
        />
    );
};
```

**Optimal Debounce Timing:**

- **300-500ms**: Search/filtering
- **1000ms**: Auto-save
- **100-200ms**: Real-time validation

---

## List Rendering Optimization

### Key Prop Usage

```typescript
// ✅ CORRECT - Stable unique keys
{items.map(item => (
    <ListItem key={item.id}>
        {item.name}
    </ListItem>
))}

// ❌ AVOID - Index as key (unstable if list changes)
{items.map((item, index) => (
    <ListItem key={index}>  // WRONG if list reorders
        {item.name}
    </ListItem>
))}
```

### Memoized List Items

```typescript
const ListItem = React.memo<ListItemProps>(({ item, onAction }) => {
    return (
        <div
            onClick={() => onAction(item.id)}
            className="p-4 hover:bg-gray-50 cursor-pointer"
        >
            {item.name}
        </div>
    );
});

export const List: React.FC<{ items: Item[] }> = ({ items }) => {
    const handleAction = useCallback((id: string) => {
        console.log('Action:', id);
    }, []);

    return (
        <div className="divide-y divide-gray-200">
            {items.map(item => (
                <ListItem
                    key={item.id}
                    item={item}
                    onAction={handleAction}
                />
            ))}
        </div>
    );
};
```

---

## Form Performance

### Watch Specific Fields (Not All)

```typescript
import { useForm } from 'react-hook-form';

export const MyForm: React.FC = () => {
    const { register, watch, handleSubmit } = useForm();

    // ❌ AVOID - Watches all fields, re-renders on any change
    const formValues = watch();

    // ✅ CORRECT - Watch only what you need
    const username = watch('username');
    const email = watch('email');

    // Or multiple specific fields
    const [username, email] = watch(['username', 'email']);

    return (
        <form onSubmit={handleSubmit(onSubmit)}>
            <input {...register('username')} />
            <input {...register('email')} />
            <input {...register('password')} />

            {/* Only re-renders when username/email change */}
            <p>Username: {username}, Email: {email}</p>
        </form>
    );
};
```
