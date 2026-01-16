# Code Simplifier

Analyze and simplify recently implemented code. Removes over-engineering, unnecessary abstractions, and complexity while maintaining functionality. Runs verification loop after each simplification.

## Arguments

- `$ARGUMENTS` - Optional: specific file paths to simplify, or "branch" to simplify all changes on current branch

## Configuration

Load project configuration from `.claude/frontend-dev-toolkit.json`.

## Agent Invocation

Before starting, print this announcement:

```
═══════════════════════════════════════════════════
🧹 Invoking [code-simplifier] agent...
   └─ Task: Code Simplification
   └─ Model: opus
   └─ Branch: {current-branch}
═══════════════════════════════════════════════════
```

Print progress:
- Print `🔍 [code-simplifier] Analyzing files for simplification opportunities...` when starting
- Print `🎯 [code-simplifier] Found: {issue}` when finding issues
- Print `✂️  [code-simplifier] Simplifying: {file}` when making changes
- Print `✅ [code-simplifier] Simplification complete.` when finished

## Core Principles

**YAGNI** - You Aren't Gonna Need It
**KISS** - Keep It Simple, Stupid
**DRY** - Don't Repeat Yourself (but don't over-abstract either)

## Instructions

### Phase 1: Identify Code to Simplify

```
🔍 [code-simplifier] Analyzing files for simplification opportunities...
```

**If $ARGUMENTS contains file paths:**
- Simplify only the specified files

**If $ARGUMENTS is "branch" or empty:**
- Get changed files on current branch:
```bash
git diff main...HEAD --name-only | grep -E '\.(tsx?|jsx?)$'
```

### Phase 2: Analyze for Simplification Opportunities

For each file, look for:

**Complexity Issues:**
1. Functions > 30 lines
2. Components > 150 lines
3. Nesting depth > 3 levels
4. Too many parameters (> 4)

**Over-Abstraction:**
1. Single-use utilities/helpers
2. Wrapper components that just pass props
3. Unnecessary custom hooks (< 3 uses)
4. Premature abstractions
5. Indirection without benefit

**Dead Code:**
1. Unused imports
2. Unused variables
3. Unreachable code
4. Commented-out code blocks
5. Unused functions/components

Print findings:
```
🎯 [code-simplifier] Found: {issue description} in {file}:{line}
```

### Phase 3: Display Simplification Opportunities

```
═══════════════════════════════════════════════════
         SIMPLIFICATION OPPORTUNITIES
═══════════════════════════════════════════════════

🔴 High Priority (will simplify):
- {file}:{line} - {issue}

🟡 Medium Priority (will simplify):
- {file}:{line} - {issue}

🔵 Low Priority (optional):
- {file}:{line} - {issue}

Total: {N} simplifications to apply
═══════════════════════════════════════════════════
```

### Phase 4: Apply Simplifications (with Verification Loop)

For each simplification (high → medium priority):

```
✂️  [code-simplifier] Simplifying: {file}
```

**Simplification Patterns:**

#### Pattern 1: Inline Single-Use Functions
```typescript
// BEFORE
const formatName = (name: string) => name.toUpperCase();
const result = formatName(user.name);

// AFTER
const result = user.name.toUpperCase();
```

#### Pattern 2: Remove Unnecessary Wrappers
```typescript
// BEFORE
const MyWrapper = ({ children }: { children: ReactNode }) => (
  <div>{children}</div>
);

// AFTER (just use div directly or remove if no styling)
```

#### Pattern 3: Simplify Conditionals
```typescript
// BEFORE
if (condition) {
  return true;
} else {
  return false;
}

// AFTER
return condition;
```

#### Pattern 4: Flatten Nested Callbacks
```typescript
// BEFORE (if only used once and not passed to memoized child)
const handleClick = useCallback(() => {
  doSomething();
}, []);

// AFTER
const handleClick = () => doSomething();
```

#### Pattern 5: Remove Premature Memoization
```typescript
// BEFORE (if value is cheap to compute)
const value = useMemo(() => items.length, [items]);

// AFTER
const value = items.length;
```

#### Pattern 6: Consolidate State
```typescript
// BEFORE
const [firstName, setFirstName] = useState('');
const [lastName, setLastName] = useState('');

// AFTER (if always updated together)
const [name, setName] = useState({ first: '', last: '' });
```

### Phase 5: Verification Loop

After applying simplifications, run verification:

```bash
# Quick check after each simplification
{config.commands.typeCheck}

# Full verification after all simplifications
{config.commands.typeCheck} && {config.commands.lint} && {config.commands.build}
```

**If verification fails:**
1. Identify the breaking simplification
2. Revert that specific change
3. Continue with remaining simplifications
4. Re-run verification

**Loop until:**
- All high/medium priority simplifications applied OR reverted
- Full verification passes

### Phase 6: Summary Report

```
✅ [code-simplifier] Simplification complete.

═══════════════════════════════════════════════════
         CODE SIMPLIFICATION COMPLETE
═══════════════════════════════════════════════════

Applied Simplifications:
✅ {file}:{line} - {description}
✅ {file}:{line} - {description}

Reverted (broke verification):
⏪ {file}:{line} - {description}

Skipped (low priority):
⏭️  {file}:{line} - {description}

Metrics:
- Lines removed: {N}
- Files simplified: {N}

Verification:
✓ Type Check: Passed
✓ ESLint: Passed
✓ Build: Passed

═══════════════════════════════════════════════════
              SUGGESTED NEXT STEPS
═══════════════════════════════════════════════════

1. VERIFY IN BROWSER:
   /verify

2. REVIEW CHANGES:
   git diff --stat

3. COMMIT SIMPLIFICATIONS:
   /utils:commit

═══════════════════════════════════════════════════
```

## Simplification Rules

### DO Simplify:
- Single-use helper functions → inline them
- Wrapper components that just pass props → remove them
- Unused imports and variables → delete them
- Overly generic utilities → make them specific
- Premature optimizations → remove unless proven needed
- Complex conditionals → simplify logic
- Deeply nested code → flatten structure

### DO NOT Simplify:
- Shared utilities used in 3+ places
- Performance-critical memoization (proven with profiling)
- Error boundaries and fallbacks
- Accessibility features
- Type safety abstractions
- Code that follows established patterns in codebase

### Safety Checks:
- Never remove error handling
- Never remove loading/empty states
- Never inline security-related code
- Never simplify API layer abstractions
- Always verify after each change

## Integration with /dev:implement

This command is designed to run after `/dev:implement`:

```
/dev:feature "Add user profile page"
    ↓
/dev:implement {plan_path}
    ↓
/dev:simplify                    ← Simplify all implementation changes
    ↓
/verify                          ← Verify everything works
    ↓
/utils:commit                    ← Commit clean, simple code
```

## Report

Return a summary of:
- Simplifications applied
- Lines removed
- Files modified
- Verification results
