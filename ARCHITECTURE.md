# Architecture - Zombie Survival Game

**Version:** 0.5.0 | **Last Updated:** Session 4.5 (Logging System)

---

## Overview

Top-down zombie survival game built with pygame. Architecture follows a classic game loop pattern with component-based entities and centralized configuration.

---

## Project Structure

```
src/
├── main.py              # Entry point, logging initialization
├── logger.py            # Logging system configuration
├── game.py              # Game loop orchestration, state machine
├── game_state.py        # Game state enum (MENU, PLAYING, PAUSED, GAME_OVER)
├── config.py            # Centralized configuration (dataclasses)
├── utils.py             # Utility functions (sprite loading)
└── entities/
    ├── __init__.py
    ├── player.py        # Player character with combat and power-ups
    ├── zombie.py        # Enemy entity with AI
    └── powerup.py       # Collectible power-ups
```

---

## Core Architecture

### Game Loop (game.py)

**Pattern:** Event → Update → Render

**Responsibilities:**
- Initialize pygame and window
- Handle input events (WASD, SPACE, ESC)
- Update entity state (player, zombies, power-ups)
- Check collisions (player-zombie, player-powerup, melee attacks)
- Render entities and UI (health bar, score, wave info)
- Manage game state machine (MENU, PLAYING, PAUSED, GAME_OVER)
- Wave-based zombie spawning with exponential scaling
- High score persistence (file-based)

### Entities

**Player (entities/player.py)**
- Inherits `pygame.sprite.Sprite`
- WASD movement with delta_time (200 px/sec base)
- Health system (100 HP, damage cooldown)
- Melee combat (SPACE key, attack range, cooldown)
- Power-up effects (speed boost, shield)
- Sprite-based rendering with rotation

**Zombie (entities/zombie.py)**
- Chase AI using vector math (tracks player position)
- Speed: 80 px/sec (slower than player, escapable)
- Deals damage on collision with cooldown
- Sprite-based rendering with fallback to circle
- Drops power-ups on death (20% chance)

**Powerup (entities/powerup.py)**
- Three types: HEALTH, SPEED, SHIELD
- Spawns at zombie death location
- Timed lifetime with blink warning
- Visual effects on collection
- Sprite-based rendering with type-specific colors

### Configuration System (config.py)

**Pattern:** Dataclass-based configuration

**Why?**
- Eliminates magic numbers
- Provides type safety
- Centralizes game balance tuning
- Groups related settings

**Config Classes:**
- `GameConfig` - Screen, FPS, colors
- `PlayerConfig` - Player properties (movement, combat, health)
- `ZombieConfig` - Enemy properties (speed, damage, spawn)
- `PowerupConfig` - Power-up properties (effects, duration, colors)
- `UIConfig` - **Ratio-based UI positioning**

---

## Logging System (logger.py)

**Pattern:** Dual-handler logging (console + file)

**Architecture:**
- Python's `logging` module with custom configuration
- Two handlers: console (WARNING+) and file (DEBUG+)
- Environment variable control: `GAME_DEBUG=1` enables DEBUG console output
- Timestamped log files: `logs/game_YYYY-MM-DD_HHMMSS.log`

**Log Levels:**
- **DEBUG:** Entity lifecycle, state changes, sprite loading (verbose)
- **INFO:** Normal operations, game milestones, file operations
- **WARNING:** Recoverable errors, missing resources, fallbacks
- **ERROR:** Critical failures, unhandled exceptions

**Usage Pattern:**
```python
from logger import get_logger

logger = get_logger(__name__)

# In code
logger.debug(f"Entity spawned at ({x}, {y})")
logger.info("High score loaded successfully")
logger.warning(f"Failed to load sprite: {path}, using fallback")
logger.error(f"Unhandled exception: {e}", exc_info=True)
```

**Benefits:**
- Replaces silent error suppression (no more `contextlib.suppress`)
- Full playtest session archiving (timestamped files)
- Debug mode for verbose troubleshooting
- Consistent error tracking across all modules

---

## Key Design Decisions

### 1. Ratio-Based UI Positioning

**Decision:** UI positions as ratios of screen dimensions, not absolute pixels.

**Why?**
- Scales automatically with resolution changes
- Professional/industry standard approach
- Future-proof for resolution options

**Example:** Health bar at 1.25% from left, 25% of screen width

### 2. Frame-Independent Movement

**Decision:** All movement uses `delta_time` (seconds since last frame).

**Why?**
- Consistent speed across all hardware
- Required for multiplayer (future)
- Professional standard

**Implementation:** `position += speed * delta_time`

### 3. Centralized Configuration

**Decision:** All tunables in `config.py` using dataclasses.

**Why?**
- Single source of truth for game balance
- No hunting through code to change values
- Type-safe with IDE autocomplete
- Self-documenting (default values visible)

### 4. Circle Collision Detection

**Decision:** Simple distance-based collision for circular entities.

**Why?**
- Fast (single calculation per pair)
- Sufficient for circular entities
- Easy to understand and debug

**Formula:** `collision = distance < (radius1 + radius2)`

### 5. Component-Based Entities

**Decision:** Entities update and render themselves.

**Why?**
- Separation of concerns
- Easy to add new entity types
- Follows pygame conventions

---

## Systems

### Collision System
- **Location:** `game.py::check_collision()`
- **Type:** Circle-circle collision (distance-based)
- **Current Use:**
  - Player-zombie damage (with cooldown)
  - Player-powerup collection
  - Melee attack hit detection

### Combat System
- **Melee Attacks:** SPACE key, circular attack range
- **Player Attack:** Kills zombies within range, cooldown-based
- **Zombie Damage:** Collision-based with damage cooldown (1.0s)
- **Death Handling:** Zombie death triggers power-up spawns

### Spawning System
- **Location:** `game.py::spawn_wave()`
- **Pattern:** Wave-based with exponential scaling
- **Formula:** `zombies = 3 + (wave - 1) * 1.5`
- **Spawn Locations:** Random positions off-screen (4 sides)
- **Wave Progression:** Automatic on wave clear

### Power-up System
- **Drop Chance:** 20% on zombie kill
- **Types:** HEALTH (restore HP), SPEED (movement boost), SHIELD (damage block)
- **Lifetime:** 10 seconds with 2-second blink warning
- **Effects:** Immediate (health) or timed (speed, shield)
- **Visual Feedback:** Flash effects, damage popups, status indicators

### UI System
- **Location:** `game.py` (multiple render methods)
- **Pattern:** Responsive rendering using UIConfig ratios
- **Current:**
  - Health bar with background/foreground/text
  - Score and wave display
  - High score tracking
  - Power-up status indicators (speed, shield)
  - Wave notifications
  - Menu and game over screens

---

## Game State

### Current States (game_state.py)
- **MENU:** Start screen, waiting to begin
- **PLAYING:** Active gameplay (movement, combat, waves)
- **PAUSED:** Game paused (ESC/P key), screen frozen
- **GAME_OVER:** Player death, show final score and high score

---

## Data Flow

```
Input (WASD, SPACE, ESC)
    ↓
State Machine (menu → playing → paused/game_over)
    ↓
Entities Update (player movement, zombie AI, power-up timers)
    ↓
Collision Detection (zombies, power-ups, attacks)
    ↓
Combat System (damage, kills, drops)
    ↓
Spawning System (wave progression)
    ↓
Logging (DEBUG/INFO/WARNING/ERROR events)
    ↓
UI Update (health, score, wave, power-ups)
    ↓
Render to Screen
```

---

## Future Architecture

### Future Improvements

1. **Zombie Variants (Session 5)**
   - Multiple zombie types (different stats, behaviors)
   - Sprite-based rendering with Kenney assets
   - Variant spawn probabilities

2. **Character Animations (Session 5)**
   - Frame-based animation system
   - Idle, walking, attacking poses
   - Sprite sheets for player and zombies

3. **System Separation (Future)**
   - `src/systems/collision.py`
   - `src/systems/combat.py`
   - `src/systems/spawning.py`

4. **Audio System (Session 6+)**
   - Sound effects (attacks, damage, pickups)
   - Background music
   - Volume controls

---

## Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Language | Python | 3.11.5 |
| Game Library | pygame | 2.6.0 |
| Package Manager | uv | 0.9.18 |
| Config | dataclasses | stdlib |
| Logging | logging | stdlib |
| Testing | pytest | 8.3.0+ |
| Linting | ruff | 0.8.0+ |
| Type Checking | mypy | 1.13.0+ |

---

## Performance Considerations

- **Target:** 60 FPS
- **Current:** Multiple zombies per wave, power-ups, sprites
  - Wave scaling: 3 → 150+ zombies over 100 waves
  - Frame-independent updates with delta_time
  - Pause optimization: screen capture instead of re-render
- **Logging Overhead:** DEBUG mode minimal impact (file I/O buffered)
- **Future:** Spatial partitioning for large entity counts (if needed)

---

## Key Patterns

1. **Game Loop Pattern** - Event/Update/Render cycle
2. **Component Pattern** - Entities self-contained (update/draw methods)
3. **Data-Driven Design** - Behavior controlled by config (dataclasses)
4. **Separation of Concerns** - Config/Entities/Systems/Logging
5. **State Machine Pattern** - Explicit game states with transitions
6. **Dual-Handler Logging** - Console (interactive) + File (archival)

---

## Architectural Principles

1. **Responsive Design** - UI scales with screen size (ratio-based)
2. **Frame Independence** - Movement unaffected by FPS (delta_time)
3. **Centralized Config** - No magic numbers in code (dataclasses)
4. **Simplicity First** - Solve current problems, not hypothetical ones
5. **Observability** - Comprehensive logging for debugging and playtest analysis
6. **Error Resilience** - Graceful degradation with logged warnings (no silent failures)

---

## Logging Architecture Details

### Handler Configuration

**Console Handler:**
- Level: WARNING+ (default) or DEBUG+ (GAME_DEBUG=1)
- Format: `[LEVEL] module: message`
- Output: stdout (real-time feedback)
- Purpose: Interactive debugging and warnings

**File Handler:**
- Level: DEBUG+ (always)
- Format: `timestamp [LEVEL] module: message`
- Output: `logs/game_YYYY-MM-DD_HHMMSS.log`
- Purpose: Full playtest history archiving

### Module Logging Pattern

Every module follows this pattern:
```python
from logger import get_logger

logger = get_logger(__name__)
```

This creates a logger named after the module (e.g., `entities.zombie`), allowing:
- Log filtering by module
- Clear source identification in log files
- Hierarchical logging control (future)

### Error Handling with Logging

Replace all silent error suppression with logged exceptions:

**Before:**
```python
with contextlib.suppress(OSError):
    save_file(data)
```

**After:**
```python
try:
    save_file(data)
    logger.info("File saved successfully")
except OSError as e:
    logger.warning(f"Failed to save file: {e}")
```

This ensures:
- All errors are tracked
- Debugging is easier (check log files)
- Playtest issues are discoverable
- Production bugs have context

---

**Last Updated:** Session 4.5 (Logging system, power-ups, sprites)
