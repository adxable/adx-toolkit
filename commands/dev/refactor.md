# Refactor File

Analyze and create a plan to refactor a file into smaller, more maintainable parts following frontend architecture guidelines.

## Arguments

- `$ARGUMENTS` - Path to the file to refactor

## Configuration

Load project configuration from `.claude/frontend-dev-toolkit.json`.

## ⛔ CRITICAL: PLANNING ONLY - NO IMPLEMENTATION

**This command creates a PLAN only. You MUST NOT implement any changes.**

### Forbidden Actions
- ❌ DO NOT edit any source files (only create the plan file)
- ❌ DO NOT implement the refactoring
- ❌ DO NOT modify any code

### Required Actions
- ✅ Read and analyze the target file
- ✅ Identify extraction opportunities (hooks, components, utilities)
- ✅ Create the plan file in `.claude/specs/`
- ✅ Display the "PLAN CREATED SUCCESSFULLY" message
- ✅ Suggest running `/dev:implement {plan_path}` for implementation
- ✅ STOP after showing the suggested next steps

### Workflow Enforcement
```
/dev:refactor → Creates plan file → STOPS → User reviews plan → User runs /dev:implement
```

## Agent Invocation

Before starting the planning process, print this announcement:

```
═══════════════════════════════════════════════════
🚀 Invoking [frontend-architect] agent...
   └─ Task: Refactoring Analysis
   └─ Model: opus
   └─ File: {file_path}
═══════════════════════════════════════════════════
```

Then apply the frontend-architect agent's principles:
- Print `🏗️  [frontend-architect] Analyzing file structure...` when beginning
- Print `📚 [frontend-architect] Loading skill: react-performance` for performance patterns
- Print `📊 [frontend-architect] Analysis: {finding}` when identifying issues
- Print `✅ [frontend-architect] Planning complete.` when finished

## Instructions

### Step 1: Read and Analyze the Target File

```
🏗️  [frontend-architect] Analyzing file structure...
```

1. Read the target file specified in `$ARGUMENTS`
2. Analyze the file to identify:
   - **Total lines of code** (target: <150 lines per file)
   - **Number of useState/useEffect hooks** (signs of complex state management)
   - **Number of inline handlers** (candidates for useCallback extraction)
   - **Data transformations** (candidates for utility functions)
   - **Form logic** (candidate for custom hook)
   - **Complex JSX conditionals** (candidates for sub-components)

### Step 2: Apply Refactoring Guidelines

```
📚 [frontend-architect] Loading skill: react-performance
```

Reference the react-performance skill for optimization patterns.

#### When to Extract to Custom Hook

Extract when the file has:
- Multiple related useState calls (3+)
- Complex state transitions with useEffect
- Derived state calculations
- Business logic mixed with presentation
- Reusable stateful logic

#### When to Extract to Utility Function

Extract when the file has:
- Pure data transformations (e.g., mapping API response to form data)
- Validation logic
- Formatting functions
- Calculation logic without side effects

#### When to Split into Sub-Components

Split when the file has:
- Complex JSX conditionals (if/else in JSX)
- Multiple form sections (>3 distinct sections)
- Repeated UI patterns
- Clear logical groupings

### Step 3: Create the Refactoring Plan

Create the plan file at `.claude/specs/refactor-{file-name}.md`:

```markdown
# Refactor: {original file name}

## Metadata

- **Original File:** {full path to original file}
- **Original Lines:** {number of lines}
- **Target Lines:** {target lines after refactor}

## Analysis Summary

### Current Issues

```
📊 [frontend-architect] Analysis: {issue description}
```

- **Lines of code**: X lines (target: <150)
- **useState hooks**: X (threshold for extraction: 3+)
- **useEffect hooks**: X (consider consolidation)
- **Inline handlers**: X (candidates for useCallback)
- **Data transformations**: {list specific transformations}
- **Complex JSX sections**: {list sections}

### Extraction Opportunities

| Type | Name | Purpose | Lines Saved |
|------|------|---------|-------------|
| Hook | useXxx | {what it manages} | ~X |
| Utility | mapXxxToYyy | {what it transforms} | ~X |
| Component | XxxSection | {what it renders} | ~X |

## Refactoring Plan

### New Files to Create

#### 1. Hooks

**File:** `hooks/{hookName}.ts`
**Purpose:** {what the hook manages}
**Exports:**
- `{hookName}` - Main hook function
- `{TypeName}` - Return type interface

**Responsibilities:**
- {list what the hook handles}

#### 2. Utilities

**File:** `utils/{utilityName}.ts`
**Purpose:** {what it transforms/calculates}
**Exports:**
- `{functionName}` - Main function

#### 3. Components

**File:** `components/{ComponentName}.tsx`
**Purpose:** {what it renders}
**Props:**
```typescript
interface {ComponentName}Props {
  // List all props
}
```

### Updated Original File

After refactoring, the original file should:
- Import and use the new hooks
- Import and use the new utilities
- Render the new sub-components
- Be reduced to ~{target} lines (orchestration only)

## Step by Step Tasks

IMPORTANT: Execute every step in order, top to bottom.

### 1. Create Hook Files
- Create `{hook file path}`
- Implement hook with proper TypeScript interface
- Export hook and types

### 2. Create Utility Files
- Create `{utility file path}`
- Implement pure function with proper typing
- Export function

### 3. Create Sub-Components
- Create `{component file path}`
- Implement component with `React.memo` wrapper
- Define props interface

### 4. Refactor Original File
- Remove extracted logic
- Add imports for new hooks, utilities, components
- Update component to use extracted pieces

### 5. Validation
- Run TypeScript type checking
- Run build
- Run ESLint

## Validation Commands

```bash
{config.commands.typeCheck}
{config.commands.lint}
{config.commands.build}
```

## Notes

### Memoization Requirements

- All new sub-components should use `React.memo`
- Handlers passed to children should use `useCallback`
- Computed values should use `useMemo` when expensive
- Zustand object selectors should use `useShallow`

### Naming Conventions

- Hooks: `use{Feature}{Purpose}.ts` (e.g., `useJobEditPageForm.ts`)
- Utilities: `{verb}{Noun}.ts` (e.g., `mapJobToFormData.ts`)
- Components: `{Feature}{Section}.tsx` (e.g., `JobBasicInfoFields.tsx`)
```

### Step 4: Display Success Message

```
✅ [frontend-architect] Planning complete.

═══════════════════════════════════════════════════
            PLAN CREATED SUCCESSFULLY
═══════════════════════════════════════════════════

Plan saved to: {plan_file_path}

Original: {lines} lines → Target: {target_lines} lines
Extractions: {count} hooks, {count} utils, {count} components

═══════════════════════════════════════════════════
              SUGGESTED NEXT STEPS
═══════════════════════════════════════════════════

To implement this refactoring plan, run:

  /dev:implement {plan_file_path}

This will execute the step-by-step tasks from your plan.

═══════════════════════════════════════════════════
```

## Report

Return exclusively the path to the plan file created.
