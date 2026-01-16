# Code Splitting & Lazy Loading

Strategies for reducing bundle size and loading code on demand.

---

## React.lazy for Component Splitting

```typescript
import { lazy, Suspense } from 'react';

// ✅ CORRECT - Lazy load heavy components
const HeavyChart = lazy(() => import('./HeavyChart'));
const DataGrid = lazy(() => import('@/components/DataGrid'));
const PDFViewer = lazy(() => import('./PDFViewer'));

function Dashboard() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <HeavyChart data={chartData} />
    </Suspense>
  );
}
```

---

## Lazy Loading Heavy Dependencies

```typescript
// ❌ AVOID - Import heavy libraries at top level
import jsPDF from 'jspdf'; // Large library loaded immediately
import * as XLSX from 'xlsx'; // Large library loaded immediately

// ✅ CORRECT - Dynamic import when needed
const handleExportPDF = async () => {
  const { jsPDF } = await import('jspdf');
  const doc = new jsPDF();
  // Use it
};

const handleExportExcel = async () => {
  const XLSX = await import('xlsx');
  // Use it
};
```

---

## Route-Based Code Splitting

```typescript
import { createBrowserRouter } from 'react-router';
import { lazy, Suspense } from 'react';

// Lazy-loaded route components
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Reports = lazy(() => import('./pages/Reports'));
const Settings = lazy(() => import('./pages/Settings'));
const AdminPanel = lazy(() => import('./pages/AdminPanel'));

// Component-level code splitting for heavy features
const HeavyChart = lazy(() => import('./components/HeavyChart'));

function App() {
  return (
    <BrowserRouter>
      <Suspense fallback={<LoadingSpinner />}>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/reports" element={<Reports />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="/admin" element={<AdminPanel />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  );
}
```

**Benefits:**
- Reduces initial bundle size (faster First Contentful Paint)
- Loads code only when needed (better caching)
- Route-based splitting: Users only download visited pages

---

## Conditional Component Loading

```typescript
function DataVisualization({ data, showChart }) {
  return (
    <div>
      <h2>Data Overview</h2>
      {showChart && (
        <Suspense fallback={<div>Loading chart...</div>}>
          <HeavyChart data={data} />
        </Suspense>
      )}
    </div>
  );
}
```

---

## Bundle Optimization - Smart Imports

```typescript
// ❌ BAD - Imports entire library
import _ from 'lodash';
import { Button, Modal, Table, Form } from 'antd';

// ✅ GOOD - Import only needed functions
import debounce from 'lodash/debounce';
import groupBy from 'lodash/groupBy';

// ✅ GOOD - Tree-shakeable imports (if library supports it)
import { Button } from 'antd/es/button';
import { Modal } from 'antd/es/modal';

// ✅ GOOD - Dynamic imports for heavy libraries
const PDFViewer = lazy(() => import('react-pdf-viewer'));
const CodeEditor = lazy(() => import('@monaco-editor/react'));
```

---

## Preloading Critical Routes

```typescript
// Preload when user hovers over link
const handleMouseEnter = () => {
  import('./pages/Reports'); // Start loading before click
};

// Or use link preload
<link rel="preload" href="/static/js/reports.chunk.js" as="script" />
```

---

## Named Exports with Lazy Loading

```typescript
// When component uses named export
const MyComponent = lazy(() =>
  import('./MyComponent').then(module => ({
    default: module.MyComponent
  }))
);
```

---

## Bundle Analysis

```bash
# Webpack Bundle Analyzer
npm install --save-dev webpack-bundle-analyzer

# Vite Bundle Visualizer
npm install --save-dev rollup-plugin-visualizer

# Analyze bundle composition
npm run build -- --stats
npx webpack-bundle-analyzer dist/stats.json
```

---

## What to Lazy Load

**Always lazy load:**
- Route components (pages)
- Heavy visualization libraries (charts, maps)
- Rich text editors
- PDF viewers
- Export functionality (PDF, Excel)
- Admin-only features
- Modals with complex forms

**Don't lazy load:**
- Small, frequently used components
- Components above the fold
- Navigation components
- Layout components

---

## Complete Example

```typescript
// routes.tsx
import { lazy, Suspense } from 'react';
import { createBrowserRouter, Outlet } from 'react-router';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';

// Layout (not lazy - needed immediately)
import { AppLayout } from '@/layouts/AppLayout';

// Lazy load all route components
const HomePage = lazy(() => import('@/features/home/HomePage'));
const UsersPage = lazy(() => import('@/features/users/UsersPage'));
const ReportsPage = lazy(() => import('@/features/reports/ReportsPage'));
const SettingsPage = lazy(() => import('@/features/settings/SettingsPage'));

// Layout wrapper with Suspense
const LayoutWithSuspense = () => (
  <AppLayout>
    <Suspense fallback={<LoadingSpinner />}>
      <Outlet />
    </Suspense>
  </AppLayout>
);

export const router = createBrowserRouter([
  {
    element: <LayoutWithSuspense />,
    children: [
      { path: '/', element: <HomePage /> },
      { path: '/users', element: <UsersPage /> },
      { path: '/reports', element: <ReportsPage /> },
      { path: '/settings', element: <SettingsPage /> },
    ],
  },
]);
```
