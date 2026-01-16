# Feature Planning

Create a comprehensive plan for implementing a new feature. This command creates a plan document only - it does NOT implement any code.

## Arguments

- `$ARGUMENTS` - Feature description (text) or path to prompt file

## Configuration

Load project configuration from `.claude/frontend-dev-toolkit.json` to determine:
- Tech stack (which skills to load)
- Project paths
- Package manager
- Validation commands

## ⛔ CRITICAL: PLANNING ONLY - NO IMPLEMENTATION

**This command creates a PLAN only. You MUST NOT implement any changes.**

### Forbidden Actions
- ❌ DO NOT edit any source files (only create the plan file)
- ❌ DO NOT implement the feature
- ❌ DO NOT modify any code
- ❌ DO NOT run implementation commands
- ❌ DO NOT create components, hooks, or any feature code

### Required Actions
- ✅ Research and analyze the feature requirements
- ✅ Design the architecture and component structure
- ✅ Create the plan file in the specs directory
- ✅ Display the "PLAN CREATED SUCCESSFULLY" message
- ✅ Suggest running `/dev:implement {plan_path}` for implementation
- ✅ STOP after showing the suggested next steps

### Workflow Enforcement
```
/dev:feature → Creates plan file → STOPS → User reviews plan → User runs /dev:implement
```

**If you implement ANY code changes after creating the plan, you have violated this command's purpose.**

## Agent Invocation

Before starting the planning process, print this announcement:

```
═══════════════════════════════════════════════════
🚀 Invoking [frontend-architect] agent...
   └─ Task: Feature Planning
   └─ Model: opus
═══════════════════════════════════════════════════
```

Then apply the frontend-architect agent's principles throughout this planning process:
- Print `🏗️  [frontend-architect] Starting architectural planning...` when beginning
- Print `📚 [frontend-architect] Loading skill: {skill-name}` when referencing skills
- Print `📍 [frontend-architect] Analyzing: {file-or-pattern}` when researching codebase
- Print `✅ [frontend-architect] Planning complete.` when finished

## Instructions

### Step 1: Load Configuration

Read `.claude/frontend-dev-toolkit.json` to get project settings:

```javascript
const config = JSON.parse(fs.readFileSync('.claude/frontend-dev-toolkit.json'));
const specsPath = config.paths.specs || '.claude/specs';
const srcPath = config.paths.src || 'src';
```

### Step 2: Load Relevant Skills

Based on `config.techStack`, load the appropriate skills:

**Always load (core):**
- `react-guidelines`
- `typescript-standards`
- `tailwind-patterns`

**Conditionally load (optional):**
- `tanstack-query` if dataFetching includes 'tanstack-query'
- `zod-validation` if validation includes 'zod'
- `zustand-state` if stateManagement includes 'zustand'
- `react-router` if routing includes 'react-router'
- `react-forms` if working with forms
- `react-performance` if performance-critical feature

Print skill loading:
```
📚 [frontend-architect] Loading skill: react-guidelines (core)
📚 [frontend-architect] Loading skill: typescript-standards (core)
📚 [frontend-architect] Loading skill: tanstack-query (optional)
```

### Step 3: Parse Input

**If $ARGUMENTS is a file path (ends with .md or starts with ./):**
- Read the file and extract feature information
- Look for XML tags: `<objective>`, `<user_story>`, `<requirements>`, `<constraints>`

**If $ARGUMENTS is text:**
- Use it directly as the feature description

### Step 4: Research Codebase

Before planning, explore the codebase:

```
📍 [frontend-architect] Analyzing: project structure
📍 [frontend-architect] Analyzing: existing patterns in {srcPath}/features/
📍 [frontend-architect] Analyzing: similar implementations
```

1. Read project README if exists
2. Check existing patterns in `{srcPath}/features/` or `{srcPath}/components/`
3. Identify similar implementations for reference
4. Note any relevant utilities or hooks

### Step 5: Create Plan Document

Create the plan file at `{specsPath}/feature-{descriptive-name}.md`:

```markdown
# Feature: {Feature Name}

## Metadata

- **Type:** Feature
- **Created:** {YYYY-MM-DD}
- **Status:** Planning
- **Tech Stack:** {from config}

## Feature Description

{Detailed description of the feature, its purpose, and value to users}

## User Story

As a {type of user}
I want to {action/goal}
So that {benefit/value}

## Problem Statement

{What problem does this feature solve?}

## Solution Statement

{How will this feature solve the problem?}

## Performance Architecture

**CRITICAL: Design for render isolation BEFORE implementation.**

### State Location Rules

| State Type | Location | Why |
|------------|----------|-----|
| Modal open/close | Zustand store | Prevents parent re-renders |
| Selection state | Zustand store | Prevents props drilling |
| URL filters | useSearchParams | URL sync |
| Server data | TanStack Query | Automatic caching |

### Component Hierarchy

```
{FeatureName}/
├── {FeatureName}View.tsx          # Orchestrator
├── components/
│   ├── {FeatureName}Header.tsx    # React.memo wrapped
│   ├── {FeatureName}Content.tsx   # React.memo wrapped
│   └── {FeatureName}Modals.tsx    # Isolated, reads from Zustand
├── hooks/
│   └── use{FeatureName}.ts
├── stores/
│   └── use{FeatureName}Store.ts   # Modal/selection state
├── api/
│   ├── schema.ts                  # Zod schemas
│   ├── queries.ts                 # Query definitions
│   └── mutations.ts               # Mutation definitions
└── types/
    └── index.ts
```

### State Ownership Map

| State | Location | Subscribers | Re-render Scope |
|-------|----------|-------------|-----------------|
| {state name} | {location} | {components} | {scope} |

### Memoization Plan

- [ ] `Component` → `React.memo` (receives stable props)
- [ ] `handler` → `useCallback` (passed to memoized child)
- [ ] `computedValue` → `useMemo` (expensive computation)
- [ ] `storeSelector` → `useShallow` (Zustand object selector)

## Relevant Files

### Existing Files to Reference
- {path/to/file} - {why it's relevant}

### New Files to Create
- {path/to/new/file} - {purpose}

## Implementation Plan

### Phase 1: Foundation
{Setup and foundational work}

### Phase 2: Core Implementation
{Main feature implementation}

### Phase 3: Integration
{Connecting with existing code}

## Step by Step Tasks

IMPORTANT: Execute every step in order, top to bottom.

### 1. Setup Feature Structure
- Create feature directory at `{srcPath}/features/{feature-name}/`
- Create subdirectories: `api/`, `components/`, `hooks/`, `stores/`, `types/`

### 2. Define Types and Schemas
- Create TypeScript interfaces in `types/index.ts`
- Create Zod schemas in `api/schema.ts`

### 3. Create Zustand Store (if modals/selection)
- Create store with modal state and actions
- Export focused selector hooks with `useShallow`

### 4. Implement API Layer
- Create query definitions in `api/queries.ts`
- Create mutation definitions in `api/mutations.ts`

### 5. Build Components
- Create main view component
- Create child components with `React.memo`
- Use `useCallback` for handlers passed to children
- Add loading and error states with Suspense

### 6. Add Routing (if applicable)
- Add route in router configuration
- Create lazy-loaded route component

### 7. Validate Implementation
- Run type checking
- Run linting
- Run build

## Testing Strategy

### Unit Tests
- {Component/hook} should {behavior}

### Edge Cases
- {Edge case description}

## Acceptance Criteria

- [ ] {Criterion 1}
- [ ] {Criterion 2}
- [ ] {Criterion 3}

## Validation Commands

Execute these commands to validate the implementation:

```bash
{config.commands.typeCheck}
{config.commands.lint}
{config.commands.build}
```

## Notes

{Additional considerations, future improvements, technical debt}
```

### Step 6: Display Success Message

```
✅ [frontend-architect] Planning complete.

═══════════════════════════════════════════════════
            PLAN CREATED SUCCESSFULLY
═══════════════════════════════════════════════════

Plan saved to: {plan_file_path}

═══════════════════════════════════════════════════
              SUGGESTED NEXT STEPS
═══════════════════════════════════════════════════

To implement this feature plan, run:

  /dev:implement {plan_file_path}

This will execute the step-by-step tasks from your plan.

═══════════════════════════════════════════════════
```

## Report

Return exclusively the path to the plan file created.
