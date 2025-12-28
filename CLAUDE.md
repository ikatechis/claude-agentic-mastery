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

# Run the game (normal mode - quiet console, full file logs)
uv run python src/main.py

# Run with debug mode (verbose console output)
GAME_DEBUG=1 uv run python src/main.py

# Run with display (if available)
DISPLAY=:0 uv run python src/main.py
```

**Log files**: Saved to `logs/game_YYYY-MM-DD_HHMMSS.log` for playtest archiving

## Current Architecture

```
src/
├── main.py              # Entry point, logging initialization
├── logger.py            # Logging configuration (console + file)
├── game.py              # Main game loop, event handling, rendering
├── game_state.py        # Game state enum (MENU, PLAYING, PAUSED, GAME_OVER)
├── config.py            # Centralized configuration (dataclasses)
├── utils.py             # Utility functions (sprite loading)
└── entities/
    ├── __init__.py
    ├── player.py        # Player with health, combat, power-up effects
    ├── zombie.py        # Zombie AI with chase behavior
    └── powerup.py       # Collectible power-ups (health, speed, shield)
```

**Game Class (game.py):**
- State machine (MENU, PLAYING, PAUSED, GAME_OVER)
- Wave-based zombie spawning with exponential scaling
- Score tracking and high score system
- Power-up management and visual effects
- Health bar, wave notifications, damage popups

**Player Class (player.py):**
- Sprite-based rendering with rotation
- WASD movement (200 px/sec base, affected by power-ups)
- Health system (100 HP, damage cooldown)
- Melee combat (SPACE key, attack range, cooldown)
- Power-up effects (speed boost, shield)

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

## Logging Guidelines

**All new scripts and modules MUST follow these logging practices:**

### 1. Adding Logging to New Modules

**Standard pattern for all Python files:**

```python
from logger import get_logger

logger = get_logger(__name__)
```

**Example in a new module:**

```python
"""My new game module."""

from logger import get_logger

logger = get_logger(__name__)


def my_function():
    """Do something important."""
    logger.debug("Starting my_function")
    try:
        # ... code ...
        logger.info("Operation completed successfully")
    except SomeError as e:
        logger.warning(f"Operation failed: {e}")
```

### 2. When to Use Each Log Level

**DEBUG** (only visible with GAME_DEBUG=1 console, always in file):
- Detailed state changes for debugging
- Entity lifecycle events (spawn, death, movement)
- Sprite loading attempts and fallbacks
- Power-up collections and expirations
- Attack attempts and combat calculations
- Frame-by-frame state dumps (use sparingly)

**Examples:**
```python
logger.debug(f"Zombie spawned at ({int(x)}, {int(y)})")
logger.debug(f"Player took {damage} damage, health: {health}/{max_health}")
logger.debug(f"Sprite not found: {path}, using fallback")
logger.debug(f"Speed boost applied: {multiplier}x for {duration}s")
```

**INFO** (visible in file only by default):
- Normal game operations and milestones
- Successful file operations (save/load)
- Game lifecycle events (start, end)
- Configuration initialization
- Wave progression and score milestones

**Examples:**
```python
logger.info("Game started")
logger.info(f"High score loaded: {self.high_score}")
logger.info(f"Wave {wave_number} complete")
logger.info("Logging initialized - log file: {log_file}")
```

**WARNING** (visible in console and file):
- Recoverable errors (file not found, using fallback)
- Missing resources with graceful degradation
- Failed save operations
- Unexpected but handled conditions
- Performance concerns (if FPS drops below threshold)

**Examples:**
```python
logger.warning("Background tile not found, using solid color fallback")
logger.warning(f"Failed to save high score: {e}")
logger.warning("High score file corrupted, defaulting to 0")
logger.warning(f"FPS dropped to {fps}, expected 60")
```

**ERROR** (visible in console and file):
- Unhandled exceptions
- Critical failures that affect gameplay
- Data corruption without recovery
- System-level failures

**Examples:**
```python
logger.error(f"Unhandled exception: {e}", exc_info=True)
logger.error("Failed to initialize pygame display")
logger.error(f"Critical config file missing: {config_path}")
```

### 3. Error Handling Pattern

**NEVER suppress errors silently. Always log them.**

**❌ BAD (silent suppression):**
```python
try:
    save_data()
except OSError:
    pass  # Silent failure - bad!
```

**✅ GOOD (logged warning):**
```python
try:
    save_data()
    logger.info("Data saved successfully")
except OSError as e:
    logger.warning(f"Failed to save data: {e}")
```

**✅ GOOD (with contextlib.suppress replacement):**
```python
# Before:
with contextlib.suppress(pygame.error, FileNotFoundError):
    sprite = load_sprite(path)

# After:
try:
    sprite = load_sprite(path)
    logger.debug(f"Loaded sprite: {path}")
except (pygame.error, FileNotFoundError):
    logger.debug(f"Sprite not found: {path}, using fallback")
    sprite = None
```

### 4. Logging Best Practices

**DO:**
- Use f-strings for readable log messages
- Include context (entity IDs, coordinates, values)
- Log at appropriate levels (don't spam DEBUG in INFO)
- Use `exc_info=True` for ERROR logs to get stack traces
- Include units in numeric values (e.g., "5.2s", "120 HP", "(150, 200)")
- Make log messages searchable (consistent terminology)

**DON'T:**
- Log sensitive data (user passwords, API keys)
- Log in tight loops (every frame) unless using DEBUG level
- Use print() statements (always use logger)
- Duplicate log messages (one log per event)
- Log excessively verbose data structures (use summary info)

**Example - Entity lifecycle logging:**
```python
class Enemy:
    def __init__(self, x, y, enemy_type):
        self.id = generate_id()
        logger.debug(f"Enemy {enemy_type} spawned: ID={self.id}, pos=({int(x)}, {int(y)})")

    def take_damage(self, amount):
        old_health = self.health
        self.health -= amount
        logger.debug(f"Enemy ID={self.id} took {amount} damage, health: {self.health}/{self.max_health}")

        if self.health <= 0:
            logger.debug(f"Enemy ID={self.id} died at ({int(self.x)}, {int(self.y)})")
```

### 5. Testing Logs During Development

**Normal run (quiet console, full file logs):**
```bash
uv run python src/main.py
# Check logs/game_YYYY-MM-DD_HHMMSS.log for full details
```

**Debug run (verbose console + full file logs):**
```bash
GAME_DEBUG=1 uv run python src/main.py
# See DEBUG messages in real-time on console
```

**Viewing log files:**
```bash
# View latest log
ls -t logs/*.log | head -1 | xargs cat

# Tail live log in debug mode
tail -f logs/game_*.log

# Search for errors
grep -i error logs/game_*.log

# Filter by level
grep '\[WARNING\]' logs/game_*.log
```

### 6. Log File Archiving

- Log files are timestamped: `logs/game_YYYY-MM-DD_HHMMSS.log`
- Each playtest session creates a new file
- Files are excluded from git (in `.gitignore`)
- Review logs after playtests to identify issues
- Archive important logs for bug reports

### 7. Checklist for New Modules

When creating a new Python file:

- [ ] Import logger: `from logger import get_logger`
- [ ] Initialize logger: `logger = get_logger(__name__)`
- [ ] Replace print() with logger calls
- [ ] Add DEBUG logs for detailed state changes
- [ ] Add INFO logs for normal operations
- [ ] Add WARNING logs for recoverable errors (with try/except)
- [ ] Add ERROR logs for critical failures (with exc_info=True)
- [ ] Test with both normal and GAME_DEBUG=1 modes
- [ ] Review log output for clarity and usefulness

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

**Session 3 Complete:**
- ✅ Wave-based spawning with exponential scaling
- ✅ Score tracking and UI display
- ✅ Game states (MENU, PLAYING, GAME_OVER)
- ✅ Menu and game over screens
- ✅ Wave notifications
- ✅ High score system (in-memory)
- ✅ Pause state (ESC/P key)

**Session 4 Complete:**
- ✅ Power-up system (HEALTH, SPEED, SHIELD)
- ✅ Power-up drop chance on zombie kill
- ✅ Timed power-ups with visual indicators
- ✅ Visual effects (kill flashes, damage popups, pickup flashes)
- ✅ Sprite loading system with fallbacks
- ✅ Test coverage: 52 tests, 69% coverage

**Logging System Complete:**
- ✅ Timestamped log files for playtest archiving
- ✅ Debug mode flag (GAME_DEBUG=1)
- ✅ Dual output: console (WARNING+) and file (DEBUG+)
- ✅ Replaced silent error suppression with logged warnings
- ✅ Entity event logging (damage, spawns, power-ups)

## Future Sessions Roadmap

**Session 5: Zombie Variants & Character Animations**
- Zombie variants - Multiple zombie types with different colors/stats
  - Use Kenney Zombie 1 & Zombie 2 sprites (Topdown Shooter pack)
  - Variant spawn probabilities
- Character animations - Sprite-based animation system
  - Idle, walking, attacking poses
  - Frame-based animation with delta_time
  - Use Kenney 6-pose sprite sets (stand, hold, gun, machine, reload, silencer)

**Session 6+: Polish & Expansion**
- Sound effects & music (Kenney Audio assets)
- More enemy types (Survivors, Robots from Kenney)
- Power-up improvements & new types
- Level/environment tiles & obstacles

## Remember

**VERIFICATION ISN'T OPTIONAL - IT'S MANDATORY**

Every suggestion without verification is a potential bug.
Always use ref.tools to search docs first. State what you verified.
Build with confidence through verification.

**MCP Tools Available:**
- ✅ **ref.tools** - Installed and configured for pygame/Python documentation
- Use `ref_search_documentation` and `ref_read_url` for all API verifications
