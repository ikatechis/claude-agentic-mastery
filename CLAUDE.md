# Zombie Survival Game - Claude Instructions

## Project Overview

Top-down zombie survival game built with pygame. This is a learning project for mastering agentic coding with Claude Code.

## Tech Stack

- **Python:** 3.11.5 (managed by pyenv)
- **Package Manager:** uv (v0.9.18)
- **Game Library:** pygame==2.6.0
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

1. **Search official documentation** (use ref.tools MCP for API lookups)
   - **Primary:** `ref_search_documentation` + `ref_read_url` for library/framework APIs
   - **Secondary:** `web_search` for tutorials, examples, troubleshooting
   - Check library versions in pyproject.toml before searching
   - Verify Python 3.11 compatibility for standard library features
   - Check tool documentation (uv, pyenv, etc.) for command syntax

2. **Verify exact syntax**
   - Function signatures (parameters, return types)
   - Method names and parameters
   - Class structure and inheritance patterns
   - Command-line flags and options

3. **Check @pyproject.toml for library versions**
   - ALWAYS read pyproject.toml before suggesting library code
   - Verify APIs exist in the specified version
   - Never assume newer/older API features

4. **State confidence level for library-specific suggestions:**
   - ✅ **VERIFIED:** "Checked pygame 2.6.0 docs via ref.tools - pygame.sprite.Sprite requires super().__init__()"
   - ✅ **OBVIOUS:** "Using standard Python `for` loop (no verification needed)"
   - ⚠️ **UNCERTAIN:** "Will search pygame docs to verify correct parameters"
   - ❌ **GUESSING:** "Let me verify this with ref.tools before proceeding"

5. **Never guess:**
   - API names or signatures
   - Parameter syntax
   - Configuration file formats
   - Command flags
   - Library version features

### What to Verify

**External Library APIs:**
- Function/method signatures, parameter names/types, return values
- Class inheritance patterns, special methods
- Framework-specific concepts (sprites, events, collision detection, etc.)
- Version-specific features and deprecations

**Python Features:**
- Syntax compatibility with project's Python version (check pyproject.toml)
- Standard library functions, built-in methods
- Type hints and annotations

**Tools & Commands:**
- Package manager commands (uv add, sync, run, etc.)
- Version managers (pyenv local, global, etc.)
- Git commands (commit, push, branch, etc.)

**Configuration Files:**
- pyproject.toml structure, dependencies format
- Tool-specific config (.python-version, .gitignore, etc.)

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

✅ **GOOD:** "Used ref.tools to verify pygame.sprite.Group - confirmed add(), remove(), update(), draw() methods"

✅ **GOOD:** "Searched pygame 2.6.0 docs via ref_read_url - pygame.display.set_mode((width, height)) confirmed"

❌ **BAD:** "I think pygame has a circle() function" (proceeds without verification)

### When to Use Each Tool

**Use ref.tools (ref_search_documentation + ref_read_url):**
- Quick API signature verification
- Function parameter names and types
- Class methods and attributes
- Official documentation lookups
- **Benefits:** Faster, more precise, lower token usage, prompt caching

**Use web_search:**
- Need code examples or tutorials
- Troubleshooting specific errors
- Community solutions and patterns
- Broader context beyond API docs

### Smart Verification (Reduce API Usage)

**❌ DON'T verify these (waste of tokens):**
- Basic Python syntax: `if`, `for`, `while`, `print()`, `len()`, `range()`
- Standard operators: `+`, `-`, `*`, `/`, `==`, `and`, `or`
- APIs already verified in current session (reference previous verification)
- Obvious operations: variable assignment, function calls, imports
- Common patterns: `__init__()`, `super().__init__()`, `self.attribute`

**✅ DO verify these (critical for correctness):**
- **External library APIs** (pygame, numpy, any third-party packages)
- New library functions/classes not yet used in project
- Version-specific features (check exact version in pyproject.toml)
- Parameter order/names for unfamiliar functions
- Return types and expected values
- Framework-specific patterns (pygame event handling, sprite systems, etc.)

**💡 Optimization tips:**
- **Batch verifications:** Search "pygame sprite Group add update draw" instead of 3 separate lookups
- **Reference earlier:** "As verified earlier, pygame.sprite.Group.add()..."
- **Be concise:** Skip verbose explanations unless asked
- **Only read files when needed:** Don't speculatively read files

## Development Workflow

1. **Before coding:** Verify APIs with ref.tools (or web_search if needed)
2. **After coding:** Test immediately with `uv run python src/main.py`
3. **Before committing:** Ensure game runs without errors
4. **Git commits:** Use conventional commit format (feat:, fix:, docs:, etc.)

### Example Verification Workflow

```bash
# 1. Check what we need (e.g., collision detection for zombies)
ref_search_documentation("pygame sprite collision pygame 2.6.0")

# 2. Read specific API docs
ref_read_url("https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.spritecollide")

# 3. Verify exact syntax before writing code
# ✅ CONFIRMED: spritecollide(sprite, group, dokill, collided=None)

# 4. Write code with confidence
# 5. Test immediately
uv run python src/main.py
```

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
- ✅ pygame 2.6.0 installed
- ✅ Game window (800x600, 60 FPS)
- ✅ Player with WASD movement
- ✅ Verification protocol established

**Session 2 Complete:**
- ✅ Zombie entities with chase AI
- ✅ Circle-based collision detection
- ✅ Health system with damage cooldown
- ✅ Melee combat (SPACE key, attack range)
- ✅ Zombie spawning system (off-screen, random sides)
- ✅ Visual health bar UI
- ✅ Centralized config system (dataclasses)

**Session 2.5 Complete:**
- ✅ Modern dev tooling (ruff, mypy, pytest)
- ✅ Pre-commit hooks + GitHub Actions CI/CD
- ✅ Test infrastructure (6 tests, 43% coverage)
- ✅ Code quality automation

**Next Session:** Wave-based spawning, score counter, game states

## Remember

**VERIFICATION ISN'T OPTIONAL - IT'S MANDATORY**

Every suggestion without verification is a potential bug.
Always use ref.tools to search docs first. State what you verified.
Build with confidence through verification.

**MCP Tools Available:**
- ✅ **ref.tools** - Installed and configured for pygame/Python documentation
- Use `ref_search_documentation` and `ref_read_url` for all API verifications
