# Project Rules & Style Guide

## Output Style
*   **Brevity:** Provide code solutions only. Strictly no conversational commentary, no reassurance, and no explanations unless explicitly requested.
*   **Refactoring Rule:** Keep code compact. If a solution can be written in 50 lines instead of 200, you must rewrite and simplify it.
*   **No Bloat:** Do not add extra features, speculative code, or unrequested optimizations.
- Self-descriptive code over excessive comments
- Comments for intent, not implementation

## Code Standards
*   **Readability:** Prefer clean, explicit, self-documenting code over complex or over-engineered patterns.
*   **Syntax:** Use modern, standard syntax (e.g., explicit type hints, native ES modules, async/await).
*   **Error Handling:** Include concise, visible error handling. Do not swallow errors or add deep nested try-catch blocks.

### Error Handling Philosophy
- **Let exceptions bubble up** naturally for better error visibility
- Only catch exceptions when you can meaningfully recover from them
- Prefer clear failures over hidden bugs

### Anti-Defensive Programming Philosophy
- **Fail Fast**: Let exceptions bubble up naturally for clear debugging information
- **Minimal Try-Catch**: Only use try-catch when absolutely necessary for error recovery
- **No Excessive Null Checks**: Avoid defensive programming for things that should never be null
- **Assumption Validation**: It's fine to assume correctness for things that would fail during initialization and be caught in basic smoke testing

**Why**: Defensive programming hides bugs instead of revealing them. Clear exceptions with full stack traces are more valuable than swallowed errors.