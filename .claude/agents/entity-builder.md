# Entity Builder Subagent

Auto-generate pygame entity classes following this project's established patterns, conventions, and best practices.

## Purpose

Generate new entity classes (enemies, projectiles, pickups, etc.) that:
- Follow project structure and conventions
- Use centralized config dataclasses
- Include sprite loading with fallbacks
- Implement logging for lifecycle events
- Have proper update() and render() methods
- Are testable with python-testing skill

## What This Agent Does

1. **Analyzes existing entities** to understand patterns:
   - `src/entities/player.py` - Movement, rotation, sprite handling
   - `src/entities/zombie.py` - AI, chasing behavior
   - `src/entities/powerup.py` - Lifetime, collision, effects

2. **Studies project conventions**:
   - Config dataclasses in `src/config.py`
   - Logging patterns from `src/logger.py`
   - Sprite loading from `src/utils.py`
   - Frame-independent movement (delta_time)

3. **Generates complete entity** with:
   - Config dataclass in `src/config.py`
   - Entity class in `src/entities/<name>.py`
   - Proper imports and logging
   - update(), render(), and helper methods
   - Integration points for game loop

4. **Creates tests** (using python-testing skill):
   - Unit tests in `tests/entities/test_<name>.py`
   - Fixtures in `tests/conftest.py` if needed

## How to Invoke

```
Use the Task tool with subagent_type='general-purpose' and resume this agent:

Task(
  description="Generate <EntityName> entity",
  prompt="""
  Generate a new entity following entity-builder patterns:

  Entity: <EntityName> (e.g., Projectile, PowerUp, Boss)
  Purpose: <what it does>
  Behavior: <how it moves/acts>
  Properties: <key attributes>

  Requirements:
  - Follow patterns from existing entities (player.py, zombie.py, powerup.py)
  - Create config dataclass in config.py
  - Use sprite loading from utils.py
  - Add logging for lifecycle events
  - Frame-independent movement with delta_time
  - Include circle collision if needed

  Reference:
  - .claude/agents/entity-builder.md (this file)
  - .claude/skills/pygame-patterns/ (pygame patterns)
  """,
  subagent_type='general-purpose'
)
```

## Entity Generation Checklist

### 1. Config Dataclass (src/config.py)

```python
@dataclass
class <EntityName>Config:
    """<EntityName> entity settings"""
    # Movement
    speed: float = <value>       # Pixels per second

    # Visual
    radius: int = <value>        # Collision radius
    color: tuple = (<r>, <g>, <b>)
    sprite_path: str = "assets/sprites/<name>.png"

    # Behavior-specific attributes
    <other_fields>: <type> = <default>

# Add to global instances at bottom
<entity_name>_config = <EntityName>Config()
```

### 2. Entity Class (src/entities/<name>.py)

```python
"""<EntityName> entity for <purpose>."""

import math
import pygame
from logger import get_logger
from config import <entity_name>_config
from utils import load_sprite

logger = get_logger(__name__)


class <EntityName>:
    """<Description of entity>."""

    def __init__(self, x: float, y: float, <other_params>):
        """Initialize <entity> at position.

        Args:
            x: Initial X position
            y: Initial Y position
            <other_params>: <descriptions>
        """
        # Position
        self.x = x
        self.y = y

        # Config
        self.config = <entity_name>_config

        # Sprite
        self.sprite_image = load_sprite(
            self.config.sprite_path,
            self.config.radius * 2
        )
        self.original_sprite = self.sprite_image  # For rotation if needed

        # State
        self.alive = True
        <other_state>

        logger.debug(f"<EntityName> created at ({int(x)}, {int(y)})")

    def update(self, delta_time: float) -> None:
        """Update entity state.

        Args:
            delta_time: Time since last frame (seconds)
        """
        if not self.alive:
            return

        # Movement (frame-independent)
        self.x += self.velocity_x * delta_time
        self.y += self.velocity_y * delta_time

        # Behavior update
        <behavior_logic>

    def render(self, screen) -> None:
        """Render entity to screen.

        Args:
            screen: Pygame surface to draw on
        """
        if not self.alive:
            return

        if self.sprite_image:
            # Sprite rendering
            rect = self.sprite_image.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(self.sprite_image, rect)
        else:
            # Fallback circle
            pygame.draw.circle(
                screen,
                self.config.color,
                (int(self.x), int(self.y)),
                self.config.radius
            )

    def check_collision(self, other_x: float, other_y: float, other_radius: int) -> bool:
        """Check circle collision with another entity.

        Args:
            other_x: Other entity X position
            other_y: Other entity Y position
            other_radius: Other entity collision radius

        Returns:
            True if entities are colliding
        """
        dx = self.x - other_x
        dy = self.y - other_y
        distance = math.sqrt(dx * dx + dy * dy)
        return distance < (self.config.radius + other_radius)
```

### 3. Tests (tests/entities/test_<name>.py)

Use **python-testing** skill to generate:
- Test initialization
- Test update() with delta_time
- Test collision detection
- Test lifecycle (spawning, death)
- Parametrized tests for edge cases

### 4. Integration (src/game.py)

Add to game loop:
```python
# In Game.__init__()
self.<entities> = []

# In Game.update()
for entity in self.<entities>:
    entity.update(delta_time)

# In Game.render()
for entity in self.<entities>:
    entity.render(self.screen)
```

## Pattern References

### Movement Patterns
- **Static**: No movement (powerup.py)
- **Velocity-based**: Constant direction (projectile - see pygame-patterns/projectiles.md)
- **Chase AI**: Follow target (zombie.py:76-95)
- **WASD Control**: Player input (player.py:101-127)

### Sprite Patterns
- **Load with fallback**: utils.py:10-27
- **Rotation**: player.py:237-254 (rotate from original_sprite)
- **Circle fallback**: All entities have this

### Collision Patterns
- **Circle collision**: Pythagorean distance check
- **Used in**: Player-zombie, player-powerup, projectile-zombie

### Lifecycle Patterns
- **Alive flag**: Set to False, caller removes
- **Logging**: Debug spawn/death events
- **Cleanup**: Remove when not alive (game loop iterates over copy)

## Example Invocations

### Generate Projectile Entity

```
Generate a Projectile entity:
- Spawns at player position with angle
- Moves in straight line at constant velocity
- Circular collision with zombies
- Despawns after lifetime or hit
- Uses ProjectileConfig from config.py

Reference pygame-patterns/projectiles.md for verified patterns.
```

### Generate Boss Entity

```
Generate a Boss zombie entity:
- Larger radius and more health than normal zombie
- Slower movement speed
- Chase player (like normal zombie)
- Uses BossConfig from config.py
- Different sprite (zombie2 from Kenney assets)
```

### Generate Pickup Entity

```
Generate an Ammo pickup entity:
- Static position (doesn't move)
- Circular collision with player
- Despawns after lifetime with blink warning
- Uses PickupConfig from config.py
- Similar pattern to powerup.py
```

## Integration with Other Skills

### pygame-patterns Skill
Reference when generating:
- Projectile movement → patterns/projectiles.md
- Angle/velocity conversion
- Collision detection
- Frame-independent movement

### python-testing Skill
After generating entity:
- Use skill to create comprehensive tests
- Test movement, collision, lifecycle
- Parametrize edge cases

### game-artist Skill
For sprite assets:
- Search Kenney collection for sprites
- Generate if not available
- Follow sprite loading pattern from utils.py

## Quality Standards

Generated entities must:
- ✅ Use config dataclass (no hardcoded values)
- ✅ Include logging (spawn, death, state changes)
- ✅ Load sprite with fallback to circle
- ✅ Frame-independent movement (delta_time)
- ✅ Follow naming conventions (CamelCase class, snake_case vars)
- ✅ Include docstrings (Google style)
- ✅ Handle pygame Y-axis inversion correctly
- ✅ Use type hints where appropriate
- ✅ Be testable (pure functions, injectable config)

## Common Entity Types

| Entity Type | Movement | Collision | Lifetime | Example |
|-------------|----------|-----------|----------|---------|
| Projectile | Velocity | Circle | Timed | Bullet, arrow |
| Enemy | AI/Chase | Circle | Until death | Zombie, boss |
| Pickup | Static | Circle | Timed | Health, ammo |
| Player | Input | Circle | Persistent | Main character |
| Obstacle | Static | Rectangle | Persistent | Wall, barrier |

## Verification Checklist

Before finalizing generated entity:
- [ ] Config dataclass added to config.py
- [ ] Global config instance created
- [ ] Entity imports config correctly
- [ ] Sprite loading uses utils.py:load_sprite()
- [ ] Logging added for key events
- [ ] update() uses delta_time correctly
- [ ] render() handles sprite and fallback
- [ ] check_collision() uses circle math
- [ ] Docstrings follow Google style
- [ ] Tests generated (or planned with python-testing)

## Example Output

When invoked, the agent should:

1. **Read existing patterns**:
   - Read src/entities/player.py
   - Read src/entities/zombie.py
   - Read src/entities/powerup.py
   - Read src/config.py
   - Read .claude/skills/pygame-patterns/patterns/projectiles.md

2. **Generate config**:
   - Add dataclass to config.py
   - Create global instance

3. **Generate entity class**:
   - Create src/entities/<name>.py
   - Follow established patterns
   - Include all methods

4. **Suggest integration**:
   - Where to add to game.py
   - How to spawn/manage
   - Collision handling

5. **Recommend tests**:
   - Invoke python-testing skill
   - List test cases needed
