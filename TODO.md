# TODO - Zombie Survival Game

**Last Updated:** Session 1 (Complete)

## Session 2 Tasks (Next)
- [ ] Create ARCHITECTURE.md documenting game structure
- [ ] Add zombie spawning system
  - [ ] Zombie class (red circle, slower than player)
  - [ ] Spawn at random positions off-screen
  - [ ] Multiple zombies at once
- [ ] Implement zombie AI (move toward player)
  - [ ] Calculate direction to player
  - [ ] Move zombies each frame
- [ ] Add collision detection
  - [ ] Player-zombie collision
  - [ ] Remove zombie on collision (temporary)
- [ ] Implement melee combat system
  - [ ] SPACE key to attack
  - [ ] Attack range (50 pixels)
  - [ ] Attack cooldown (0.5 seconds)
  - [ ] Kill zombies in range
- [ ] Add health system
  - [ ] Player starts with 100 health
  - [ ] Lose 10 health per zombie collision
  - [ ] Display health in top-left corner
  - [ ] Game over at 0 health
- [ ] **VERIFY all pygame APIs before implementing**

## Future Sessions
- Session 3+: Skills, Subagents, Advanced features
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
- [x] Create VERIFICATION.md checklist
- [x] Make first git commit
- [x] Create .gitignore
- [x] Establish verification-first workflow
