#!/usr/bin/env python3
"""
Prompt reminder hook
Hook: UserPromptSubmit
Purpose: Remind about verification protocol for pygame-related prompts
"""

import json
import sys

data = json.load(sys.stdin)
prompt = data.get("tool_input", {}).get("prompt", "").lower()

# Add reminder for pygame-related prompts
if "pygame" in prompt and ("how" in prompt or "what" in prompt):
    print(
        json.dumps(
            {"systemMessage": "Remember: Verify pygame APIs with ref.tools before suggesting code!"}
        )
    )

sys.exit(0)
