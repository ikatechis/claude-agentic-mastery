# Verification Protocol - Quick Reference

## Before ANY Code/Command

**Never skip these steps:**

- [ ] Search official documentation
- [ ] Verify exact syntax
- [ ] Check @pyproject.toml for versions
- [ ] State confidence level
- [ ] Never guess

## Confidence Levels

### ✅ VERIFIED
"Checked [source] - [exact detail confirmed]"

**Examples:**
- "Searched pygame 2.5.2 docs - pygame.sprite.Sprite requires super().__init__()"
- "Verified pygame.draw.circle(surface, color, center, radius) signature"
- "Checked uv docs - 'uv add package==version' adds to pyproject.toml"

### ⚠️ UNCERTAIN
"Will search [source] to verify [detail]"

**Examples:**
- "Will search pygame docs for correct event handling syntax"
- "Need to verify pygame.font parameters before suggesting code"

### ❌ GUESSING
"Let me verify this with web_search first"

**Never proceed with guessing - always search first**

## What to Verify

### Pygame APIs
- Function/method signatures
- Parameter names and types
- Return values
- Class inheritance patterns
- Event types and constants

### Python Features
- Syntax compatibility with Python 3.11
- Standard library functions
- Built-in methods

### Tools & Commands
- uv commands (add, sync, run, etc.)
- pyenv commands (local, global, etc.)
- Git commands (init, add, commit, etc.)

### Configuration Files
- pyproject.toml structure
- .python-version format
- .gitignore patterns

## Good vs Bad Examples

### ✅ GOOD - Always Do This

```
Claude: "Before creating the sprite class, let me verify the pygame.sprite.Sprite API"
[Searches pygame 2.5.2 documentation]
Claude: "✅ VERIFIED: pygame.sprite.Sprite is the base class. Child classes must call super().__init__() and should define self.image and self.rect attributes. Source: pygame.org/docs/ref/sprite.html"
```

### ❌ BAD - Never Do This

```
Claude: "I think pygame sprites need an update() method. Let me create the class..."
[Proceeds without verification]
```

## Verification Workflow

```
1. User Request
   ↓
2. Identify what needs verification
   ↓
3. Search official documentation (web_search)
   ↓
4. Verify exact details
   ↓
5. State: "✅ VERIFIED: [details] from [source]"
   ↓
6. Write code with confidence
   ↓
7. Test immediately
```

## Why Verification Matters

**Without verification:**
- Hours debugging hallucinated APIs
- Wrong parameter names/types
- Version incompatibilities
- Frustration and wasted time

**With verification:**
- Code works first time
- Confidence in suggestions
- Learn real APIs
- Professional development habits

## Remember

**Verification isn't optional. It's mandatory.**

Every unverified suggestion is a potential bug waiting to happen.

**When in doubt:**
1. Search the docs
2. Verify the syntax
3. State what you found
4. Then write code

**Never:**
- Assume API signatures
- Guess parameter syntax
- Skip version checking
- Claim certainty without sources

## Quick Decision Tree

```
Need to suggest code/command?
    ↓
Do I know the EXACT syntax?
    ↓
    NO → Search docs → Verify → State "✅ VERIFIED"
    ↓
    YES → Did I verify it THIS session?
        ↓
        NO → Search docs → Verify → State "✅ VERIFIED"
        ↓
        YES → Proceed with confidence
```

## Verification is a Habit

The more you verify, the more natural it becomes.
The project succeeds when verification becomes automatic.

**Build with confidence. Verify first. Always.**
