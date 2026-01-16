# Claude Code Hooks

This directory contains Python hooks for Claude Code that provide logging, skill activation, and session management functionality.

## Prerequisites

- Python 3.8+ (3.11+ recommended)
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer and resolver

## Hooks Overview

| Hook | Event | Description |
|------|-------|-------------|
| `user_prompt_submit.py` | UserPromptSubmit | Logs user prompts and optionally validates them |
| `skill-activation-prompt.py` | UserPromptSubmit | Detects keywords/patterns to suggest relevant skills |
| `pre_tool_use.py` | PreToolUse | Logs tool usage before execution |
| `post_tool_use.py` | PostToolUse | Logs tool usage after execution |
| `notification.py` | Notification | Logs notifications from Claude |
| `stop.py` | Stop | Logs session stop events, optionally saves transcript |
| `subagent_stop.py` | SubagentStop | Logs subagent stop events |
| `pre_compact.py` | PreCompact | Logs context compaction events |

## Installation

1. Copy the `hooks` directory to your project root or `.claude/hooks/`

2. Add hook configuration to your `.claude/settings.json` or `.claude/settings.local.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "uv run hooks/skill-activation-prompt.py || true"
          },
          {
            "type": "command",
            "command": "uv run hooks/user_prompt_submit.py --log-only || true"
          }
        ]
      }
    ],
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "uv run hooks/stop.py --chat || true"
          }
        ]
      }
    ]
  }
}
```

See `settings.example.json` for a complete configuration.

## Directory Structure

```
hooks/
├── notification.py           # Notification event logger
├── post_tool_use.py          # Post-tool execution logger
├── pre_tool_use.py           # Pre-tool execution logger
├── pre_compact.py            # Context compaction logger
├── skill-activation-prompt.py # Skill detection and suggestion
├── stop.py                   # Session stop handler
├── subagent_stop.py          # Subagent stop handler
├── user_prompt_submit.py     # User prompt logger/validator
├── settings.example.json     # Example settings configuration
├── README.md                 # This file
├── logs/                     # Session logs directory (auto-created)
└── utils/
    ├── __init__.py
    ├── constants.py          # Shared constants and helpers
    └── llm/
        ├── __init__.py
        ├── anth.py           # Anthropic API helper
        └── oai.py            # OpenAI API helper
```

## Logging

All hooks log to `logs/{session_id}/` directory, creating JSON files for each event type:
- `user_prompt_submit.json`
- `skill_activation.json`
- `pre_tool_use.json`
- `post_tool_use.json`
- `notification.json`
- `stop.json`
- `subagent_stop.json`
- `pre_compact.json`
- `chat.json` (when `--chat` flag is used with stop hooks)

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `CLAUDE_HOOKS_LOG_DIR` | Base directory for logs | `logs` |
| `CLAUDE_PROJECT_DIR` | Project directory for skill rules | `~/project` |
| `ANTHROPIC_API_KEY` | API key for Anthropic LLM helpers | - |
| `OPENAI_API_KEY` | API key for OpenAI LLM helpers | - |
| `ENGINEER_NAME` | Name for personalized completion messages | - |

## Command Line Options

### user_prompt_submit.py
- `--validate` - Enable prompt validation against blocked patterns
- `--log-only` - Only log prompts, no validation

### stop.py / subagent_stop.py
- `--chat` - Save conversation transcript to `chat.json`

### notification.py
- `--notify` - Enable TTS notifications (placeholder for custom implementation)

## Skill Activation

The `skill-activation-prompt.py` hook reads skill rules from `.claude/skills/skill-rules.json`:

```json
{
  "version": "1.0",
  "skills": {
    "frontend-dev-guidelines": {
      "promptTriggers": {
        "keywords": ["react", "component", "typescript"],
        "intentPatterns": ["create.*component", "implement.*feature"]
      },
      "priority": "high",
      "enforcement": "suggest"
    }
  }
}
```

Priority levels: `critical`, `high`, `medium`, `low`
