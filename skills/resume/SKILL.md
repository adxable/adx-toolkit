# Resume Skill

Continue work from where the previous session left off.

## Instructions

Read the project state and prepare to continue work.

**Steps:**
1. Read `.claude/state/STATE.md`
2. Optionally read these for additional context:
   - `.claude/state/ROADMAP.md` - Overall roadmap
   - `.claude/state/PROJECT.md` - Project overview
   - Any plan files mentioned in STATE.md

3. Present a brief summary to the user:
   ```
   ## Resuming Session

   **Last session:** [date]
   **Current task:** [task name]

   ### Where we left off
   [brief description of last work]

   ### Ready to continue with
   [next steps from STATE.md]

   Shall I continue with [specific next task]?
   ```

4. Wait for user confirmation before proceeding with work

## Important

- Don't start working immediately - summarize and confirm first
- If STATE.md is missing or empty, inform the user and offer to help set up state tracking
- Reference specific plan files if they exist (e.g., `.claude/plans/plan-*.md`)
