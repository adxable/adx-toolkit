#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

from utils.constants import ensure_session_log_dir


def load_skill_rules(project_dir: str) -> Dict[str, Any]:
    """Load skill rules from .claude/skills/skill-rules.json"""
    rules_path = Path(project_dir) / '.claude' / 'skills' / 'skill-rules.json'

    if not rules_path.exists():
        return {'version': '1.0', 'skills': {}}

    with open(rules_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def match_keywords(prompt: str, keywords: List[str]) -> bool:
    """Check if any keyword matches the prompt (case-insensitive)"""
    prompt_lower = prompt.lower()
    return any(kw.lower() in prompt_lower for kw in keywords)


def match_intent_patterns(prompt: str, patterns: List[str]) -> bool:
    """Check if any intent pattern matches the prompt (case-insensitive)"""
    return any(re.search(pattern, prompt, re.IGNORECASE) for pattern in patterns)


def find_matched_skills(prompt: str, skills: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Find all skills that match the prompt"""
    matched = []

    for skill_name, config in skills.items():
        triggers = config.get('promptTriggers')
        if not triggers:
            continue

        # Check keyword matching
        keywords = triggers.get('keywords', [])
        if keywords and match_keywords(prompt, keywords):
            matched.append({
                'name': skill_name,
                'matchType': 'keyword',
                'config': config
            })
            continue

        # Check intent pattern matching
        intent_patterns = triggers.get('intentPatterns', [])
        if intent_patterns and match_intent_patterns(prompt, intent_patterns):
            matched.append({
                'name': skill_name,
                'matchType': 'intent',
                'config': config
            })

    return matched


def group_by_priority(matched_skills: List[Dict[str, Any]]) -> Dict[str, List[str]]:
    """Group matched skills by priority level"""
    groups = {
        'critical': [],
        'high': [],
        'medium': [],
        'low': []
    }

    for skill in matched_skills:
        priority = skill['config'].get('priority', 'low')
        if priority in groups:
            groups[priority].append(skill['name'])

    return groups


def format_output(groups: Dict[str, List[str]]) -> str:
    """Format the skill activation message"""
    output = '=' * 50 + '\n'
    output += 'SKILL ACTIVATION CHECK\n'
    output += '=' * 50 + '\n\n'

    if groups['critical']:
        output += '! CRITICAL SKILLS (REQUIRED):\n'
        for skill in groups['critical']:
            output += f'  > {skill}\n'
        output += '\n'

    if groups['high']:
        output += '+ RECOMMENDED SKILLS:\n'
        for skill in groups['high']:
            output += f'  > {skill}\n'
        output += '\n'

    if groups['medium']:
        output += '* SUGGESTED SKILLS:\n'
        for skill in groups['medium']:
            output += f'  > {skill}\n'
        output += '\n'

    if groups['low']:
        output += '- OPTIONAL SKILLS:\n'
        for skill in groups['low']:
            output += f'  > {skill}\n'
        output += '\n'

    output += 'ACTION: Use Skill tool BEFORE responding\n'
    output += '=' * 50 + '\n'

    return output


def log_skill_activation(session_id: str, prompt: str, matched_skills: List[Dict[str, Any]]):
    """Log skill activation to session directory."""
    try:
        # Ensure session log directory exists
        log_dir = ensure_session_log_dir(session_id)
        log_file = log_dir / 'skill_activation.json'

        # Read existing log data or initialize empty list
        if log_file.exists():
            with open(log_file, 'r') as f:
                try:
                    log_data = json.load(f)
                except (json.JSONDecodeError, ValueError):
                    log_data = []
        else:
            log_data = []

        # Create log entry
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'prompt': prompt[:200] + '...' if len(prompt) > 200 else prompt,  # Truncate long prompts
            'matched_skills': [
                {
                    'name': skill['name'],
                    'match_type': skill['matchType'],
                    'priority': skill['config'].get('priority', 'low'),
                    'enforcement': skill['config'].get('enforcement', 'suggest')
                }
                for skill in matched_skills
            ],
            'total_matches': len(matched_skills)
        }

        # Append the entry
        log_data.append(log_entry)

        # Write back to file with formatting
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)

    except Exception as e:
        # Don't fail the hook if logging fails
        print(f"Warning: Failed to log skill activation: {e}", file=sys.stderr)


def main():
    try:
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)

        # Extract session_id and prompt
        session_id = input_data.get('session_id', 'unknown')
        prompt = input_data.get('prompt', '')

        if not prompt:
            sys.exit(0)

        # Get project directory
        project_dir = os.environ.get('CLAUDE_PROJECT_DIR', os.path.expanduser('~/project'))

        # Load skill rules
        rules = load_skill_rules(project_dir)
        skills = rules.get('skills', {})

        if not skills:
            sys.exit(0)

        # Find matched skills
        matched_skills = find_matched_skills(prompt, skills)

        # Log skill activation (always log, even if no matches)
        log_skill_activation(session_id, prompt, matched_skills)

        # Output message if matches found
        if matched_skills:
            groups = group_by_priority(matched_skills)
            output = format_output(groups)
            print(output)

        sys.exit(0)

    except json.JSONDecodeError:
        # Handle JSON decode errors gracefully
        sys.exit(0)
    except Exception as e:
        # Log error but exit cleanly
        print(f"Error in skill-activation-prompt hook: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == '__main__':
    main()
