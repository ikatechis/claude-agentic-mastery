# Architecture - Zombie Survival Game

**Version:** 0.2.0 | **Last Updated:** Session 2

---

## Overview

Top-down zombie survival game built with pygame. Architecture follows a classic game loop pattern with component-based entities and centralized configuration.

---

## Project Structure

```
src/
├── main.py              # Entry point
├── game.py              # Game loop orchestration
├── config.py            # Centralized configuration (dataclasses)
└── entities/
    ├── player.py        # Player character
    └── zombie.py        # Enemy entity
```

---

## Core Architecture

### Game Loop (game.py)

**Pattern:** Event → Update → Render

**Responsibilities:**
- Initialize pygame and window
- Handle input events
- Update entity state
- Check collisions
- Render entities and UI
- Manage game state

### Entities

**Player (entities/player.py)**
- Inherits `pygame.sprite.Sprite`
- Handles WASD movement
- Manages health and damage cooldown
- Renders as green circle

**Zombie (entities/zombie.py)**
- Simple chase AI using vector math
- Slower than player (escapable)
- Deals damage on collision
- Renders as red circle

### Configuration System (config.py)

**Pattern:** Dataclass-based configuration

**Why?**
- Eliminates magic numbers
- Provides type safety
- Centralizes game balance tuning
- Groups related settings

**Config Classes:**
- `GameConfig` - Screen, FPS, colors
- `PlayerConfig` - Player properties
- `ZombieConfig` - Enemy properties
- `UIConfig` - **Ratio-based UI positioning**

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
- **Type:** Circle-circle collision
- **Current Use:** Player-zombie damage
- **Future:** Projectiles, pickups, melee attacks

### Combat System
- **Current:** Passive damage on collision with cooldown
- **Planned:** Active melee attacks (SPACE key, attack range)

### UI System
- **Location:** `game.py::render_health_bar()`
- **Pattern:** Responsive rendering using UIConfig ratios
- **Current:** Health bar with background/foreground/text

---

## Game State

### Current States
- **Running:** Active gameplay
- **Game Over:** Player health ≤ 0

### Planned States
- Menu, Paused, Wave Complete

---

## Data Flow

```
Input (WASD, SPACE)
    ↓
Entities Update (movement, AI)
    ↓
Collision Detection
    ↓
Combat System (damage)
    ↓
UI Update (health display)
    ↓
Render to Screen
```

---

## Future Architecture

### Session 3+ Improvements

1. **Entity Management**
   - List-based zombie management
   - Dynamic add/remove

2. **Spawning System**
   - Random spawn positions off-screen
   - Wave-based difficulty progression

3. **System Separation**
   - `src/systems/collision.py`
   - `src/systems/combat.py`
   - `src/systems/spawning.py`

4. **State Machine**
   - Formal menu/playing/paused states
   - State transition logic

---

## Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Language | Python | 3.11.5 |
| Game Library | pygame | 2.6.0 |
| Package Manager | uv | 0.9.18 |
| Config | dataclasses | stdlib |

---

## Performance Considerations

- **Target:** 60 FPS
- **Current:** Single zombie (negligible overhead)
- **Future:** Multiple zombies → O(n) updates, may need spatial partitioning

---

## Key Patterns

1. **Game Loop Pattern** - Event/Update/Render cycle
2. **Component Pattern** - Entities self-contained
3. **Data-Driven Design** - Behavior controlled by config
4. **Separation of Concerns** - Config/Entities/Systems

---

## Architectural Principles

1. **Responsive Design** - UI scales with screen size
2. **Frame Independence** - Movement unaffected by FPS
3. **Centralized Config** - No magic numbers in code
4. **Simplicity First** - Solve current problems, not hypothetical ones

---

**Last Updated:** Session 2 (Zombies, collision, health system)
