# Gemini Code Assist Style Guide

## Review Focus

Please focus your code reviews on:

### Critical Issues
- Security vulnerabilities (SQL injection, XSS, command injection, etc.)
- Logic bugs that affect functionality
- Performance bottlenecks
- Memory leaks or resource management issues

### Important Issues
- Incorrect API usage or deprecated methods
- Missing error handling for critical paths
- Race conditions or concurrency issues
- Breaking changes to public interfaces

### Code Quality
- Inconsistent patterns within the codebase
- Missing documentation for complex logic
- Overly complex code that could be simplified

## Review Style

- Be concise and actionable
- Provide specific examples or fixes when possible
- Explain *why* something is an issue, not just *what*
- Focus on correctness over style preferences

## Verification and Uncertainty

**CRITICAL: When you are uncertain about a suggestion:**
- Do NOT guess or make up API signatures, configuration schemas, or documentation
- State clearly: "I'm not certain about X, please verify in the official docs"
- If a comment references external documentation, acknowledge you cannot fetch it
- Admit when you don't have enough context to make a confident suggestion
- Prefer asking clarifying questions over making assumptions

**For configuration files and schemas:**
- Only suggest configurations you are absolutely certain are correct
- If unsure about schema structure, say so explicitly
- Warn when suggesting changes to critical files (.gemini/config.yaml, pyproject.toml, etc.)

## Ignore

- Minor style preferences (indentation, naming) unless they violate project conventions
- Subjective refactoring that doesn't improve clarity
- Nitpicks that don't affect functionality

## Project Context

This is a pygame-based game project following:
- Frame-independent movement using `delta_time`
- Centralized configuration in `config.py` using dataclasses
- Component-based entity pattern
- Verification-first development workflow
