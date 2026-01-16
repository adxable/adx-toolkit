# Patch Plan

Create a **focused patch plan** to resolve a specific issue. This command creates a concise plan with minimal, targeted changes.

## Arguments

- `$1` - Description of the issue to fix
- `$2` (optional) - Path to original specification file for context

## Configuration

Load project configuration from `.claude/frontend-dev-toolkit.json`.

## ⛔ CRITICAL: PLANNING ONLY - NO IMPLEMENTATION

**This command creates a PLAN only. You MUST NOT implement any changes.**

### Forbidden Actions
- ❌ DO NOT edit any source files (only create the patch plan file)
- ❌ DO NOT apply the patch
- ❌ DO NOT modify any code
- ❌ DO NOT make "quick fixes" even if they seem trivial

### Required Actions
- ✅ Analyze the issue and determine minimal changes needed
- ✅ Create the patch plan file in `.claude/specs/patch/`
- ✅ Display the "PATCH PLAN CREATED" message
- ✅ Suggest running `/dev:implement {plan_path}` for implementation
- ✅ STOP after showing the suggested next steps

### Workflow Enforcement
```
/dev:patch → Creates patch plan file → STOPS → User reviews plan → User runs /dev:implement
```

## Agent Invocation

Before starting the planning process, print this announcement:

```
═══════════════════════════════════════════════════
🚀 Invoking [frontend-architect] agent...
   └─ Task: Patch Planning
   └─ Model: opus
═══════════════════════════════════════════════════
```

Then apply the frontend-architect agent's principles:
- Print `🏗️  [frontend-architect] Starting patch analysis...` when beginning
- Print `🔍 [frontend-architect] Investigating: {area}` when researching
- Print `✅ [frontend-architect] Patch plan complete.` when finished

## Instructions

### Step 1: Analyze the Issue

```
🏗️  [frontend-architect] Starting patch analysis...
```

- Read the original specification at `$2` if provided
- Use `$1` (issue_description) as the basis for the patch
- Run `git diff --stat` to understand recent changes
- Identify the minimal set of changes required

### Step 2: Research Scope

```
🔍 [frontend-architect] Investigating: {affected area}
```

- Identify the specific files that need changes
- Keep the scope minimal - only fix what's described
- Think about the most efficient way to implement

### Step 3: Create Patch Plan

Create the patch plan file at `.claude/specs/patch/patch-{descriptive-name}.md`:

```markdown
# Patch: {concise patch title}

## Issue Summary

**Original Spec:** {spec_path if provided, otherwise "N/A"}
**Issue:** {brief description of the issue}
**Solution:** {brief description of the solution approach}

## Files to Modify

{list only the files that need changes - be specific and minimal}

- `{path/to/file}` - {what needs to change}

## Implementation Steps

IMPORTANT: Execute every step in order, top to bottom.

### Step 1: {specific action}

- {implementation detail}
- {implementation detail}

### Step 2: {specific action}

- {implementation detail}
- {implementation detail}

{continue as needed, but keep it minimal - typically 2-5 steps}

## Validation

Execute every command to validate the patch is complete with zero regressions.

{list 1-5 specific commands or checks to verify the patch works correctly}

```bash
{config.commands.typeCheck}
{config.commands.lint}
{config.commands.build}
```

## Patch Scope

**Lines of code to change:** {estimate}
**Risk level:** {low|medium|high}
**Testing required:** {brief description}
```

### Step 4: Display Success Message

```
✅ [frontend-architect] Patch plan complete.

═══════════════════════════════════════════════════
              PATCH PLAN CREATED
═══════════════════════════════════════════════════

Plan saved to: {patch_plan_file_path}

Scope: {brief scope description}
Risk Level: {risk}
Files Affected: {count}

═══════════════════════════════════════════════════
              SUGGESTED NEXT STEPS
═══════════════════════════════════════════════════

To implement this patch plan, run:

  /dev:implement {patch_plan_file_path}

This will execute the implementation steps from your patch plan.

═══════════════════════════════════════════════════
```

## Report

Return exclusively the path to the patch plan file created.
