# Create Issues Command

Create GitHub issues from templates.

## Usage
```bash
/create-issues
```

Auto-called after TDD Planner proposes & user confirms.

## Actions

Launch Issue Creator (@.claude/agents/issue-creator.md):
1. Verify gh CLI
2. Parse templates
3. Create issues via `gh issue create`
4. Capture #42, #43...
5. Return to TDD Planner
