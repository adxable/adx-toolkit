---
name: react-performance
description: React performance optimization patterns using memoization, code splitting, and efficient rendering strategies. Use when optimizing slow React applications, reducing bundle size, improving user experience with large datasets, or splitting view components for better re-render isolation.
---

# React Performance Optimization

Expert guidance for optimizing React application performance through memoization, code splitting, virtualization, state management optimization, and efficient rendering strategies.

## When to Use This Skill

- Optimizing slow-rendering React components
- Preventing unnecessary re-renders in complex component trees
- Splitting view components for better isolation
- Optimizing Zustand stores and selectors
- Reducing bundle size for faster initial load times
- Improving responsiveness for large lists or data tables
- Debugging performance issues with React DevTools Profiler

## Quick Start - Performance Checklist

Before implementing any component, check these optimization points:

- [ ] `useMemo` for expensive computations (filter, sort, map)
- [ ] `useCallback` for functions passed to children
- [ ] `React.memo` for expensive/frequently re-rendered components
- [ ] Debounce search/filter (300-500ms)
- [ ] Cleanup timeouts/intervals in useEffect
- [ ] Watch specific form fields (not all)
- [ ] Stable keys in lists
- [ ] Lazy load heavy libraries (jsPDF, XLSX)
- [ ] Code splitting with React.lazy
- [ ] Split Zustand stores by concern (modals vs filters vs data)
- [ ] Use `useShallow` for object selectors in Zustand
- [ ] Single Suspense boundary at layout level (not per-route)
- [ ] Split monolithic hooks into component-based architecture

---

## Topic Guides

### Core Memoization Patterns
Fundamental React optimization with useMemo, useCallback, and React.memo.
**[Read: resources/memoization-patterns.md](resources/memoization-patterns.md)**

### View Component Splitting
Architecture for splitting large views into smaller components with isolated re-renders.
**[Read: resources/view-component-splitting.md](resources/view-component-splitting.md)**

### Zustand Store Optimization
Patterns for optimizing Zustand stores to minimize re-renders.
**[Read: resources/zustand-optimization.md](resources/zustand-optimization.md)**

### Code Splitting & Lazy Loading
Strategies for reducing bundle size and loading code on demand.
**[Read: resources/code-splitting.md](resources/code-splitting.md)**

---

## Quick Reference

### useMemo - Expensive Computations

```typescript
// When to use: filter, sort, map operations; complex calculations
const filteredItems = useMemo(() => {
    return items
        .filter(item => item.name.toLowerCase().includes(searchTerm.toLowerCase()))
        .sort((a, b) => a.name.localeCompare(b.name));
}, [items, searchTerm]);
```

### useCallback - Event Handlers

```typescript
// When to use: Functions passed as props to children
const handleClick = useCallback((id: string) => {
    console.log('Clicked:', id);
}, []); // Empty deps = function never changes
```

### React.memo - Component Memoization

```typescript
// When to use: Expensive components, list items, DataGrid cells
export const ExpensiveComponent = React.memo<ExpensiveComponentProps>(
    function ExpensiveComponent({ data, onAction }) {
        return <ComplexVisualization data={data} />;
    }
);
```

### Zustand with useShallow

```typescript
import { useShallow } from 'zustand/shallow';

// CRITICAL: Always use useShallow for object selectors
const { isOpen, item } = useModalStore(
    useShallow((state) => ({
        isOpen: state.isEditModalOpen,
        item: state.selectedItem,
    }))
);
```

---

## Anti-Patterns to Avoid

| Pattern | Problem | Solution |
|---------|---------|----------|
| Object selector without `useShallow` | Infinite re-render loops | Wrap in `useShallow` |
| Inline functions in JSX passed to children | New reference every render | Use `useCallback` |
| Modal state in parent component | Unnecessary re-renders | Move to Zustand store |
| Missing `memo` on child components | Cascading re-renders | Wrap in `React.memo` |
| Index as list key | Breaks reconciliation | Use stable unique IDs |
| Watch all form fields | Excessive re-renders | Watch specific fields |

---

## Resources

- **React Docs - Performance**: https://react.dev/learn/render-and-commit
- **React DevTools**: Chrome/Firefox extension for profiling
- **react-window**: https://github.com/bvaughn/react-window
- **Zustand**: https://github.com/pmndrs/zustand
- **Bundle analyzers**: webpack-bundle-analyzer, vite-bundle-visualizer
