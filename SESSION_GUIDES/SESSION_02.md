# Session 02: Zombies & Combat

**Phase:** 1 - Foundation
**Duration:** 2-3 hours
**Prerequisites:** Session 1 completed

## Goals

- ✅ Zombie spawning system
- ✅ Zombie AI (moves toward player)
- ✅ Basic collision detection
- ✅ Melee combat system
- ✅ Health and damage
- ✅ ARCHITECTURE.md with verification protocols

## 🔒 Verification Protocol

**Before ALL code:**
1. Search pygame 2.5.2 docs
2. Verify AI movement calculations
3. Confirm collision methods
4. State: ✅ VERIFIED or ⚠️ UNCERTAIN

## Part 1: ARCHITECTURE.md (20 min)

```
> Create ARCHITECTURE.md documenting:
> 1. Game loop structure
> 2. Entity pattern (Player, Zombie, all inherit base)
> 3. File organization
> 4. Systems overview (collision, combat, spawning)
>
> MUST verify:
> - Search pygame sprite group patterns
> - Verify entity architecture best practices
> - Document verification sources
```

## Part 2: Zombie Class (45 min)

```
> Create Zombie class in src/entities/zombie.py:
> - Red circle visual
> - Spawns at random position offscreen
> - Moves toward player (AI)
> - Speed: 80 pixels/second (slower than player)
>
> VERIFICATION REQUIRED:
> - Search pygame vector math for movement toward target
> - Verify angle/direction calculation
> - Check pygame.math.Vector2 if using it
```

**Testing:**
- [ ] Zombies spawn around screen edges
- [ ] Zombies move toward player
- [ ] Multiple zombies can exist
- [ ] Zombies don't move too fast

## Part 3: Collision Detection (45 min)

```
> Add collision detection in game.py:
> - Detect player-zombie collision
> - For now, just remove zombie on collision
> - Later we'll add damage
>
> MUST VERIFY:
> - Search pygame.sprite.spritecollide() docs
> - Verify parameters and return value
> - Confirm dokill parameter usage
```

## Part 4: Melee Combat (45 min)

```
> Add simple melee attack:
> - SPACE key to attack
> - Attack range: 50 pixels
> - Kills zombies in range
> - 0.5 second cooldown between attacks
>
> VERIFY:
> - pygame.time.get_ticks() for cooldown
> - Distance calculation methods
> - Best practice for attack cooldown
```

## Part 5: Health System (30 min)

```
> Add health to player:
> - Start with 100 health
> - Lose 10 health per zombie collision
> - Display health in top-left
> - Game over at 0 health
>
> VERIFY:
> - pygame.font.Font usage
> - Text rendering methods
> - Health bar rendering (if visual)
```

## Verification Checklist

- [ ] All pygame functions verified in docs
- [ ] Version compatibility checked
- [ ] Confidence levels stated
- [ ] No guessed API syntax

## What You Learned

- ARCHITECTURE.md documentation
- AI movement calculations
- Collision detection systems
- Combat mechanics
- **Continued verification discipline**

**Next:** Session 3 - Skills & Context Management
