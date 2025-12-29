#!/bin/bash
# Session startup script
# Hook: SessionStart
# Purpose: Display project status and configure environment

echo "=== Zombie Survival Game Session ==="
echo "Python: $(python --version 2>&1)"
echo "Working dir: $CLAUDE_PROJECT_DIR"

# Set debug mode for session
if [ -n "$CLAUDE_ENV_FILE" ]; then
    echo 'export GAME_DEBUG=1' >> "$CLAUDE_ENV_FILE"
fi
