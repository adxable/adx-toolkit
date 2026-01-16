# Frontend Dev Toolkit

A comprehensive Claude Code plugin for React/TypeScript frontend development workflows. Includes planning, implementation, verification, code review, intelligent hooks, context management, and MCP integrations.

## What's New in v2.0

- **Hooks System** - Python-based hooks for logging, smart context loading, and session management
- **Memory System** - Persistent context across sessions with CLAUDE.md and decision logs
- **Smart Context Loader** - Auto-detects work context and suggests relevant skills
- **Session Summaries** - Automatic summary generation on session end
- **MCP Integrations** - Pre-configured servers for Playwright, sequential-thinking, and more

## Features

- **Planning Commands** - Structured feature, bug, and chore planning
- **Implementation Commands** - Guided implementation from plans
- **Verification Commands** - Parallel type checking, linting, and build verification
- **Code Review Commands** - Automated code review with inline comments
- **Utility Commands** - Git commit, PR creation, and project utilities
- **Intelligent Hooks** - Context-aware assistance and session tracking
- **Memory System** - Maintain project knowledge across sessions

## Prerequisites

- Python 3.8+ (3.11+ recommended)
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer

```bash
# Install uv if not present
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Installation

```bash
# Copy plugin to your Claude plugins directory
cp -r frontend-dev-toolkit ~/.claude/plugins/

# Or symlink for development
ln -s /path/to/frontend-dev-toolkit ~/.claude/plugins/frontend-dev-toolkit
```

## Quick Start

1. **Copy configuration files to your project:**

```bash
# Copy settings.json to your project's .claude directory
cp settings.json /your-project/.claude/settings.json

# Copy MCP config
cp mcp.json /your-project/.claude/mcp.json

# Copy memory templates
cp -r memory/ /your-project/.claude/memory/

# Copy hooks
cp -r hooks/ /your-project/hooks/
```

2. **Run the setup command:**

```bash
/frontend-dev-toolkit:setup
```

3. **Fill in your CLAUDE.md:**

Edit `.claude/memory/CLAUDE.md` with your project's specifics.

---

## Commands

### Setup & Configuration

| Command | Description |
|---------|-------------|
| `/setup` | Interactive project setup - configures tech stack and paths |

### Development Workflow

| Command | Description |
|---------|-------------|
| `/dev:feature <description>` | Create a feature implementation plan |
| `/dev:bug <description>` | Create a bug fix plan |
| `/dev:chore <description>` | Create a maintenance/refactoring plan |
| `/dev:implement <plan-path>` | Implement a plan step-by-step |
| `/dev:refactor <target>` | Guided code refactoring |
| `/dev:simplify <scope>` | Remove over-engineering from code |
| `/dev:patch <description>` | Quick patch/hotfix |
| `/dev:resolve-conflicts` | Help resolve git merge conflicts |

### Verification

| Command | Description |
|---------|-------------|
| `/verify:verify [url]` | Run full verification loop (types, lint, build, browser) |
| `/verify:types` | Run TypeScript type checking |
| `/verify:lint` | Run ESLint |

### Code Review

| Command | Description |
|---------|-------------|
| `/review:review` | Full code review of branch changes |

### Utilities

| Command | Description |
|---------|-------------|
| `/utils:commit` | Generate and create git commit |
| `/utils:pr` | Create pull request with description |
| `/utils:clean-comments` | Remove [CR] review comments |

---

## Hooks System

The plugin includes Python-based hooks that enhance Claude Code functionality.

### Available Hooks

| Hook | Event | Description |
|------|-------|-------------|
| `smart_context_loader.py` | UserPromptSubmit | Auto-detects context and suggests skills |
| `skill-activation-prompt.py` | UserPromptSubmit | Triggers skills based on keywords |
| `user_prompt_submit.py` | UserPromptSubmit | Logs prompts, optional validation |
| `pre_tool_use.py` | PreToolUse | Logs tool usage before execution |
| `post_tool_use.py` | PostToolUse | Logs tool usage after execution |
| `stop.py` | Stop | Session summary generation |
| `subagent_stop.py` | SubagentStop | Subagent session logging |
| `notification.py` | Notification | Notification logging |
| `pre_compact.py` | PreCompact | Context compaction logging |

### Smart Context Loader

**How it works:** When you submit a prompt, the hook scans for keywords and regex patterns (e.g., "form", "validation", "create.*component"). Based on matches, it outputs a context panel suggesting which skills to load and provides relevant notes for your task.

**Example output:**
```
──────────────────────────────────────────────────
📋 SMART CONTEXT DETECTED
──────────────────────────────────────────────────

💡 Suggested Skills:
   → react-forms
   → zod-validation

📝 Context Notes:
   ❗ [FORMS] Form handling - consider validation, error states, and accessibility

──────────────────────────────────────────────────
```

| Detected Context | Suggested Skills |
|-----------------|------------------|
| Forms, validation | `react-forms`, `zod-validation` |
| API, data fetching | `tanstack-query` |
| Styling, UI | `tailwind-patterns`, `frontend-design` |
| Components | `react-guidelines`, `typescript-standards` |
| Performance | `react-performance` |
| TypeScript | `typescript-standards` |
| Testing | Testing context notes |
| Refactoring | `react-guidelines`, `typescript-standards` |

### Session Summaries

**How it works:** When a session ends (Stop hook), the transcript is parsed to extract key information. The hook analyzes all messages to identify user prompts, tool calls, file operations, and errors, then generates a summary for review and continuity.

**Generated files:**
- `logs/{session_id}/session_summary.txt` - Human-readable summary
- `logs/{session_id}/session_summary.json` - Structured data for programmatic access

**Example output:**
```
============================================================
SESSION SUMMARY
============================================================
Generated: 2025-01-16 15:30:45

## What Was Requested
  1. Implement hooks from Shiplex.Web.Frontend
  2. Add memory system and MCP configs
  3. Update README documentation

## Files Modified
  ✏️  hooks/stop.py
  ✏️  settings.json
  ✏️  README.md

## Tools Used
  Read, Write, Edit, Bash, Glob, Grep

## Statistics
  • Total messages: 47
  • Files modified: 15
  • Files read: 23
  • Commands run: 8
============================================================
```

---

## Memory System

**How it works:** Claude Code automatically reads `CLAUDE.md` from your project root at session start. This file contains project context that persists across sessions - your tech stack, conventions, active decisions, and things to avoid. The supporting files (`decisions.md`, `conventions.md`, `lessons.md`) help you build institutional knowledge over time.

**Why it matters:** Without persistent context, each session starts fresh. The memory system ensures Claude understands your project's patterns, past decisions, and lessons learned - leading to more consistent, project-aware assistance.

### Directory Structure

```
memory/
├── CLAUDE.md       # Main context file - auto-loaded by Claude Code
├── decisions.md    # Architecture Decision Records (ADRs)
├── conventions.md  # Discovered code patterns
├── lessons.md      # What worked/didn't, insights
└── README.md       # Memory system documentation
```

### File Purposes

| File | Purpose | Update Frequency |
|------|---------|------------------|
| `CLAUDE.md` | Project overview, tech stack, conventions, "do nots" | When setup changes |
| `decisions.md` | Log architectural decisions with rationale | When making decisions |
| `conventions.md` | Document discovered patterns in codebase | When patterns emerge |
| `lessons.md` | Track what worked, what didn't, debugging tips | After completing work |

### Usage

1. Copy `memory/CLAUDE.md` to your project root (Claude auto-reads it)
2. Fill in your project's tech stack and conventions
3. Add "Do NOT" rules for things Claude should avoid
4. Update `decisions.md` when making architectural choices
5. Log patterns in `conventions.md` as they're established
6. Record insights in `lessons.md` after completing work

---

## MCP Server Integrations

Pre-configured MCP servers for enhanced capabilities.

### Included Servers

| Server | Purpose |
|--------|---------|
| `sequential-thinking` | Enhanced reasoning for complex problems |
| `playwright` | Browser automation and testing |
| `filesystem` | Enhanced file operations |
| `memory` | Persistent key-value storage |
| `fetch` | HTTP requests for API testing |
| `git` | Enhanced git operations |

### Configuration

Copy `mcp.json` to your project's `.claude/mcp.json`:

```json
{
  "mcpServers": {
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@anthropics/mcp-server-sequential-thinking"]
    },
    "playwright": {
      "command": "npx",
      "args": ["-y", "@anthropics/mcp-server-playwright"]
    }
  }
}
```

See `mcp.example.json` for all available servers and configurations.

---

## Skills

### Core Skills (Always Available)

| Skill | Description |
|-------|-------------|
| `react-guidelines` | React best practices and patterns |
| `typescript-standards` | TypeScript conventions |
| `tailwind-patterns` | Tailwind CSS patterns |

### Optional Skills

| Skill | Description |
|-------|-------------|
| `tanstack-query` | Data fetching with TanStack Query |
| `zod-validation` | Schema validation with Zod |
| `react-forms` | Form handling patterns |
| `react-performance` | Performance optimization |
| `frontend-design` | UI/UX design patterns |

---

## Agents

Specialized agents for different development tasks:

| Agent | Purpose |
|-------|---------|
| `code-reviewer` | Reviews code and adds [CR] comments |
| `frontend-architect` | Designs component architecture |
| `react-developer` | Implements React features |
| `typescript-expert` | Resolves type issues |
| `ui-stylist` | Styling and design implementation |
| `explorer` | Codebase exploration and analysis |
| `web-research-specialist` | Web research and documentation lookup |

---

## Directory Structure

```
frontend-dev-toolkit/
├── .claude-plugin/
│   └── plugin.json              # Plugin metadata
├── agents/                      # Specialized agents
│   ├── code-reviewer.md
│   ├── frontend-architect.md
│   ├── react-developer.md
│   ├── typescript-expert.md
│   ├── ui-stylist.md
│   ├── explorer.md
│   └── web-research-specialist.md
├── commands/                    # Slash commands
│   ├── setup.md
│   ├── dev/                     # Development commands
│   ├── verify/                  # Verification commands
│   ├── review/                  # Code review commands
│   └── utils/                   # Utility commands
├── hooks/                       # Python hooks
│   ├── smart_context_loader.py
│   ├── skill-activation-prompt.py
│   ├── user_prompt_submit.py
│   ├── stop.py
│   ├── ...
│   └── utils/                   # Hook utilities
├── memory/                      # Memory system templates
│   ├── CLAUDE.md
│   ├── decisions.md
│   ├── conventions.md
│   └── lessons.md
├── skills/                      # Skill definitions
│   ├── core/
│   └── optional/
├── mcp.json                     # MCP server config
├── mcp.example.json             # Extended MCP examples
├── settings.json                # Default settings with hooks
└── README.md
```

---

## Configuration

### settings.json

The plugin includes a pre-configured `settings.json` with all hooks enabled:

```json
{
  "permissions": {
    "allow": ["Edit:*", "Write:*", "Bash:*"],
    "defaultMode": "acceptEdits"
  },
  "enableAllProjectMcpServers": true,
  "enabledMcpjsonServers": ["sequential-thinking", "playwright"],
  "hooks": {
    "UserPromptSubmit": [...],
    "Stop": [...],
    ...
  }
}
```

### Environment Variables

| Variable | Description |
|----------|-------------|
| `CLAUDE_HOOKS_LOG_DIR` | Base directory for logs (default: `logs`) |
| `CLAUDE_PROJECT_DIR` | Project directory for skill rules |
| `ANTHROPIC_API_KEY` | For LLM-powered hook features |
| `OPENAI_API_KEY` | Alternative LLM provider |
| `ENGINEER_NAME` | For personalized messages |

---

## Tech Stack Support

### Core (Always Enabled)
- React 19+
- TypeScript
- Tailwind CSS

### Optional (Configure During Setup)
- TanStack Query
- React Router / TanStack Router
- Zod
- Zustand
- React Hook Form
- AG Grid
- shadcn/ui

---

## Contributing

1. Fork the repository
2. Create your feature branch
3. Make your changes
4. Submit a pull request

## License

MIT
