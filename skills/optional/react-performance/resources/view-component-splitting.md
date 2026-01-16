# View Component Splitting for Performance

Guidelines for splitting large view components into smaller, focused components to prevent unnecessary re-renders.

---

## The Problem

When a view component holds multiple pieces of state (filters, modals, data), **any state change causes the entire component tree to re-render**:

```typescript
// ❌ BAD - All state in one component
export const MyView: React.FC = () => {
  const [isFilterVisible, setIsFilterVisible] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);  // Modal state change...
  const [criteria, setCriteria] = useSearchParams(); // or custom URL filter hook
  const { data } = useQuery(...);

  // ...re-renders EVERYTHING including filters and table!
  return (
    <>
      <Filters ... />
      <Table ... />
      <Modal open={isModalOpen} />
    </>
  );
};
```

---

## The Solution: Component Splitting + Zustand Store

### Architecture Pattern

```
ViewComponent (orchestrator)
├── FiltersSidebar ────────── [criteria state]
├── Header
│   ├── FilterButton ──────── [filter visibility]
│   └── ActionButtons ─────── [modal open actions]
├── Table ─────────────────── [data, loading, callbacks]
└── Modals ────────────────── [modal state from Zustand]
    ├── CreateModal ───────── [useCreateModalState]
    └── EditModal ─────────── [useEditModalState]
```

### Step 1: Create Zustand Store for Modal State

```typescript
// src/features/{feature}/stores/use{View}Store.ts
import { create } from 'zustand';
import { useShallow } from 'zustand/shallow';

interface MyViewState {
  // Modal state
  isCreateModalOpen: boolean;
  isEditModalOpen: boolean;
  selectedItem: ItemType | undefined;

  // Modal actions
  openCreateModal: () => void;
  openEditModal: (item: ItemType) => void;
  setCreateModalOpen: (open: boolean) => void;
  setEditModalOpen: (open: boolean) => void;
}

export const useMyViewStore = create<MyViewState>((set) => ({
  // Initial state
  isCreateModalOpen: false,
  isEditModalOpen: false,
  selectedItem: undefined,

  // Actions
  openCreateModal: () => {
    set({ isCreateModalOpen: true });
  },

  openEditModal: (item) => {
    set({ selectedItem: item, isEditModalOpen: true });
  },

  setCreateModalOpen: (open) => {
    set({ isCreateModalOpen: open });
    if (!open) set({ selectedItem: undefined });
  },

  setEditModalOpen: (open) => {
    set({ isEditModalOpen: open });
    if (!open) set({ selectedItem: undefined });
  }
}));

// ⚠️ CRITICAL: Use useShallow for object selectors to prevent infinite loops!
export const useCreateModalState = () =>
  useMyViewStore(
    useShallow((state) => ({
      isCreateModalOpen: state.isCreateModalOpen,
      setCreateModalOpen: state.setCreateModalOpen
    }))
  );

export const useEditModalState = () =>
  useMyViewStore(
    useShallow((state) => ({
      isEditModalOpen: state.isEditModalOpen,
      selectedItem: state.selectedItem,
      setEditModalOpen: state.setEditModalOpen
    }))
  );

export const useModalActions = () =>
  useMyViewStore(
    useShallow((state) => ({
      openCreateModal: state.openCreateModal,
      openEditModal: state.openEditModal
    }))
  );
```

### Step 2: Create Split Components

#### Filter Components

```typescript
// components/MyViewFilters.tsx
import { memo, useMemo } from 'react';

interface FilterButtonProps {
  isFilterVisible: boolean;
  onToggleFilter: () => void;
}

export const MyViewFilterButton = memo(function MyViewFilterButton({
  isFilterVisible,
  onToggleFilter
}: FilterButtonProps) {
  return (
    <Button
      variant={isFilterVisible ? 'primary' : 'ghost'}
      size="sm"
      onClick={onToggleFilter}
    >
      <FilterIcon />
    </Button>
  );
});

interface FiltersSidebarProps {
  isFilterVisible: boolean;
  criteria: QueryCriteria;
  onApplyCriteria: (criteria: QueryCriteria) => void;
  onClearCriteria: () => void;
}

export const MyViewFiltersSidebar = memo(function MyViewFiltersSidebar({
  isFilterVisible,
  criteria,
  onApplyCriteria,
  onClearCriteria
}: FiltersSidebarProps) {
  const formValues = useMemo(() => transformToFormData(criteria), [criteria]);

  if (!isFilterVisible) return null;

  return (
    <div className="animate-in fade-in slide-in-from-left-3 border-r w-64 shrink-0">
      <Filters
        onApply={onApplyCriteria}
        onClear={onClearCriteria}
        initialValues={formValues}
      />
    </div>
  );
});
```

#### Modal Components (Isolated State)

```typescript
// components/MyViewModals.tsx
import { memo } from 'react';
import { useCreateModalState, useEditModalState } from '../stores/useMyViewStore';

interface ModalsProps {
  items: ItemType[];
}

export const MyViewModals = memo(function MyViewModals({ items }: ModalsProps) {
  return (
    <>
      <CreateModal items={items} />
      <EditModal items={items} />
    </>
  );
});

// Each modal subscribes only to its own state
const CreateModal = memo(function CreateModal({ items }: { items: ItemType[] }) {
  const { isCreateModalOpen, setCreateModalOpen } = useCreateModalState();

  return (
    <FormModal
      mode="create"
      open={isCreateModalOpen}
      onOpenChange={setCreateModalOpen}
      items={items}
    />
  );
});

const EditModal = memo(function EditModal({ items }: { items: ItemType[] }) {
  const { isEditModalOpen, selectedItem, setEditModalOpen } = useEditModalState();

  return (
    <FormModal
      mode="edit"
      open={isEditModalOpen}
      onOpenChange={setEditModalOpen}
      items={items}
      itemToEdit={selectedItem}
    />
  );
});
```

### Step 3: Refactor Main View Component

```typescript
// MyView.tsx
import { useCallback, useState } from 'react';
import { useModalActions } from './stores/useMyViewStore';

export const MyView: React.FC = () => {
  // Local state for filter visibility
  const [isFilterVisible, setIsFilterVisible] = useState(false);

  // URL filters (stays in parent for URL sync)
  // Use useSearchParams or a custom URL filter hook
  const [criteria, setCriteria] = useState<QueryCriteria>(defaultCriteria);
  const clearCriteria = useCallback(() => setCriteria(defaultCriteria), []);

  // Data fetching
  const { data, isLoading } = useQuery(...);

  // Modal actions from store - stable references, no re-renders
  const { openCreateModal, openEditModal } = useModalActions();

  // Memoized callbacks
  const handleToggleFilter = useCallback(() => {
    setIsFilterVisible((prev) => !prev);
  }, []);

  return (
    <>
      <div className="flex flex-1 overflow-hidden">
        {/* Filters - re-renders only when filter state changes */}
        <MyViewFiltersSidebar
          isFilterVisible={isFilterVisible}
          criteria={criteria}
          onApplyCriteria={setCriteria}
          onClearCriteria={clearCriteria}
        />

        <div className="flex h-full w-full flex-col">
          {/* Table - re-renders only when data changes */}
          <MyViewTable
            isLoading={isLoading}
            data={data ?? []}
            onEdit={openEditModal}
          />
        </div>
      </div>

      {/* Modals - ISOLATED, only re-renders when modal state changes */}
      <MyViewModals items={data ?? []} />
    </>
  );
};
```

---

## Key Rules

### 1. Always Use `useShallow` for Object Selectors

```typescript
// ❌ BAD - Creates new object every render → infinite loop!
export const useModalState = () =>
  useStore((state) => ({
    isOpen: state.isOpen,
    setOpen: state.setOpen
  }));

// ✅ GOOD - useShallow does shallow comparison
import { useShallow } from 'zustand/shallow';

export const useModalState = () =>
  useStore(
    useShallow((state) => ({
      isOpen: state.isOpen,
      setOpen: state.setOpen
    }))
  );
```

### 2. Use `memo` for All Split Components

```typescript
// ✅ Always wrap split components in memo
export const MyComponent = memo(function MyComponent(props) {
  // ...
});
```

### 3. Use `useCallback` for All Event Handlers Passed to Children

```typescript
// ✅ Stable reference prevents child re-renders
const handleClick = useCallback(() => {
  doSomething();
}, []);
```

### 4. Isolate Modal State in Zustand Store

Modal open/close state causes the most unnecessary re-renders. Always move to store.

---

## Checklist for New Views

- [ ] Create Zustand store for modal state with `useShallow` selectors
- [ ] Split into: Filters, Header/Actions, Table, Modals components
- [ ] Wrap all split components in `React.memo`
- [ ] Use `useCallback` for all handlers passed to children
- [ ] Modals component uses store selectors, not props
- [ ] Verify no infinite re-render loops (test by opening modal)

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Object selector without `useShallow` | Add `useShallow` wrapper |
| Inline functions in JSX | Use `useCallback` |
| Modal state in parent component | Move to Zustand store |
| Missing `memo` on child components | Wrap in `React.memo` |
| Creating new objects in render | Use `useMemo` |
