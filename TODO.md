# TODO - Zombie Survival Game

**Last Updated:** Session 2 (70% Complete)

## Session 2 Tasks (Ongoing - 70% Complete)

### Completed ✅
- [x] Create centralized config system (src/config.py)
  - [x] GameConfig dataclass
  - [x] PlayerConfig dataclass
  - [x] ZombieConfig dataclass
  - [x] UIConfig dataclass with responsive positioning
- [x] Add Zombie entity (src/entities/zombie.py)
  - [x] Zombie class (red circle, slower than player)
  - [x] Chase AI (vector-based movement toward player)
- [x] Implement zombie AI
  - [x] Calculate direction to player
  - [x] Normalize movement vector
  - [x] Frame-independent movement
- [x] Add collision detection
  - [x] Circle-based collision (math.sqrt distance)
  - [x] check_collision() method in game.py
- [x] Add health system
  - [x] Player starts with 100 health
  - [x] take_damage() method with cooldown
  - [x] Damage cooldown (1 second)
  - [x] Lose 10 health per zombie collision
  - [x] Display health bar (responsive, ratio-based)
  - [x] Game over at 0 health
- [x] Upgrade pygame 2.5.2 → 2.6.0
- [x] Add ref.tools MCP server for docs lookup
- [x] **VERIFIED** all pygame APIs before implementing ✅

### Remaining ❌
- [ ] Create ARCHITECTURE.md documenting game structure
- [ ] Implement melee combat system
  - [ ] SPACE key to attack
  - [ ] Attack range (50 pixels)
  - [ ] Attack cooldown (0.5 seconds)
  - [ ] Kill zombies in attack range
- [ ] Implement zombie spawning system
  - [ ] Multiple zombies (currently only 1 hardcoded)
  - [ ] Random spawn positions off-screen
  - [ ] Wave-based spawning (progressive difficulty)

## Future Sessions
- Session 3: Skills creation, Subagents introduction
- Session 4+: Advanced features, MCP integration
- (Will be filled in as we progress)

## Completed ✓

### Session 1 - Foundation (Complete)
- [x] Set up Python 3.11.5 with pyenv
- [x] Install and configure uv package manager
- [x] Add pygame==2.5.2 dependency
- [x] Create project structure (src/, entities/)
- [x] Initialize git repository
- [x] Create game window (800x600, 60 FPS)
- [x] Add player character (green circle)
- [x] Implement WASD movement (8-directional)
- [x] Frame-independent movement (delta_time)
- [x] Player boundary checking
- [x] Diagonal movement normalization
- [x] Create CLAUDE.md with VERIFICATION PROTOCOL ⭐
- [x] Make first git commit
- [x] Create .gitignore
- [x] Establish verification-first workflow
