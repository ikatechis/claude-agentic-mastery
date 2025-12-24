# GitHub Copilot Review Instructions

## Focus Areas

### Critical
- Security vulnerabilities (injection attacks, XSS, unsafe operations)
- Logic errors that cause incorrect behavior
- Resource leaks or memory management issues
- Race conditions and concurrency bugs

### Important
- Performance bottlenecks
- Incorrect API usage
- Missing error handling
- Type safety issues

### Code Quality
- Code clarity and maintainability
- Inconsistent patterns
- Missing documentation for complex logic

## Review Style

- **Be concise:** Focus on actionable feedback
- **Provide examples:** Show correct implementation when suggesting changes
- **Explain reasoning:** Say *why* something is an issue, not just *what*
- **Prioritize correctness:** Functionality > style preferences
- **Admit uncertainty:** If unsure about a suggestion, say so explicitly

## Project Context

This is a **pygame-based zombie survival game** built as a learning project for AI-assisted development.

### Technical Stack
- **Language:** Python 3.11.5
- **Game Library:** pygame 2.6.0
- **Package Manager:** uv
- **Config Pattern:** Dataclasses for centralized configuration

### Architecture Patterns
- **Frame-independent movement:** All movement uses `delta_time` multipliers
- **Component-based entities:** Entities self-update and self-render
- **Centralized config:** All tunable values in `src/config.py`
- **Verification-first:** Always verify APIs before suggesting code

### Current Focus (Session 2)
- Combat system implementation
- Multi-entity management (zombie spawning)
- Collision detection and damage systems

## What to Avoid

- Minor style nitpicks (unless they violate project conventions)
- Premature optimization suggestions
- Subjective refactoring that doesn't improve clarity
- Hallucinating API signatures or configuration schemas
- Confident suggestions about things you're unsure of

## Special Instructions

**For configuration files:**
- Only suggest schemas you can verify are correct
- Warn before suggesting changes to `.gemini/config.yaml`, `pyproject.toml`, etc.
- If unsure about config structure, state this explicitly

**For pygame APIs:**
- Verify pygame 2.6.0 compatibility before suggesting
- Check method signatures and parameters
- Consider performance implications for game loop code
