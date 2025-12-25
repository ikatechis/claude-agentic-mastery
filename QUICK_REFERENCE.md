# Quick Reference - Commands & Shortcuts

> **📖 Complete project guide:** See @CLAUDE.md
> **⚡ This file:** Quick command reference only

## 🔒 Verification Protocol (Brief)

**Before any code:** Verify in docs → Check @pyproject.toml → State ✅ VERIFIED
**Full protocol:** See CLAUDE.md § Verification

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
