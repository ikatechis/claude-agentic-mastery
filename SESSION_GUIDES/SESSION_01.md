# Session 01: Foundation & First Code

**Phase:** 1 - Foundation
**Duration:** 2-3 hours
**Prerequisites:** Claude Code installed, basic Python knowledge

---

## Goals for This Session

By the end of Session 1, you will have:
- ✅ A working game window with top-down view
- ✅ Player character with WASD movement
- ✅ Your first CLAUDE.md file with verification protocol
- ✅ A git repository with initial commit
- ✅ Understanding of documentation-first workflow

---

## Concepts You'll Learn

### 1. Verification-First Development
- **ALWAYS** search official documentation before coding
- Check pygame version in pyproject.toml
- Verify function signatures and parameters
- State confidence level for every suggestion

### 2. Basic Claude Code Workflow
- Starting Claude Code in a project
- Using @ to reference files
- Testing code immediately
- Iterating on feedback with verification

### 3. Git with Claude
- Initializing repositories
- Making commits through Claude
- Writing good commit messages

### 4. CLAUDE.md Basics
- What goes in CLAUDE.md
- Including verification requirements
- Keeping it short and focused

---

## 🔒 CRITICAL: Verification Protocol for This Session

**Before writing ANY code, Claude MUST:**

1. Search pygame 2.5.2 documentation
2. Verify function/method signatures
3. Confirm parameter names
4. State: "✅ VERIFIED:" or "⚠️ Will verify:"

**Examples:**
```
❌ "Use pygame.display.set_mode()"
✅ "Searched pygame docs - pygame.display.set_mode((width, height)) confirmed"

❌ "The player should use update()"
✅ "Verified pygame.sprite.Sprite pattern - update() method is standard"
```

---

## Step-by-Step Guide

### Part 1: Project Setup (15 minutes)

**1. Create and navigate to project:**
```bash
mkdir ~/pygame-agentic-mastery
cd ~/pygame-agentic-mastery
```

**2. Initialize git:**
```bash
git init
```

**3. Start Claude Code:**
```bash
claude
```

**4. Tell Claude what we're building:**
```
> I want to build a top-down zombie survival game using pygame.
> This is Session 1, where we'll create:
> - A game window (800x600)
> - A player character that moves with WASD
> - Top-down camera perspective
> - Basic project structure
>
> IMPORTANT: You must follow strict verification protocols.
> Before suggesting ANY pygame code:
> 1. Search pygame 2.5.2 documentation
> 2. Verify the exact function/method signature
> 3. Confirm parameter names and types
> 4. State your confidence: "✅ VERIFIED:" or "⚠️ UNCERTAIN:"
>
> Never guess API names or parameters. Always verify first.
>
> Before we start coding, let's plan the file structure.
> What should we create first?
```

---

### Part 2: Initial File Structure (20 minutes)

**Expected from Claude:**
Claude should suggest something like:
```
pygame-agentic-mastery/
├── src/
│   ├── main.py       # Entry point
│   ├── game.py       # Main game class
│   └── player.py     # Player class
├── .python-version   # Python version (pyenv)
├── pyproject.toml    # Dependencies (uv)
└── README.md
```

**Then Claude should say:**
```
⚠️ Before creating pyproject.toml, I need to verify:
1. Current stable Python version
2. Current stable pygame version

[Searches official documentation]

✅ VERIFIED: Python 3.10+ recommended
✅ VERIFIED: Latest stable pygame is 2.5.2

I'll create:
- .python-version with 3.10
- pyproject.toml with pygame==2.5.2
```

**Your task:**
1. Review Claude's suggestion
2. **Ensure Claude searched docs before deciding versions**
3. Ask questions if anything is unclear
4. Approve the structure

**Tell Claude:**
```
> Looks good! Create .python-version and pyproject.toml first.
> Remember to search and verify the pygame version.
> Use: pyenv local 3.10 to create .python-version
> Use: uv init and uv add pygame==2.5.2
```

---

### Part 3: Create Basic Game Window (30 minutes)

**Tell Claude:**
```
> Create a basic pygame window that:
> 1. Opens at 800x600 resolution
> 2. Has a dark gray background (to look like ground)
> 3. Shows "Zombie Survival" as the window title
> 4. Runs at 60 FPS
> 5. Can be closed with the X button or ESC key
>
> Put this in src/main.py and src/game.py
>
> IMPORTANT VERIFICATION REQUIREMENTS:
> Before writing ANY pygame code, you MUST:
> 1. Search "pygame 2.5.2 documentation" for each function
> 2. Verify the exact syntax
> 3. State: "✅ VERIFIED: pygame.display.set_mode() takes (width, height) tuple"
>
> Do NOT guess function names or parameters.
```

**What Claude should do:**
```
I'll create the game window. First, let me verify the pygame APIs I'll use:

[Searches pygame 2.5.2 documentation]

✅ VERIFIED: pygame.init() - initializes all pygame modules
✅ VERIFIED: pygame.display.set_mode((width, height)) - creates window
✅ VERIFIED: pygame.display.set_caption(title) - sets window title
✅ VERIFIED: pygame.time.Clock() - creates clock for FPS control
✅ VERIFIED: clock.tick(fps) - limits frame rate

Now I'll create the files...
```

**If Claude doesn't verify first:**
```
> STOP. Before writing code, you MUST search pygame 2.5.2 docs and verify:
> 1. pygame.display.set_mode() signature
> 2. pygame.time.Clock.tick() usage
> 3. Any other pygame functions you'll use
>
> State your verification results before proceeding.
```

**After Claude creates the code:**

1. **Review the code:**
   - Did Claude verify functions first?
   - Does code look reasonable?
   - Do you understand what each part does?

2. **Test it:**
```
> Run the game so I can test it
```

3. **Verify:**
   - Black/dark gray window appears?
   - Title is correct?
   - ESC key closes it?
   - X button works?

4. **If something's wrong:**
```
> The window closes immediately / doesn't respond / [describe issue]
> Search pygame docs to find the correct approach, then fix this.
```

---

### Part 4: Add Player Character (45 minutes)

**Tell Claude:**
```
> Now let's add a player character:
> 1. Create a Player class in src/player.py
> 2. For now, draw a simple green circle to represent the survivor
> 3. Position it at the center of the screen
> 4. It should move with WASD keys (top-down movement)
> 5. Movement should be in 8 directions (diagonal movement allowed)
> 6. Keep the player inside screen boundaries
> 7. Movement speed should feel responsive (around 200 pixels/second)
>
> Update game.py to create and render the player
>
> VERIFICATION REQUIREMENTS:
> You MUST search and verify:
> - pygame.sprite.Sprite class structure
> - pygame.draw.circle() signature and parameters
> - pygame.key.get_pressed() usage
> - Movement with delta_time for frame independence
>
> Show your verification results before writing code.
```

**What Claude should do:**
```
I'll create the player system. First, let me verify the pygame APIs:

[Searches pygame 2.5.2 documentation]

✅ VERIFIED: pygame.sprite.Sprite base class requires super().__init__()
✅ VERIFIED: pygame.draw.circle(surface, color, center, radius) signature
✅ VERIFIED: pygame.key.get_pressed() returns dict of key states
✅ VERIFIED: K_w, K_a, K_s, K_d are the key constants
✅ VERIFIED: delta_time in seconds, multiply by speed for frame-independence

Creating player code now...
```

**Testing checklist:**
```
> After you create the player code, run the game.
> I need to verify:
> - [ ] Player appears as a green circle at center
> - [ ] W key moves player up
> - [ ] S key moves player down
> - [ ] A key moves player left
> - [ ] D key moves player right
> - [ ] Diagonal movement works (W+A, etc.)
> - [ ] Player doesn't go off screen edges
> - [ ] Movement feels smooth (not jerky)
```

**Common issues and fixes:**

| Issue | How to fix |
|-------|-----------|
| Movement too fast | "Search docs for delta_time usage, adjust speed constant" |
| Movement too slow | "Verify speed calculation, increase if needed" |
| Jerky movement | "Check that we're using delta_time correctly per pygame docs" |
| Player goes off screen | "Verify boundary checking logic" |
| Diagonal too fast | "Search for vector normalization in pygame/math docs" |

---

### Part 5: Create CLAUDE.md with Verification Protocol (20 minutes)

**Tell Claude:**
```
> Let's create a CLAUDE.md file for this project.
> Include:
> 1. Tech stack (Python 3.10+, pygame==2.5.2, managed by pyenv + uv)
> 2. How to run the game (uv run python src/main.py)
> 3. Current architecture (what each file does)
> 4. MANDATORY verification protocol
>
> The verification protocol is CRITICAL. Include:
> "Before suggesting ANY code, command, or technical detail:
>  1. Search official documentation (web_search)
>  2. Verify function signatures and parameters
>  3. Check @pyproject.toml for library versions
>  4. State confidence: ✅ VERIFIED or ⚠️ UNCERTAIN
>  5. Never guess - always verify first"
>
> Also include "What to Verify" and "Why Verification Matters" sections.
> Keep the file comprehensive but scannable.
```

**Review the CLAUDE.md:**
- Is verification protocol clearly stated?
- Does it emphasize searching docs first?
- Does it include what to verify and why it matters?
- Would it help Claude in future sessions?

**If verification protocol is missing or weak:**
```
> The verification protocol is not strong enough.
> Add a section that REQUIRES:
> - Searching official docs before ALL code
> - Stating verification results
> - Never guessing API syntax
> Make this mandatory and prominent.
```

---

### Part 7: First Git Commit (15 minutes)

**Tell Claude:**
```
> Let's make our first git commit.
> Add all the files we created and commit with the message:
> "feat: initial project setup with player movement and verification protocol"
```

**Verify the commit:**
```
> Show me the git log
```

You should see your first commit!

---

### Part 8: Session Wrap-up (15 minutes)

**Create TODO.md:**
```
> Create a TODO.md file that lists what we should build next:
> - Simple zombie spawning
> - Player-zombie collision
> - Basic combat (melee attack)
> - Health system
> - Score/kill counter
>
> Mark what we completed today as done.
```

**Create PROGRESS.md:**
```
> Create a PROGRESS.md file documenting what we built in Session 1:
> - Basic game window with top-down view
> - Player character with WASD movement
> - Verification protocol established
> - CLAUDE.md with mandatory verification requirements
> - Project structure and git repository
>
> Include a "Lessons Learned" section:
> - Importance of verifying docs before coding
> - How verification prevents bugs
> - pygame 2.5.2 API basics
```

**Final commit:**
```
> Commit these new docs with message:
> "docs: add TODO, PROGRESS, and VERIFICATION tracking"
```

---

## Troubleshooting

### Common Issues

**Issue: pygame not installed**
```
> Search for uv sync command
> Verify correct usage
> Then install: uv sync
> Run game again with: uv run python src/main.py
```

**Issue: ImportError**
```
> Check that all files are in the right directories
> Show me the current file structure
> Verify import statements match pygame docs
```

**Issue: Player doesn't move**
```
> Search pygame docs for key event handling
> Verify we're using pygame.key.get_pressed() correctly
> Check movement calculation uses delta_time
```

**Issue: Claude didn't verify before coding**
```
> STOP. You must search pygame 2.5.2 docs BEFORE writing code.
> Show me your verification results for [specific function].
> Only proceed after verification.
```

---

## Session 1 Checklist

Before ending this session, verify:

- [ ] Game window opens and runs
- [ ] Player character is visible (green circle)
- [ ] WASD movement works in all 8 directions
- [ ] Player stays within screen boundaries
- [ ] CLAUDE.md exists with STRONG verification protocol
- [ ] README.md exists
- [ ] .python-version specifies Python 3.10+
- [ ] pyproject.toml has pygame==2.5.2
- [ ] uv.lock exists (generated by uv sync)
- [ ] TODO.md lists next features
- [ ] PROGRESS.md documents Session 1
- [ ] Git repository initialized
- [ ] At least 2 commits made
- [ ] You understand verification importance
- [ ] Claude verified docs before every code suggestion

---

## What You Learned

**Technical:**
- Setting up a pygame project
- Top-down game camera perspective
- Player movement with WASD (8-directional)
- Frame-independent movement (delta_time)
- Boundary checking

**Agentic Coding:**
- **Verification-first development** (MOST IMPORTANT!)
- Basic Claude Code workflow
- Using @ to reference files
- Running code through Claude
- Making git commits through Claude
- Creating focused documentation (CLAUDE.md)

**Verification Skills:**
- Searching official docs before coding
- Verifying function signatures
- Checking library versions
- Stating confidence levels
- Never guessing technical details

---

## Reflection Questions

Take 5 minutes to think about:

1. Did Claude verify documentation before every code suggestion?
2. How did verification prevent potential bugs?
3. What pygame functions did we verify?
4. Why is verification critical for agentic development?
5. How does the game look/feel so far?

**Document answers in PROGRESS.md!**

---

## Next Session Preview

In Session 2, we'll add:
- Simple zombie spawning (random positions)
- Zombie AI (move toward player)
- Basic collision detection
- ARCHITECTURE.md documentation

**New concepts:**
- ARCHITECTURE.md patterns
- Better testing workflows
- Continued verification discipline

---

## Session 1 Complete! 🎉

You now have:
- ✅ Working pygame project
- ✅ Player with 8-directional movement
- ✅ Strong verification protocol established
- ✅ Basic documentation
- ✅ Git repository
- ✅ Foundation for agentic coding with confidence

**Ready for Session 2?**
```
> Read @SESSION_GUIDES/SESSION_02.md
> Let's add zombies and combat!
```

---

## 🔒 Remember: Verification First, Always

**Never code without:**
1. Searching official docs
2. Verifying syntax
3. Checking versions
4. Stating confidence

**This discipline will save you hours of debugging!**
