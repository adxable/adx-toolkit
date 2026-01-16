# Implement Plan

Execute a plan document step-by-step. This command reads a plan file and implements each task in order.

## Arguments

- `$ARGUMENTS` - Path to the plan file (e.g., `.claude/specs/feature-user-auth.md`)

## Configuration

Load project configuration from `.claude/frontend-dev-toolkit.json`.

## Agent Invocation

Before starting implementation, print this announcement:

```
═══════════════════════════════════════════════════
🚀 Invoking [react-developer] agent...
   └─ Task: Implementation
   └─ Model: sonnet
   └─ Plan: {plan_file_path}
═══════════════════════════════════════════════════
```

Then apply the react-developer agent's principles throughout implementation:
- Print `⚛️  [react-developer] Starting implementation...` when beginning
- Print `📚 [react-developer] Loading skill: {skill-name}` when referencing skills
- Print `📄 [react-developer] Creating: {file-path}` when creating files
- Print `✏️  [react-developer] Editing: {file-path}` when editing files
- Print `✅ [react-developer] Implementation complete.` when finished

### Specialist Agents (invoke as needed)

During implementation, if you encounter specific needs, invoke specialist agents:

**For TypeScript errors or complex type work:**
```
═══════════════════════════════════════════════════
🚀 Invoking [typescript-expert] agent...
   └─ Task: Type Error Resolution
   └─ Model: sonnet
═══════════════════════════════════════════════════
```
Print `📘 [typescript-expert] Analyzing types...` when starting.
Print `🔧 [typescript-expert] Fixing: {error-description}` when fixing.
Print `✅ [typescript-expert] Type issues resolved.` when done.

**For styling work:**
```
═══════════════════════════════════════════════════
🚀 Invoking [ui-stylist] agent...
   └─ Task: Component Styling
   └─ Model: sonnet
═══════════════════════════════════════════════════
```
Print `🎨 [ui-stylist] Starting styling work...` when starting.
Print `✨ [ui-stylist] Styling: {component-name}` when styling.
Print `✅ [ui-stylist] Styling complete.` when done.

**For codebase exploration:**
```
═══════════════════════════════════════════════════
🚀 Invoking [explorer] agent...
   └─ Task: Codebase Search
   └─ Model: haiku
═══════════════════════════════════════════════════
```
Print `🔍 [explorer] Searching codebase...` when starting.
Print `📍 [explorer] Found: {description}` when finding results.
Print `✅ [explorer] Search complete.` when done.

**For debugging or finding solutions online:**
```
═══════════════════════════════════════════════════
🚀 Invoking [web-research-specialist] agent...
   └─ Task: Research & Debugging
   └─ Model: sonnet
═══════════════════════════════════════════════════
```
Print `🌐 [web-research-specialist] Starting research...` when starting.
Print `📚 [web-research-specialist] Found: {source-description}` when finding sources.
Print `✅ [web-research-specialist] Research complete.` when done.

## Instructions

### Step 1: Load and Validate Plan

Read the plan file from `$ARGUMENTS`:

```
⚛️  [react-developer] Starting implementation...
```

Parse the plan to extract:
- Feature/Bug/Chore name
- Step by step tasks
- Relevant files
- Validation commands
- Acceptance criteria

### Step 2: Display Implementation Overview

```
═══════════════════════════════════════════════════
           IMPLEMENTATION OVERVIEW
═══════════════════════════════════════════════════

Plan: {plan name}
Type: {Feature/Bug/Chore}
Tasks: {number of tasks}

Steps to implement:
1. {Task 1 summary}
2. {Task 2 summary}
3. {Task 3 summary}
...

═══════════════════════════════════════════════════
```

### Step 3: Execute Tasks Sequentially

For each task in the "Step by Step Tasks" section:

1. **Announce the task:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Task {N}/{Total}: {Task Title}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

2. **Load relevant skills** for the task type:
   - Creating components → `react-guidelines`
   - Adding types → `typescript-standards`
   - Styling → `tailwind-patterns`
   - Data fetching → `tanstack-query`
   - Form validation → `zod-validation`, `react-forms`
   - Performance → `react-performance`

3. **Read relevant files** mentioned in the task

4. **Implement the changes** following:
   - Project patterns from loaded skills
   - Tech stack from configuration
   - Existing code conventions

5. **Invoke specialist agents** as needed:
   - TypeScript errors → invoke `typescript-expert`
   - Complex styling → invoke `ui-stylist`
   - Need to find patterns → invoke `explorer`
   - Stuck on issue → invoke `web-research-specialist`

6. **Verify after each task:**
   - Run type check if TypeScript files changed
   - Ensure no obvious errors

7. **Mark task complete:**
```
✅ Task {N} complete: {brief summary of changes}
```

### Step 4: Run Validation Commands

After all tasks complete, run validation from the plan:

```
═══════════════════════════════════════════════════
           RUNNING VALIDATION
═══════════════════════════════════════════════════
```

Execute each validation command:
- Type checking
- Linting
- Build

If validation fails:
1. Identify the error
2. Invoke appropriate specialist agent if needed
3. Fix the issue
4. Re-run validation
5. Continue until all pass

### Step 5: Verify Acceptance Criteria

Check each acceptance criterion from the plan:

```
═══════════════════════════════════════════════════
         ACCEPTANCE CRITERIA CHECK
═══════════════════════════════════════════════════

✅ {Criterion 1} - Verified
✅ {Criterion 2} - Verified
⚠️ {Criterion 3} - Needs manual verification
```

### Step 6: Display Completion Summary

```
✅ [react-developer] Implementation complete.

═══════════════════════════════════════════════════
         IMPLEMENTATION COMPLETE
═══════════════════════════════════════════════════

Plan: {plan name}

Files Created:
  • {path/to/file1.tsx}
  • {path/to/file2.ts}

Files Modified:
  • {path/to/existing1.tsx}
  • {path/to/existing2.ts}

Validation Results:
  ✅ Type Check: Passed
  ✅ Lint: Passed
  ✅ Build: Passed

Acceptance Criteria: {X}/{Y} verified

═══════════════════════════════════════════════════
              SUGGESTED NEXT STEPS
═══════════════════════════════════════════════════

1. SIMPLIFY CODE (recommended - removes over-engineering):
   /dev:simplify

2. VERIFY CHANGES (type-check + lint + build):
   /verify

3. CODE REVIEW:
   /review

4. CREATE COMMIT:
   /utils:commit

5. CREATE PR:
   /utils:pr

═══════════════════════════════════════════════════
```

## Implementation Guidelines

### Follow Existing Patterns

- Check similar components in the codebase
- Match naming conventions
- Use existing utilities and helpers
- Follow the project's code style

### Quality Standards

- No `any` types in TypeScript
- Proper error handling
- Accessibility considerations
- Performance optimization (memoization where needed)

### Code Organization

- One component per file
- Hooks in dedicated files
- Types in dedicated files
- Keep files focused and small

### When to Invoke Specialist Agents

| Situation | Agent to Invoke |
|-----------|-----------------|
| TypeScript compilation errors | typescript-expert |
| Complex generic types needed | typescript-expert |
| Styling complex layouts | ui-stylist |
| Animation implementation | ui-stylist |
| Finding similar patterns | explorer |
| Locating implementations | explorer |
| Debugging strange errors | web-research-specialist |
| Finding best practices | web-research-specialist |

## Error Handling

If implementation encounters errors:

1. **Type errors:** Invoke `typescript-expert`, fix immediately
2. **Lint errors:** Fix or disable with explanation
3. **Build errors:** Must resolve before completing
4. **Missing dependencies:** Install and document
5. **Stuck on issue:** Invoke `web-research-specialist`

## Report

Return a summary of:
- Tasks completed
- Files created/modified
- Agents invoked during implementation
- Validation results
- Any manual steps needed
