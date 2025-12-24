# Quick Reference - Verification-First Agentic Coding

## 🔒 VERIFICATION PROTOCOL (Always First!)

**Before ANY code/command:**
```
1. Search official docs (web_search)
2. Verify exact syntax
3. Check @pyproject.toml versions
4. State: ✅ VERIFIED or ⚠️ UNCERTAIN
5. Never guess
```

## Essential Commands

### Context Management
```bash
Shift+Tab         # Cycle modes (normal/plan/auto-accept)
/context          # Check context usage
/compact          # Free context (at 70%+)
```

### Skills & Agents  
```bash
/skills           # List available Skills
/agents           # Manage subagents
```

### Project Navigation
```bash
@filename         # Reference files
@folder/file      # Reference with path
```

## Verification Examples

### ✅ GOOD
```
"Searched pygame 2.5.2 docs - pygame.sprite.Sprite.update() confirmed"
"Verified pygame.draw.circle(surface, color, center, radius) signature"
```

### ❌ BAD
```
"I think pygame has update()"
"Use pygame.draw.circle() probably"
```

## When to Verify

- [ ] Before writing ANY code
- [ ] Before using ANY pygame function
- [ ] Before suggesting ANY parameter
- [ ] Before creating config files
- [ ] Before using command flags

## Quick Decision: Use Plan Mode?

```
Context > 70%? → Yes, use plan mode (Shift+Tab)
Need to explore 5+ files? → Yes
Want to code NOW? → No, normal mode
```

## Git Commit Format

```
feat: new feature
fix: bug fix
docs: documentation
refactor: code improvement
```

## Remember

**Verification isn't optional. It's mandatory.**

Every suggestion without verification is a potential bug.
