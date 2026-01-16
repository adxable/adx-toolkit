# Resolve Git Conflicts

Resolve all git conflicts in the current rebase or merge operation. This command keeps changes from the target branch and integrates your feature changes on top, then performs comprehensive verification.

## Prerequisites

- Active rebase or merge with conflicts
- Working directory is the git repository root or subdirectory

## Configuration

Load project configuration from `.claude/frontend-dev-toolkit.json`.

## Agent Invocation

Before starting, print this announcement:

```
═══════════════════════════════════════════════════
🔧 Invoking [conflict-resolver] agent...
   └─ Task: Git Conflict Resolution
   └─ Model: opus
═══════════════════════════════════════════════════
```

Print progress:
- Print `🔍 [conflict-resolver] Detecting conflict state...` when starting
- Print `📄 [conflict-resolver] Resolving: {file}` for each file
- Print `✅ [conflict-resolver] Conflict resolved: {file}` when done with file
- Print `🔄 [conflict-resolver] Running verification...` before verification
- Print `✅ [conflict-resolver] All conflicts resolved.` when finished

## Instructions

### Step 1: Detect Conflict State

```
🔍 [conflict-resolver] Detecting conflict state...
```

```bash
git status
```

Determine which operation is in progress:
- **Rebase**: Look for "interactive rebase in progress" or "rebase in progress"
- **Merge**: Look for "You have unmerged paths"

If no conflict state detected, inform the user and exit.

### Step 2: List Conflicted Files

```bash
git diff --name-only --diff-filter=U
```

### Step 3: Resolve Each Conflicted File

For each conflicted file:

```
📄 [conflict-resolver] Resolving: {file}
```

1. **Read the file** to see the conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`)

2. **Analyze the conflict**:
   - `<<<<<<< HEAD` section: Changes from target branch (main)
   - `=======` divider
   - `>>>>>>> [branch/commit]` section: Your feature changes

3. **Resolution Strategy** (integrate both changes):
   - If the conflict is about **removing vs keeping code**:
     - Keep the removal if your branch intentionally deleted it
     - Keep the code if your branch needs it for features
   - If the conflict is about **different implementations**:
     - Prefer your feature branch's implementation
     - Ensure any new dependencies from main are preserved
   - If the conflict is about **imports or dependencies**:
     - Keep imports that are actually used in the final code
     - Remove imports that reference deleted code

4. **Edit the file** to remove conflict markers and produce the correct merged result

5. **Verify** the file has no remaining conflict markers

```
✅ [conflict-resolver] Conflict resolved: {file}
```

### Step 4: Initial Verification

```
🔄 [conflict-resolver] Running verification...
```

After resolving all conflicts:

```bash
# Type check the resolved files
{config.commands.typeCheck}

# Lint the resolved files
{config.commands.lint}
```

Fix any TypeScript or ESLint errors introduced by the resolution.

### Step 5: Stage and Continue

```bash
# Stage all resolved files
git add {resolved-files}

# Continue the rebase or complete the merge
git rebase --continue
# OR
git commit  # for merge
```

### Step 6: Post-Resolution Verification

**CRITICAL**: After the rebase/merge completes, perform comprehensive verification.

#### 6.1 Identify Related Files

For each resolved file, identify related files that may need verification:

1. **Component files**: Find parent components that use the resolved component
2. **Interface/Type files**: Check if props/types are consistent
3. **Store files**: Verify store exports match imports
4. **Hook files**: Check custom hooks used by resolved files

#### 6.2 Verify Component Props Match Interfaces

For each resolved React component file:

1. **Read the component's interface definition** (the Props interface)
2. **Find all usages of the component** in other files
3. **Verify each usage passes only valid props**

Common issues to check:
- Props renamed during conflict resolution
- Props removed but still being passed
- New required props not being passed

#### 6.3 Verify Imports Are Valid

Check that all imports in resolved files reference existing exports:

1. **Read each import statement**
2. **Verify the imported module exists**
3. **Verify the imported export exists in that module**

#### 6.4 Run Full Validation Suite

```bash
# Full TypeScript check
{config.commands.typeCheck}

# Lint all affected files
{config.commands.lint}

# Production build
{config.commands.build}
```

### Step 7: Final State Check

```bash
git status
git log --oneline -3
```

Confirm the operation completed successfully.

## Resolution Guidelines

### Feature Branch Conflicts

When your branch adds new features:
- Keep main's existing functionality
- Add your new features on top
- Ensure both work together

### Cleanup Branch Conflicts

When your branch removes code:
- Keep your cleanup changes
- Prefer navigation-based handlers over modal handlers (if removing modals)
- Prefer simpler implementations

### Import Conflicts

- Remove imports for deleted files/functions
- Keep imports for code that still exists
- Add any new imports needed by your changes

### Common Prop Naming Conflicts

Watch for these common patterns where naming differs:

| Pattern | Main Branch | Feature Branch | Resolution |
|---------|-------------|----------------|------------|
| View handler | `onView` | `onEdit` | Check component interface |
| Create handler | `onCreate` | `onAdd` | Check component interface |
| Modal opener | `openModal` | `handleClick` | Check if modals were removed |

## Report

After successful conflict resolution AND verification, display:

```
✅ [conflict-resolver] All conflicts resolved.

═══════════════════════════════════════════════════
            CONFLICTS RESOLVED SUCCESSFULLY
═══════════════════════════════════════════════════

Resolved files:
  • {file1}
  • {file2}

Operation completed: {rebase/merge}

═══════════════════════════════════════════════════
          POST-RESOLUTION VERIFICATION
═══════════════════════════════════════════════════

Verified:
✅ All component props match interfaces
✅ All imports reference valid exports
✅ TypeScript check passed
✅ ESLint check passed
✅ Production build succeeded

{If fixes were made:}
Fixed issues:
- {file}: Changed {old} to {new} (reason)

═══════════════════════════════════════════════════
                 NEXT STEPS
═══════════════════════════════════════════════════

1. Review the changes: git log --oneline -5
2. Test your application manually
3. Push when ready: git push origin {branch} --force-with-lease

═══════════════════════════════════════════════════
```

## Checklist

Before marking resolution complete, verify:

- [ ] No conflict markers remain in any file
- [ ] All component usages pass valid props only
- [ ] All imports reference existing files/exports
- [ ] TypeScript compilation passes
- [ ] ESLint passes
- [ ] Production build succeeds
