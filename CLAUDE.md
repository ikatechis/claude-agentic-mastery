# Zombie Survival Game - Claude Instructions

## Project Overview

Top-down zombie survival game built with pygame. This is a learning project for mastering agentic coding with Claude Code.

## Tech Stack

- **Python:** 3.11.5 (managed by pyenv)
- **Package Manager:** uv (v0.9.18)
- **Game Library:** pygame==2.5.2
- **Version Control:** Git

## How to Run

```bash
# Install dependencies (first time only)
uv sync

# Run the game
uv run python src/main.py

# Run with display (if available)
DISPLAY=:0 uv run python src/main.py
```

## Current Architecture

```
src/
├── main.py              # Entry point, starts the game
├── game.py              # Main game loop, event handling, rendering
└── entities/
    ├── __init__.py
    └── player.py        # Player character with WASD movement
```

**Game Class (game.py):**
- Manages pygame initialization
- Runs main game loop (60 FPS)
- Handles events (QUIT, ESC key)
- Updates and renders all entities

**Player Class (player.py):**
- Green circle sprite (radius 15)
- WASD movement (200 px/sec)
- Frame-independent movement using delta_time
- Boundary checking (stays within screen)

## 🔒 MANDATORY VERIFICATION PROTOCOL

**⚠️ BEFORE SUGGESTING ANY CODE, COMMAND, OR TECHNICAL DETAIL ⚠️**

### You MUST:

1. **Search official documentation** (use web_search tool)
   - pygame documentation for pygame 2.5.2
   - Python documentation for Python 3.11
   - uv documentation for package management

2. **Verify exact syntax**
   - Function signatures (parameters, return types)
   - Method names and parameters
   - Class structure and inheritance patterns
   - Command-line flags and options

3. **Check @pyproject.toml for library versions**
   - ALWAYS read pyproject.toml before suggesting library code
   - Verify APIs exist in the specified version
   - Never assume newer/older API features

4. **State confidence level for EVERY suggestion:**
   - ✅ **VERIFIED:** "Checked pygame 2.5.2 docs - pygame.sprite.Sprite requires super().__init__()"
   - ⚠️ **UNCERTAIN:** "Will search pygame docs to verify correct parameters"
   - ❌ **GUESSING:** "Let me verify this with web_search before proceeding"

5. **Never guess:**
   - API names or signatures
   - Parameter syntax
   - Configuration file formats
   - Command flags
   - Library version features

### What to Verify

**Pygame APIs:**
- Function/method signatures, parameter names/types, return values
- Class inheritance patterns, event types and constants

**Python Features:**
- Syntax compatibility with Python 3.11
- Standard library functions, built-in methods

**Tools & Commands:**
- uv commands (add, sync, run, etc.)
- pyenv commands (local, global, etc.)
- Git commands (init, add, commit, etc.)

**Configuration Files:**
- pyproject.toml structure, .python-version format, .gitignore patterns

### Why Verification Matters

**Without verification:**
- Hours debugging hallucinated APIs
- Wrong parameter names/types
- Version incompatibilities
- Frustration and wasted time

**With verification:**
- Code works first time
- Confidence in suggestions
- Learn real APIs
- Professional development habits

**Result:** Session 1 had 14 verifications → ZERO bugs on first run

### Examples

✅ **GOOD:** "Searched pygame 2.5.2 docs - pygame.display.set_mode((width, height)) confirmed"

❌ **BAD:** "I think pygame has a circle() function" (proceeds without verification)

## Development Workflow

1. **Before coding:** Search docs and verify APIs
2. **After coding:** Test immediately with `uv run python src/main.py`
3. **Before committing:** Ensure game runs without errors
4. **Git commits:** Use conventional commit format (feat:, fix:, docs:, etc.)

## Project Goals

Building through 15 sessions to learn:
- Skills, Subagents, MCP servers
- Hooks, slash commands
- Context management
- **Verification-first development** (core skill)

## Current Status

**Session 1 Complete:**
- ✅ Python 3.11.5 with pyenv
- ✅ uv package manager setup
- ✅ pygame 2.5.2 installed
- ✅ Game window (800x600, 60 FPS)
- ✅ Player with WASD movement
- ✅ Verification protocol established

**Next Session:** Add zombies, collision, combat

## Remember

**VERIFICATION ISN'T OPTIONAL - IT'S MANDATORY**

Every suggestion without verification is a potential bug.
Always search docs first. State what you verified.
Build with confidence through verification.
