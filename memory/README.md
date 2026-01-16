# Memory System

This directory contains project context that Claude Code uses to maintain continuity across sessions.

## Files

| File | Purpose | Update Frequency |
|------|---------|------------------|
| `CLAUDE.md` | Main context file - project overview, stack, conventions | When project setup changes |
| `decisions.md` | Architecture Decision Records (ADRs) | When making significant decisions |
| `conventions.md` | Discovered code patterns and conventions | When patterns are established |
| `lessons.md` | What worked/didn't work, insights | After completing features or fixing issues |

## Usage

### For Plugin Users

1. Copy this `memory/` directory to your project's `.claude/memory/`
2. Fill in `CLAUDE.md` with your project specifics
3. Update other files as your project evolves

### Auto-Loading

The `CLAUDE.md` file should be placed at:
- Project root: `CLAUDE.md`
- Or: `.claude/CLAUDE.md`
- Or: `.claude/memory/CLAUDE.md`

Claude Code automatically reads `CLAUDE.md` from the project root.

### Best Practices

1. **Keep CLAUDE.md concise** - Focus on what Claude needs to know
2. **Log decisions promptly** - Don't let context get lost
3. **Update lessons regularly** - Capture insights while fresh
4. **Review periodically** - Remove outdated information

## Integration with Hooks

The session summary hook (`stop.py`) can automatically suggest updates to these files based on the session's work.
