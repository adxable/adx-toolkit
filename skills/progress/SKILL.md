# Progress Skill

Show current project progress and state.

## Instructions

Read and display the current project state from `.claude/state/STATE.md`.

**Steps:**
1. Read `.claude/state/STATE.md` if it exists
2. Display a concise summary:
   - Current phase and task
   - Recent work completed
   - Next steps
   - Any blockers

If STATE.md doesn't exist, inform the user that state tracking isn't set up for this project and offer to create it.

## Output Format

```
## Current Progress

**Phase:** [phase name]
**Task:** [current task]
**Last Updated:** [date]

### Recent Work
- [bullet points of recent work]

### Next Steps
1. [next steps]

### Blockers
- [any blockers or "None"]
```

## Related Files

- `.claude/state/STATE.md` - Current state
- `.claude/state/ROADMAP.md` - Project roadmap
- `.claude/state/REQUIREMENTS.md` - Requirements
- `.claude/state/PROJECT.md` - Project overview
