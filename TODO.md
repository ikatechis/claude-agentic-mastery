# TODO - Zombie Survival Game

**Last Updated:** Session 2.5 (COMPLETE) - December 25, 2024

## Session 2 Tasks ✅ COMPLETE

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

- [x] Create ARCHITECTURE.md documenting game structure
- [x] Implement melee combat system
  - [x] SPACE key to attack
  - [x] Attack range (50 pixels)
  - [x] Attack cooldown (0.5 seconds)
  - [x] Kill zombies in attack range
- [x] Implement zombie spawning system
  - [x] Multiple zombies (3 initial zombies)
  - [x] Random spawn positions off-screen (all 4 sides)
  - [ ] Wave-based spawning (progressive difficulty) - DEFERRED to Session 3

## Session 2.5 Tasks ✅ COMPLETE

### Modern Development Tooling
- [x] Ruff linting + formatting
- [x] mypy type checking
- [x] pytest with 6 initial tests (43% coverage)
- [x] pytest-cov for coverage reporting
- [x] pre-commit hooks (automated quality checks)
- [x] GitHub Actions CI/CD pipeline
- [x] Dependabot for dependency updates
- [x] .editorconfig for editor consistency
- [x] Code refactored with guard clauses
- [x] All type hints fixed for mypy compliance

## Session 3 Tasks (Next Up)

### Game Features
- [ ] Wave-based zombie spawning system (progressive difficulty)
- [ ] Score/kill counter display
- [ ] Game states system (Menu, Playing, Game Over)
- [ ] Restart functionality (game over screen)
- [ ] Increase test coverage beyond 43%

### Agentic Concepts to Learn
- [ ] Context management techniques
- [ ] Advanced verification protocols
- [ ] Documentation patterns (update PROGRESS.md)

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
