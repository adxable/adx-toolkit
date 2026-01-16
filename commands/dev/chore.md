# Chore Planning

Create a plan for maintenance, refactoring, or technical debt work. This command creates a plan document only - it does NOT implement any changes.

## Arguments

- `$ARGUMENTS` - Description of the maintenance task

## Configuration

Load project configuration from `.claude/frontend-dev-toolkit.json`.

## ⛔ CRITICAL: PLANNING ONLY - NO IMPLEMENTATION

**This command creates a PLAN only. You MUST NOT implement any changes.**

### Forbidden Actions
- ❌ DO NOT edit any source files (only create the plan file)
- ❌ DO NOT complete the chore
- ❌ DO NOT modify any code
- ❌ DO NOT run implementation commands

### Required Actions
- ✅ Research and analyze the chore requirements
- ✅ Create the plan file in the specs directory
- ✅ Display the "PLAN CREATED SUCCESSFULLY" message
- ✅ Suggest running `/dev:implement {plan_path}` for implementation
- ✅ STOP after showing the suggested next steps

### Workflow Enforcement
```
/dev:chore → Creates plan file → STOPS → User reviews plan → User runs /dev:implement
```

## Agent Invocation

Before starting the planning process, print this announcement:

```
═══════════════════════════════════════════════════
🚀 Invoking [frontend-architect] agent...
   └─ Task: Chore Planning
   └─ Model: opus
═══════════════════════════════════════════════════
```

Then apply the frontend-architect agent's principles:
- Print `🏗️  [frontend-architect] Starting chore planning...` when beginning
- Print `📚 [frontend-architect] Loading skill: {skill-name}` when referencing skills
- Print `📍 [frontend-architect] Analyzing: {area}` when researching
- Print `✅ [frontend-architect] Planning complete.` when finished

## Instructions

### Step 1: Load Configuration

Read `.claude/frontend-dev-toolkit.json` to get project settings.

### Step 2: Analyze the Chore

```
🏗️  [frontend-architect] Starting chore planning...
```

Based on `$ARGUMENTS`, determine the type:
- **Refactoring:** Code restructuring without behavior change
- **Dependency Update:** Updating packages
- **Technical Debt:** Addressing known issues
- **Configuration:** Build/tooling changes
- **Documentation:** Updating docs
- **Cleanup:** Removing dead code

### Step 3: Research Impact

```
📍 [frontend-architect] Analyzing: {affected area}
```

1. Identify affected files
2. Check for dependencies on affected code
3. Assess risk level
4. Identify testing requirements

### Step 4: Create Chore Plan

Create the plan file at `{specsPath}/chore-{descriptive-name}.md`:

```markdown
# Chore: {Chore Title}

## Metadata

- **Type:** Chore
- **Category:** {Refactoring/Dependency/TechDebt/Config/Docs/Cleanup}
- **Created:** {YYYY-MM-DD}
- **Status:** Planning
- **Risk Level:** {Low/Medium/High}

## Description

{What needs to be done and why}

## Motivation

{Why is this chore necessary?}

- {Reason 1}
- {Reason 2}

## Scope

### In Scope
- {What will be changed}

### Out of Scope
- {What will NOT be changed}

## Relevant Files

### Files to Modify
- {path/to/file} - {what will change}

### Files to Reference
- {path/to/file} - {why it's relevant}

## Performance Architecture (if refactoring views)

**Include this section if the chore involves refactoring views with tables/filters/modals.**

### State Location Rules

| State Type | Required Location | Why |
|------------|-------------------|-----|
| Modal open/close | Zustand store | Prevents parent re-renders |
| Selection state | Zustand store | Prevents props drilling |
| URL filters | useSearchParams | URL sync |

### Memoization Requirements

- All split components: `React.memo`
- All handlers passed to children: `useCallback`
- All Zustand object selectors: `useShallow`

## Step by Step Tasks

IMPORTANT: Execute every step in order, top to bottom.

### 1. {First Task}
- {Specific action}

### 2. {Second Task}
- {Specific action}

### 3. Validate Changes
- Run type checking
- Run linting
- Run build

## Risk Assessment

### Potential Issues
- {Risk 1} - Mitigation: {how to handle}

### Rollback Plan
{How to revert if something goes wrong}

## Testing Strategy

- {How to verify the chore is complete}
- {How to ensure no regression}

## Validation Commands

```bash
{config.commands.typeCheck}
{config.commands.lint}
{config.commands.build}
```

## Acceptance Criteria

- [ ] {Criterion 1}
- [ ] {Criterion 2}
- [ ] No regression in existing functionality

## Notes

{Additional context}
```

### Step 5: Display Success Message

```
✅ [frontend-architect] Planning complete.

═══════════════════════════════════════════════════
            PLAN CREATED SUCCESSFULLY
═══════════════════════════════════════════════════

Plan saved to: {plan_file_path}

Category: {category}
Risk Level: {risk}
Files Affected: {count}

═══════════════════════════════════════════════════
              SUGGESTED NEXT STEPS
═══════════════════════════════════════════════════

To implement this chore, run:

  /dev:implement {plan_file_path}

This will execute the step-by-step tasks from your plan.

═══════════════════════════════════════════════════
```

## Report

Return exclusively the path to the plan file created.
