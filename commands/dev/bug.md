# Bug Planning

Create a plan to resolve a bug. This command creates a plan document only - it does NOT fix any code.

## Arguments

- `$ARGUMENTS` - Bug description (text) or path to prompt file

## Configuration

Load project configuration from `.claude/frontend-dev-toolkit.json`.

## ⛔ CRITICAL: PLANNING ONLY - NO IMPLEMENTATION

**This command creates a PLAN only. You MUST NOT implement any changes.**

### Forbidden Actions
- ❌ DO NOT edit any source files (only create the plan file)
- ❌ DO NOT fix the bug
- ❌ DO NOT modify any code
- ❌ DO NOT run implementation commands
- ❌ DO NOT make "quick fixes" even if they seem obvious

### Required Actions
- ✅ Research and analyze the bug
- ✅ Identify root cause
- ✅ Create the plan file in the specs directory
- ✅ Display the "PLAN CREATED SUCCESSFULLY" message
- ✅ Suggest running `/dev:implement {plan_path}` for implementation
- ✅ STOP after showing the suggested next steps

### Workflow Enforcement
```
/dev:bug → Creates plan file → STOPS → User reviews plan → User runs /dev:implement
```

## Agent Invocation

Before starting the planning process, print this announcement:

```
═══════════════════════════════════════════════════
🚀 Invoking [frontend-architect] agent...
   └─ Task: Bug Analysis & Planning
   └─ Model: opus
═══════════════════════════════════════════════════
```

Then apply the frontend-architect agent's principles:
- Print `🏗️  [frontend-architect] Starting bug analysis...` when beginning
- Print `📚 [frontend-architect] Loading skill: {skill-name}` when referencing skills
- Print `🔍 [frontend-architect] Investigating: {area}` when researching
- Print `🎯 [frontend-architect] Root cause identified: {cause}` when found
- Print `✅ [frontend-architect] Planning complete.` when finished

## Instructions

### Step 1: Load Configuration

Read `.claude/frontend-dev-toolkit.json` to get project settings.

### Step 2: Parse Input

**If $ARGUMENTS is a file path:**
- Read the file and extract bug information
- Look for XML tags: `<problem_statement>`, `<reproduction_steps>`, `<expected_behavior>`

**If $ARGUMENTS is text:**
- Use it directly as the bug description

### Step 3: Investigate the Bug

```
🏗️  [frontend-architect] Starting bug analysis...
```

Based on the bug description:

1. **Search for related code:**
   ```
   🔍 [frontend-architect] Investigating: {component/area}
   ```
   - Find relevant files
   - Look for error messages, component names, function names

2. **Identify the affected area:**
   - Which component(s)?
   - Which feature?
   - Which data flow?

3. **Trace to root cause:**
   - Read the relevant code
   - Follow the data flow
   - Identify the actual cause

4. **Announce root cause:**
   ```
   🎯 [frontend-architect] Root cause identified: {brief cause}
   ```

### Step 4: Create Bug Fix Plan

Create the plan file at `{specsPath}/bug-{descriptive-name}.md`:

```markdown
# Bug Fix: {Bug Title}

## Metadata

- **Type:** Bug
- **Created:** {YYYY-MM-DD}
- **Status:** Planning
- **Severity:** {Critical/High/Medium/Low}

## Bug Description

{What is happening? Include error messages if applicable}

## Steps to Reproduce

1. {Step 1}
2. {Step 2}
3. {Step 3}

## Expected Behavior

{What should happen instead}

## Actual Behavior

{What is currently happening}

## Root Cause Analysis

### Investigation Findings

{What did you discover while investigating?}

### Root Cause

{What is causing the bug?}

### Affected Files

- `{path/to/file}:{line}` - {how it's affected}

## Solution Statement

{How the fix will solve the problem}

## Relevant Files

### Files to Modify
- {path/to/file} - {what needs to change}

### Files to Reference
- {path/to/file} - {why it's relevant}

## Step by Step Tasks

IMPORTANT: Execute every step in order, top to bottom.

### 1. {First Fix Step}
- {Specific change to make}

### 2. {Second Fix Step}
- {Specific change to make}

### 3. Validate Fix
- Run type checking
- Run linting
- Run build
- Verify bug is fixed

## Performance Considerations

**Will this fix introduce re-render risks?**
- [ ] No new state that could cascade re-renders
- [ ] No inline objects/functions passed to children
- [ ] Existing memoization patterns preserved

## Testing Strategy

### Bug Verification
- {How to verify the fix works}

### Regression Testing
- {What to check hasn't broken}

### Edge Cases
- {Edge case to test}

## Validation Commands

```bash
{config.commands.typeCheck}
{config.commands.lint}
{config.commands.build}
```

## Acceptance Criteria

- [ ] Bug no longer occurs
- [ ] No regression in related functionality
- [ ] All validation commands pass

## Notes

{Additional context, related issues, or considerations}
```

### Step 5: Display Success Message

```
✅ [frontend-architect] Planning complete.

═══════════════════════════════════════════════════
            PLAN CREATED SUCCESSFULLY
═══════════════════════════════════════════════════

Plan saved to: {plan_file_path}

Root Cause: {brief description}
Recommended Fix: {approach summary}

═══════════════════════════════════════════════════
              SUGGESTED NEXT STEPS
═══════════════════════════════════════════════════

To implement this bug fix, run:

  /dev:implement {plan_file_path}

This will execute the step-by-step tasks from your plan.

═══════════════════════════════════════════════════
```

## Report

Return exclusively the path to the plan file created.
