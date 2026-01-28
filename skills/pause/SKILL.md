# Pause Skill

Save current work context before closing the session.

## Instructions

Update `.claude/state/STATE.md` with the current session's progress.

**Steps:**
1. Read the current STATE.md
2. Update the following sections:
   - **Last Updated:** Set to today's date
   - **Recent Work (This Session):** Add bullet points of what was accomplished
   - **Files Recently Modified:** List files changed in this session
   - **Next Steps:** Update based on current progress
   - **Blockers:** Note any issues encountered

3. Ask the user if there's anything specific they want to note before closing

4. Write the updated STATE.md

5. Confirm with a brief summary:
   ```
   Session paused. Progress saved to STATE.md.

   To continue: Run /adx:resume or say "Continue from where I left off"
   ```

## Important

- Preserve existing content in STATE.md, only update relevant sections
- Be concise in descriptions
- Include specific file paths when listing modified files
- Don't overwrite decisions or project context unless explicitly asked
