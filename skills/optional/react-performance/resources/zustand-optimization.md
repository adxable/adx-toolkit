# Zustand Store Optimization

Patterns for optimizing Zustand stores to minimize re-renders.

---

## Split Stores by Concern

Combining unrelated state in one store causes unnecessary re-renders:

```typescript
// ❌ AVOID - Single monolithic store
const useViewStore = create((set) => ({
  // Filter state
  isFilterVisible: false,
  criteria: {},
  // Modal state
  isCreateModalOpen: false,
  isEditModalOpen: false,
  selectedItem: null,
  // Actions...
}));
// Problem: Opening modal re-renders filter subscribers!

// ✅ CORRECT - Split by concern
const useFilterStore = create((set) => ({
  isFilterVisible: false,
  toggleFilterVisible: () => set((s) => ({ isFilterVisible: !s.isFilterVisible })),
}));

const useModalStore = create((set) => ({
  isCreateModalOpen: false,
  isEditModalOpen: false,
  selectedItem: null,
  openCreateModal: () => set({ isCreateModalOpen: true }),
  openEditModal: (item) => set({ isEditModalOpen: true, selectedItem: item }),
}));
```

---

## Use Selectors with useShallow

```typescript
import { useShallow } from 'zustand/shallow';

// ❌ AVOID - Returns new object every time, causes re-renders
const { isOpen, item } = useModalStore((state) => ({
  isOpen: state.isEditModalOpen,
  item: state.selectedItem,
}));

// ✅ CORRECT - useShallow prevents unnecessary re-renders
const { isOpen, item } = useModalStore(
  useShallow((state) => ({
    isOpen: state.isEditModalOpen,
    item: state.selectedItem,
  }))
);

// ✅ ALSO CORRECT - Single primitive selector (no useShallow needed)
const isOpen = useModalStore((state) => state.isEditModalOpen);
```

---

## Export Focused Selector Hooks

```typescript
// Create focused selector hooks for common access patterns
export const useEditModalState = () =>
  useModalStore(
    useShallow((state) => ({
      isEditModalOpen: state.isEditModalOpen,
      selectedItem: state.selectedItem,
      setEditModalOpen: state.setEditModalOpen,
    }))
  );

export const useModalActions = () =>
  useModalStore(
    useShallow((state) => ({
      openCreateModal: state.openCreateModal,
      openEditModal: state.openEditModal,
    }))
  );
```

---

## Complete Store Example

```typescript
// src/features/{feature}/stores/use{View}Store.ts
import { create } from 'zustand';
import { useShallow } from 'zustand/shallow';

interface MyViewState {
  // Modal state
  isCreateModalOpen: boolean;
  isEditModalOpen: boolean;
  selectedItem: ItemType | undefined;

  // Selection state
  selectedItems: ItemType[];

  // Modal actions
  openCreateModal: () => void;
  openEditModal: (item: ItemType) => void;
  setCreateModalOpen: (open: boolean) => void;
  setEditModalOpen: (open: boolean) => void;

  // Selection actions
  setSelectedItems: (items: ItemType[]) => void;
  clearSelectedItems: () => void;
}

export const useMyViewStore = create<MyViewState>((set) => ({
  // Initial state
  isCreateModalOpen: false,
  isEditModalOpen: false,
  selectedItem: undefined,
  selectedItems: [],

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
  },

  setSelectedItems: (items) => {
    set({ selectedItems: items });
  },

  clearSelectedItems: () => {
    set({ selectedItems: [] });
  }
}));

// Focused selector hooks - CRITICAL: use useShallow!
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

export const useSelectedItems = () =>
  useMyViewStore(
    useShallow((state) => ({
      selectedItems: state.selectedItems,
      setSelectedItems: state.setSelectedItems,
      clearSelectedItems: state.clearSelectedItems
    }))
  );
```

---

## Key Rules

### 1. Always Use `useShallow` for Object Selectors

```typescript
// ❌ BAD - Creates new object every render - infinite loop!
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

### 2. Primitive Selectors Don't Need useShallow

```typescript
// Single primitive value - no useShallow needed
const isOpen = useStore((state) => state.isOpen);
const count = useStore((state) => state.count);
```

### 3. Keep URL State in React Components

URL filter hooks use React Router and must stay in a component context:

```typescript
// Parent component manages URL state
const [searchParams, setSearchParams] = useSearchParams();

// Pass to children via props
<FiltersSidebar criteria={criteria} onApply={setCriteria} />
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Object selector without `useShallow` | Add `useShallow` wrapper |
| Monolithic store with unrelated state | Split into focused stores |
| Subscribing to entire store | Use focused selectors |
| URL state in Zustand | Keep in React components |
