#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
# ]
# ///

"""
Stop Hook with Session Summary Generation

Handles session stop events:
- Logs stop data
- Optionally saves transcript to chat.json (--chat)
- Optionally generates session summary (--summary)
"""

import argparse
import json
import os
import sys
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

from utils.constants import ensure_session_log_dir

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def parse_transcript(transcript_path: str) -> List[Dict[str, Any]]:
    """Parse JSONL transcript file into list of messages"""
    messages = []
    try:
        with open(transcript_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        messages.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
    except Exception:
        pass
    return messages


def extract_session_info(messages: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Extract useful information from transcript messages"""
    info = {
        "user_prompts": [],
        "tools_used": [],
        "files_modified": [],
        "files_created": [],
        "files_read": [],
        "commands_run": [],
        "errors_encountered": [],
        "total_messages": len(messages)
    }

    for msg in messages:
        msg_type = msg.get("type", "")

        # Extract user prompts
        if msg_type == "human" or msg.get("role") == "user":
            content = msg.get("content", msg.get("message", ""))
            if isinstance(content, str) and content.strip():
                # Truncate long prompts
                prompt = content[:200] + "..." if len(content) > 200 else content
                info["user_prompts"].append(prompt)

        # Extract tool usage
        if msg_type == "tool_use" or "tool" in msg:
            tool_name = msg.get("name", msg.get("tool", ""))
            if tool_name:
                if tool_name not in info["tools_used"]:
                    info["tools_used"].append(tool_name)

                # Track file operations
                tool_input = msg.get("input", {})
                if isinstance(tool_input, dict):
                    file_path = tool_input.get("file_path", tool_input.get("path", ""))
                    if file_path:
                        if tool_name in ["Write", "Edit", "MultiEdit"]:
                            if file_path not in info["files_modified"]:
                                info["files_modified"].append(file_path)
                        elif tool_name == "Read":
                            if file_path not in info["files_read"]:
                                info["files_read"].append(file_path)

                    # Track bash commands
                    if tool_name == "Bash":
                        command = tool_input.get("command", "")
                        if command:
                            # Truncate long commands
                            cmd = command[:100] + "..." if len(command) > 100 else command
                            info["commands_run"].append(cmd)

        # Extract errors
        if msg_type == "tool_result" or "error" in str(msg).lower():
            content = str(msg.get("content", msg.get("output", "")))
            if "error" in content.lower() or "failed" in content.lower():
                error = content[:150] + "..." if len(content) > 150 else content
                info["errors_encountered"].append(error)

    # Deduplicate and limit
    info["files_modified"] = list(set(info["files_modified"]))[:20]
    info["files_read"] = list(set(info["files_read"]))[:20]
    info["commands_run"] = info["commands_run"][:15]
    info["errors_encountered"] = info["errors_encountered"][:10]

    return info


def generate_summary(info: Dict[str, Any]) -> str:
    """Generate a human-readable session summary"""
    summary = []
    summary.append("=" * 60)
    summary.append("SESSION SUMMARY")
    summary.append("=" * 60)
    summary.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    summary.append("")

    # What was requested
    if info["user_prompts"]:
        summary.append("## What Was Requested")
        for i, prompt in enumerate(info["user_prompts"][:5], 1):
            # Clean up the prompt for display
            clean_prompt = prompt.replace("\n", " ").strip()
            summary.append(f"  {i}. {clean_prompt}")
        if len(info["user_prompts"]) > 5:
            summary.append(f"  ... and {len(info['user_prompts']) - 5} more prompts")
        summary.append("")

    # Files modified
    if info["files_modified"]:
        summary.append("## Files Modified")
        for f in info["files_modified"][:10]:
            summary.append(f"  ✏️  {f}")
        if len(info["files_modified"]) > 10:
            summary.append(f"  ... and {len(info['files_modified']) - 10} more files")
        summary.append("")

    # Tools used
    if info["tools_used"]:
        summary.append("## Tools Used")
        summary.append(f"  {', '.join(info['tools_used'])}")
        summary.append("")

    # Commands run
    if info["commands_run"]:
        summary.append("## Commands Executed")
        for cmd in info["commands_run"][:5]:
            summary.append(f"  $ {cmd}")
        if len(info["commands_run"]) > 5:
            summary.append(f"  ... and {len(info['commands_run']) - 5} more commands")
        summary.append("")

    # Errors
    if info["errors_encountered"]:
        summary.append("## Errors Encountered")
        for err in info["errors_encountered"][:3]:
            summary.append(f"  ⚠️  {err[:100]}")
        summary.append("")

    # Statistics
    summary.append("## Statistics")
    summary.append(f"  • Total messages: {info['total_messages']}")
    summary.append(f"  • Files modified: {len(info['files_modified'])}")
    summary.append(f"  • Files read: {len(info['files_read'])}")
    summary.append(f"  • Commands run: {len(info['commands_run'])}")
    summary.append("")

    summary.append("=" * 60)

    return "\n".join(summary)


def save_summary(log_dir: Path, summary: str, info: Dict[str, Any]):
    """Save summary to files"""
    # Save human-readable summary
    summary_file = log_dir / 'session_summary.txt'
    with open(summary_file, 'w') as f:
        f.write(summary)

    # Save structured data
    data_file = log_dir / 'session_summary.json'
    with open(data_file, 'w') as f:
        json.dump({
            "generated_at": datetime.now().isoformat(),
            "info": info
        }, f, indent=2)


def main():
    try:
        # Parse command line arguments
        parser = argparse.ArgumentParser()
        parser.add_argument('--chat', action='store_true',
                          help='Copy transcript to chat.json')
        parser.add_argument('--summary', action='store_true',
                          help='Generate session summary')
        args = parser.parse_args()

        # Read JSON input from stdin
        input_data = json.load(sys.stdin)

        # Extract required fields
        session_id = input_data.get("session_id", "unknown")
        transcript_path = input_data.get("transcript_path", "")

        # Ensure session log directory exists
        log_dir = ensure_session_log_dir(session_id)
        log_path = log_dir / "stop.json"

        # Read existing log data or initialize empty list
        if log_path.exists():
            with open(log_path, 'r') as f:
                try:
                    log_data = json.load(f)
                except (json.JSONDecodeError, ValueError):
                    log_data = []
        else:
            log_data = []

        # Append new data
        log_data.append(input_data)

        # Write back to file with formatting
        with open(log_path, 'w') as f:
            json.dump(log_data, f, indent=2)

        # Handle transcript processing
        if transcript_path and os.path.exists(transcript_path):
            messages = parse_transcript(transcript_path)

            # Save chat.json if requested
            if args.chat and messages:
                chat_file = log_dir / 'chat.json'
                with open(chat_file, 'w') as f:
                    json.dump(messages, f, indent=2)

            # Generate summary if requested
            if args.summary and messages:
                info = extract_session_info(messages)
                summary = generate_summary(info)
                save_summary(log_dir, summary, info)

                # Print summary to stdout so user sees it
                print("\n" + summary)

        sys.exit(0)

    except json.JSONDecodeError:
        sys.exit(0)
    except Exception as e:
        print(f"Error in stop hook: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
