# Zombie Survival Game

**A top-down zombie survival game built with pygame - learning project for mastering agentic coding with Claude Code**

## Quick Start

```bash
# Prerequisites: Python 3.11.5 (via pyenv) + uv package manager

# Clone and run
git clone <your-repo-url>
cd claude-agentic-mastery
uv sync
uv run python src/main.py
```

## Current Features

### Core Gameplay
- **Player Movement** - WASD controls with smooth sprite rotation
- **Zombie AI** - Chase behavior with pathfinding toward player
- **Combat System** - Melee attacks with 50px range and cooldown
- **Health System** - 100 HP with damage cooldown and visual health bar
- **Collision Detection** - Circle-based physics

### Progression
- **Wave-Based Spawning** - Progressive difficulty with increasing zombies
- **Score System** - Kill counter with high score tracking
- **Game States** - Menu, Playing, Game Over with restart

### Power-Ups (Session 4)
- **Health Pack** - Restores 30-50 HP (green)
- **Speed Boost** - 1.5x movement for 5-10 seconds (cyan)
- **Shield** - Blocks 3 hits (gold)
- **Drop System** - 20% chance on zombie kill
- **Visual Indicators** - Active effect displays

### Visual Polish
- **Sprite Integration** - Professional Kenney Topdown Shooter assets
- **Dynamic Rotation** - Sprites face movement/target direction
- **Background Tiling** - Textured ground plane
- **Visual Effects** - Kill flashes, damage popups, pickup animations

## Controls

| Key | Action |
|-----|--------|
| **WASD** | Move player |
| **SPACE** | Melee attack |
| **ESC** | Quit game |

## About This Project

This is a **learning project** focused on mastering agentic coding with Claude Code through building a complete game. The project demonstrates:

- **Verification-First Development** - Always verify APIs before coding
- **Multi-Agent Workflows** - Plan mode with parallel exploration
- **MCP Integration** - GitHub, ref.tools, Pollinations
- **Skills & Subagents** - Custom testing skills and agent composition
- **Modern Python Tooling** - ruff, mypy, pytest, pre-commit hooks

### What You'll Learn

**Agentic Coding Skills:**
- Skills (auto-invoked expertise)
- Subagents (isolated execution)
- MCP servers (GitHub, ref.tools, Pollinations)
- Hooks (automation)
- Slash commands
- Context management

**Critical Skill: Verification-First Development**
- Always search official docs before coding
- Verify function signatures and parameters
- Check library versions in pyproject.toml
- State confidence levels
- Never guess technical details

### Project Progress

**Completed Sessions:** 4 / 15 (27%)

| Session | Focus | Status |
|---------|-------|--------|
| **Session 1** | Foundation & verification protocol | ✅ Complete |
| **Session 2** | Zombies, collision, combat | ✅ Complete |
| **Session 2.5** | Modern dev tooling (ruff, mypy, pytest) | ✅ Complete |
| **Session 3** | Sprites, rotation, wave system | ✅ Complete |
| **Session 4** | Power-up system (multi-agent workflow) | ✅ Complete |
| Session 5+ | TBD | ⏳ Upcoming |

**Game Features Completion:** ~45%

Remaining features: Zombie variants, sound/music, particle effects, boss zombies, final polish

### Verification Protocol

**Before EVERY coding decision, we:**
1. Search official documentation (ref.tools MCP)
2. Verify function signatures and parameters
3. Check @pyproject.toml for exact versions
4. State confidence level ("VERIFIED" vs "UNCERTAIN")
5. Show verification source

**Never guess. Always verify.**

## Development

### Tech Stack

- **Language:** Python 3.11.5 (managed by pyenv)
- **Package Manager:** uv v0.9.18 (10-100x faster than pip)
- **Game Library:** pygame 2.6.0
- **Testing:** pytest 8.3.0 with 69% coverage (52 tests)
- **Linting:** ruff 0.8.0 (fast, Rust-based)
- **Type Checking:** mypy 1.13.0
- **CI/CD:** GitHub Actions + pre-commit hooks

### Project Structure

```
claude-agentic-mastery/
├── src/
│   ├── main.py              # Entry point
│   ├── game.py              # Game loop, event handling, rendering
│   ├── config.py            # Dataclass configuration
│   ├── utils.py             # Utility functions (sprite loading, etc.)
│   ├── game_state.py        # GameState enum (MENU, PLAYING, GAME_OVER)
│   └── entities/
│       ├── player.py        # Player with movement, combat, effects
│       ├── zombie.py        # Zombie AI with chase behavior
│       └── powerup.py       # Power-up system (health, speed, shield)
├── tests/
│   ├── test_player.py       # Player unit tests
│   ├── test_zombie.py       # Zombie unit tests
│   ├── test_powerup.py      # Power-up unit tests (19 tests)
│   ├── test_game.py         # Game integration tests
│   └── test_config.py       # Configuration tests
├── assets/
│   ├── sprites/             # Kenney Topdown Shooter sprites
│   └── kenney_packs/        # Asset pack files
├── .github/
│   └── workflows/ci.yml     # GitHub Actions CI/CD
├── .claude/
│   └── skills/              # Custom skills (python-testing)
├── pyproject.toml           # Dependencies and tool config
├── CLAUDE.md                # Project instructions for Claude
├── PROGRESS.md              # Detailed session logs
└── TODO.md                  # Task tracking
```

### Development Commands

```bash
# Run game
uv run python src/main.py

# Run tests
uv run pytest                # With coverage
uv run pytest -v             # Verbose output
uv run pytest -k test_name   # Run specific test

# Code quality
uv run ruff check src/       # Lint
uv run ruff format src/      # Format
uv run mypy src/             # Type check

# Pre-commit hooks
pre-commit install           # Set up hooks
pre-commit run --all-files   # Run manually
```

### Running Tests

The project has **52 passing tests** with **69% code coverage**:

```bash
uv run pytest --cov=src --cov-report=term-missing -v
```

**Coverage by module:**
- `config.py`: 100%
- `utils.py`: 100%
- `powerup.py`: 97%
- `zombie.py`: 96%
- `player.py`: 66%
- `game.py`: 14% (integration code, harder to test)

### Contributing

This is a learning project, but contributions are welcome! Please:
1. Follow the verification-first protocol (check CLAUDE.md)
2. Maintain test coverage (add tests for new features)
3. Run pre-commit hooks before committing
4. Use conventional commits (feat:, fix:, docs:, etc.)

## Assets

Sprites from **Kenney Topdown Shooter** pack (CC0 license):
- https://kenney.nl/assets/top-down-shooter
- 580 free assets (characters, tiles, objects)

Game Icons from **Kenney Game Icons** pack (CC0 license):
- https://kenney.nl/assets/game-icons

## License

CC0 / Public Domain - Free to use, modify, and distribute

## Links

- **Project Documentation:** See CLAUDE.md for detailed instructions
- **Progress Log:** See PROGRESS.md for session-by-session changes
- **Task Tracking:** See TODO.md for upcoming features

---

**Built with Claude Code** - Demonstrating verification-first agentic development
