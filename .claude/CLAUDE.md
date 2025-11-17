# CLAUDE.md - TDD Workflow  

## Auto-Trigger Patterns  

Activate TDD Planner Agent on:  

- Create/Implement/Add/Build [feature]  
- Modify/Improve/Refactor/Optimize [feature]  
- Fix/Solve/Debug/Resolve [issue]  
- Error logs/stack traces  

**Do NOT trigger on**: questions, explanations, casual chat  

## Agent System  

### TDD Planner (`.claude/agents/tdd-planner.md`)  

- Research, decompose, create issues, generate TDD plans  
- Trigger: Auto or `/plan <task>`  

### Issue Creator (`.claude/agents/issue-creator.md`)  

- Create GitHub issues via `gh` CLI  
- Trigger: After user approval or `/create-issues`  

## TDD Cycle  

1. **RED**: Failing test → `test(#N): add test for X`  
2. **GREEN**: Minimum code → `feat(#N): implement X`  
3. **REFACTOR**: Clean up → `refactor(#N): improve X`  
4. **MARK**: Check `[x]` in `docs/N-...-tdd.md` → `docs(#N): mark complete`  

## Structure  

```
tests/      # Test code  
docs/       # TDD plans (N-...-tdd.md)  
src/        # Production code  
.claude/    # Agents & commands  
```

## Commit Format  

`<type>(#N): <description>`  

## Workflow  

```
User request → TDD Planner (auto) → Create TDD → Propose issues  
→ User approval → Issue Creator (auto) → Create #N, #N+1...  
→ Generate TDD plans → Execute TDD cycles → Issue Resolve (auto)  
```

## Rules  

✅ Auto-trigger, Tests in tests/, Minimum GREEN code, Include #N  
❌ Skip agents, Skip RED, Multiple issues simultaneously  

