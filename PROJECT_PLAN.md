# Pygame Agentic Coding Mastery Project

**Goal:** Build a complete zombie survival game using pygame while learning ALL agentic coding best practices through hands-on, iterative development.

**Duration:** 10-15 sessions (2-3 hours each)

**Philosophy:** Learn by building. Each phase introduces new concepts while creating a real, playable game.

---

## 🎮 Project Overview

You will build a **Top-Down Zombie Survival Game** with progressively increasing complexity:
- Phase 1-2: Basic game mechanics (player, zombies, combat)
- Phase 3-4: Advanced features (weapons, waves, resources)
- Phase 5-6: Polish and production (effects, sounds, UI)
- Phase 7-8: Optimization and deployment

**Why Zombie Survival?**
- Engaging and fun to develop
- Natural progression of features
- Visual feedback keeps it exciting
- Complex enough for real-world patterns
- Popular game genre - great portfolio piece

---

## 🔒 CRITICAL: Verification Protocol

**⚠️ MANDATORY FOR ALL SESSIONS ⚠️**

Before suggesting ANY code, command, function signature, flag, parameter, or technical implementation:

### **1. Always Search Official Documentation**

```
BEFORE writing code:
> Use web_search to verify [library] [version] documentation
> Check official docs for correct syntax
> Verify function signatures
> Confirm parameter names
> Validate flag options
```

**Examples:**
```
❌ BAD: "Use pygame.sprite.Group.draw()"
✅ GOOD: [Search pygame 2.5.2 docs] "pygame.sprite.Group has draw() method confirmed"

❌ BAD: "Use --config flag"
✅ GOOD: [Search tool docs] "Verified: command uses --config-file flag, not --config"

❌ BAD: "Create .claude.yaml"
✅ GOOD: [Search Claude Code docs] "Verified: file should be .claude/settings.json"
```

### **2. Check @pyproject.toml for Versions**

```
ALWAYS before suggesting library code:
> Read @pyproject.toml [project.dependencies]
> Note exact version (e.g., pygame==2.5.2)
> Search "[library] [version] documentation"
> Use ONLY APIs available in that version
```

### **3. State Your Confidence Level**

Every technical suggestion must include:
```
✅ VERIFIED: [source] - Checked official docs
⚠️ UNCERTAIN: Will verify with web_search
❌ GUESSING: Let me search the docs first
```

**Never guess. Always verify.**

### **4. For Configuration Files**

Before creating any config file (.json, .yaml, .md, etc.):
```
1. Search for official template/schema
2. Check exact field names
3. Verify syntax requirements
4. Confirm file location
5. Show source of information
```

**Examples:**
```
✅ "Searched Claude Code docs - .mcp.json schema requires 'mcpServers' (camelCase)"
✅ "Verified pygame.sprite.Sprite requires super().__init__() call"
✅ "Checked Python 3.10 docs - match/case syntax supported"
```

### **5. Verification Checklist (Every Session)**

Before each code block:
- [ ] Searched official documentation?
- [ ] Verified function/method exists?
- [ ] Confirmed correct parameters?
- [ ] Checked version compatibility?
- [ ] Stated confidence level?

**This prevents:**
- Hallucinated APIs
- Wrong flag names
- Outdated syntax
- Invalid config formats
- Hours of debugging

---

## Learning Objectives by Phase

### Phase 1: Foundation (Sessions 1-2) ✅ COMPLETE
**Concepts Learned:**
- ✅ Basic project structure
- ✅ Git workflow with Claude Code
- ✅ CLAUDE.md with verification protocols
- ✅ Manual testing workflow
- ✅ Documentation-first approach

**What You've Built:**
- ✅ Basic game window (800x600)
- ✅ Player character with WASD movement
- ✅ Top-down camera view
- ✅ Zombie spawning system (off-screen, random sides)
- ✅ Circle-based collision detection
- ✅ Centralized configuration system

---

### Phase 2: Process & Documentation (Sessions 3-4.5) ✅ COMPLETE
**Concepts Learned:**
- ✅ Modern development tooling (ruff, mypy, pytest)
- ✅ Pre-commit hooks + GitHub Actions CI/CD
- ✅ Test infrastructure and code quality automation
- ✅ Dataclass-based configuration patterns
- ✅ State machine architecture
- ✅ Verification protocols in practice
- ✅ Professional logging system (dual-output, debug mode)
- ✅ MCP integration (ref.tools, GitHub, Pollinations)
- ✅ Skills creation (python-testing, game-artist)

**What You've Built:**
- ✅ Melee combat system (player attacks zombies)
- ✅ Health and damage system
- ✅ Score/kill counter with persistent high score
- ✅ Game states (MENU, PLAYING, PAUSED, GAME_OVER)
- ✅ Wave system (exponential scaling)
- ✅ Power-up system (Health, Speed, Shield)
- ✅ Sprite integration with rotation
- ✅ Logging system with GAME_DEBUG mode

---

### Phase 3: Agentic Tools Basics (Sessions 5-6) 🔄 IN PROGRESS
**Concepts to Learn:**
- 🆕 Your first custom Skill (pygame-patterns)
- 🆕 Your first custom Subagent (entity-builder)
- ✅ Permission management (review existing skills)
- ✅ Project-scoped MCP configuration (already have 3 MCPs)
- ✅ Skills with verification (python-testing, game-artist)

**What You'll Build:**
- Weapon system (PISTOL, then SHOTGUN/RIFLE)
- Ranged combat (mouse aim + shooting)
- Ammunition system (ammo tracking, reload)
- Projectile entity (bullets with collision)
- Resource pickups (AMMO power-up)
- Multiple zombie types (Normal, Fast, Tank)

---

### Phase 4: Advanced Agents (Sessions 7-8)
**Concepts Learned:**
- ✅ Multiple specialized subagents
- ✅ Code reviewer subagent
- ✅ Test automation subagent
- ✅ Agent orchestration
- ✅ Context isolation patterns

**What You'll Build:**
- Boss zombies with special abilities
- Environmental hazards
- Barricade/defense building
- Day/night cycle
- Survival timer

---

### Phase 5: MCP Integration (Sessions 9-10)
**Concepts Learned:**
- ✅ GitHub MCP for PR creation
- ✅ ref.tools MCP for documentation lookup
- ✅ MCP server configuration
- ✅ API token management

**What You'll Build:**
- Sound effects (zombie groans, gunshots)
- Background music
- Particle effects (blood, muzzle flash)
- Screen shake and visual feedback
- Hit markers

---

### Phase 6: Production Polish (Sessions 11-12)
**Concepts Learned:**
- ✅ Hooks for automation
- ✅ Slash commands for workflows
- ✅ Advanced CLAUDE.md patterns
- ✅ Progressive disclosure with .claude/rules/
- ✅ Production verification protocols

**What You'll Build:**
- Main menu with options
- Pause system
- Upgrade system between waves
- High score persistence
- Settings (volume, difficulty)

---

### Phase 7: Optimization & Testing (Sessions 13-14)
**Concepts Learned:**
- ✅ Performance profiling
- ✅ Test-driven development with agents
- ✅ Automated testing workflows
- ✅ Bug tracking patterns

**What You'll Build:**
- Performance optimizations
- Comprehensive test suite
- Bug fixes and polish
- Balance adjustments
- Gameplay refinements

---

### Phase 8: Deployment (Session 15)
**Concepts Learned:**
- ✅ GitHub releases with MCP
- ✅ Documentation generation
- ✅ README automation
- ✅ Project retrospective

**What You'll Build:**
- Packaged game executable
- Complete documentation
- GitHub release
- Portfolio entry

---

## Session Structure

Each session follows this pattern:

### 1. Review (5 minutes)
- Read PROGRESS.md from last session
- Check TODO.md for next tasks
- Quick demo of what we built

### 2. Concept Introduction (10 minutes)
- Learn ONE new agentic concept
- Understand why it's useful
- See practical examples

### 3. Implementation (90-120 minutes)
- Build the feature using new concept
- **VERIFY before coding** (search docs)
- Iterate and refine
- Test immediately

### 4. Reflection (10 minutes)
- Update PROGRESS.md
- Update TODO.md
- Commit working code
- Note lessons learned

---

## File Structure

```
pygame-agentic-mastery/
├── PROJECT_PLAN.md              # This file - master plan
├── SESSION_GUIDES/              # Detailed guides per session
│   ├── SESSION_01.md           # Phase 1, Session 1
│   ├── SESSION_02.md           # Phase 1, Session 2
│   └── ...
├── CLAUDE.md                    # Main project instructions + verification
├── ARCHITECTURE.md              # Code structure
├── TODO.md                      # Task list
├── PROGRESS.md                  # What we've built
├── VERIFICATION.md              # Verification checklist
├── .python-version              # Python version (pyenv)
├── pyproject.toml               # Project config & dependencies (uv)
├── uv.lock                      # Locked dependency versions (uv)
├── .claude/
│   ├── agents/                 # Subagents
│   │   ├── entity-builder.md
│   │   ├── code-reviewer.md
│   │   └── test-runner.md
│   ├── commands/               # Slash commands
│   │   ├── test-feature.md
│   │   └── commit-feature.md
│   ├── rules/                  # Progressive disclosure
│   │   ├── entities.md
│   │   └── systems.md
│   └── skills/                 # Project skills
│       └── pygame-patterns/
│           └── SKILL.md
├── .mcp.json                   # MCP configuration
├── src/
│   ├── main.py                 # Game entry point
│   ├── game.py                 # Main game loop
│   ├── entities/               # Game entities
│   │   ├── __init__.py
│   │   ├── player.py
│   │   ├── zombie.py
│   │   └── weapon.py
│   ├── systems/                # Game systems
│   │   ├── __init__.py
│   │   ├── collision.py
│   │   ├── combat.py
│   │   └── spawning.py
│   └── utils/                  # Utilities
│       ├── __init__.py
│       └── constants.py
├── tests/
│   ├── test_entities.py
│   └── test_systems.py
├── assets/
│   ├── images/
│   ├── sounds/
│   └── fonts/
├── README.md
└── .gitignore
```

---

## Important Principles

### 1. Verification First
- **ALWAYS** search official docs before coding
- **NEVER** guess API signatures
- **STATE** your confidence level
- **CHECK** requirements.txt versions

### 2. Iterative Learning
- Learn ONE concept per session
- Practice immediately
- Verify, then code
- Reflect before moving on

### 3. Working Code First
- Every session ends with working code
- Test before committing
- Commit working features
- No half-finished features

### 4. Documentation as You Go
- Update docs in real-time
- Keep PROGRESS.md current
- Maintain TODO.md
- Update verification checklist

### 5. Test Immediately
- Run game after each change
- Test features hands-on
- Verify APIs work as documented
- Don't trust code without testing

### 6. Context Management
- Use /compact when at 70% context
- Start fresh sessions for new features
- Keep conversations focused
- Monitor with Shift+Tab

---

## Expected Outcomes

By the end of this project, you will:

✅ **Technical Skills:**
- Built a complete pygame zombie survival game
- Understand game architecture patterns
- Handle collision, AI, combat systems
- Implement procedural spawning and waves

✅ **Agentic Coding Skills:**
- Set up and use Skills effectively
- Create and orchestrate Subagents
- Configure and use MCP servers
- Manage context strategically
- Use hooks and slash commands
- Optimize CLAUDE.md
- Follow proper git workflows

✅ **Verification Skills:**
- Always check documentation first
- Never guess technical details
- State confidence levels
- Search before suggesting

✅ **Best Practices:**
- Document architecture decisions
- Track progress systematically
- Test iteratively
- Commit strategically
- Review code with agents
- Manage large codebases

✅ **Portfolio:**
- Playable zombie survival game on GitHub
- Professional documentation
- GitHub releases
- Shareable project

---

## Success Metrics

**After each session, you should be able to:**
- ✅ Explain the concept you learned
- ✅ Show working code using the concept
- ✅ Run the game and demonstrate progress
- ✅ Point to where you applied verification
- ✅ Prove you checked documentation

**After the full project:**
- ✅ Create subagents from scratch
- ✅ Configure MCP servers confidently
- ✅ Manage large project context
- ✅ Use Claude Code efficiently for ANY project
- ✅ Have a portfolio piece
- ✅ Always verify before coding

---

## Verification Protocol Summary

**Before EVERY coding decision:**

1. 🔍 **Search** official documentation
2. 📋 **Check** @pyproject.toml for versions
3. ✅ **Verify** function signatures and parameters
4. 📝 **State** confidence level
5. 🎯 **Source** your information

**Never:**
- ❌ Guess API names
- ❌ Assume parameter syntax
- ❌ Use outdated examples
- ❌ Skip version checking
- ❌ Claim certainty without verification

**Always:**
- ✅ Search first
- ✅ Verify with sources
- ✅ State "Verified:" or "Uncertain:"
- ✅ Show documentation links
- ✅ Test immediately

---

## Next Steps

1. **Read this entire document**
2. **Read SESSION_01.md**
3. **Understand verification requirements**
4. **Start Session 1**
5. **Have fun building!**

Remember: This is a learning journey. The verification protocol might feel slow at first, but it teaches you to build with confidence and accuracy. Make mistakes, experiment, verify, and ask questions. The goal is to master agentic coding through practice while building a game you can be proud of.

Let's build something awesome! 🧟‍♂️🎮
