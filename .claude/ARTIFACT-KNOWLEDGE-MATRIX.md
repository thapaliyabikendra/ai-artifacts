# Artifact Knowledge Matrix

Cross-reference of agents, skills, and their knowledge profiles (concepts + implementations).

## Purpose

This matrix shows:
1. Which concepts each agent understands
2. Which implementations each agent can apply
3. Skill-to-knowledge mappings
4. Coverage gaps

## Agent Knowledge Profiles

### By Category

#### Engineers (`agents/engineers/`)

| Agent | Understands | Applies |
|-------|-------------|---------|
| **abp-developer** | solid/srp, solid/ocp, solid/dip, clean-code/naming, clean-code/functions, clean-architecture/layers, clean-architecture/dependency-rule | dotnet/solid, dotnet/clean-code |
| react-developer | *(not yet profiled)* | *(not yet profiled)* |
| devops-engineer | *(not yet profiled)* | *(not yet profiled)* |

#### Reviewers (`agents/reviewers/`)

| Agent | Understands | Applies |
|-------|-------------|---------|
| **abp-code-reviewer** | solid/*, clean-code/*, code-smells/taxonomy, clean-architecture/layers, clean-architecture/dependency-rule, clean-architecture/smells, testing/test-smells | dotnet/solid, dotnet/clean-code, dotnet/code-smells |
| **qa-engineer** | testing/tdd-principles, testing/first, testing/test-smells | dotnet/xunit-tdd |
| react-code-reviewer | *(not yet profiled)* | *(not yet profiled)* |
| security-engineer | *(not yet profiled)* | *(not yet profiled)* |

#### Architects (`agents/architects/`)

| Agent | Understands | Applies |
|-------|-------------|---------|
| backend-architect | *(not yet profiled)* | *(not yet profiled)* |
| business-analyst | *(not yet profiled)* | *(not yet profiled)* |

#### Specialists (`agents/specialists/`)

| Agent | Understands | Applies |
|-------|-------------|---------|
| debugger | *(not yet profiled)* | *(not yet profiled)* |
| database-migrator | *(not yet profiled)* | *(not yet profiled)* |

---

## Concept Coverage

Shows which concepts are understood by at least one agent.

### SOLID Principles

| Concept | Agents Understanding |
|---------|---------------------|
| solid/srp | abp-developer, abp-code-reviewer |
| solid/ocp | abp-developer, abp-code-reviewer |
| solid/lsp | abp-code-reviewer |
| solid/isp | abp-code-reviewer |
| solid/dip | abp-developer, abp-code-reviewer |

### Clean Code

| Concept | Agents Understanding |
|---------|---------------------|
| clean-code/naming | abp-developer, abp-code-reviewer |
| clean-code/functions | abp-developer, abp-code-reviewer |
| clean-code/comments | abp-code-reviewer |

### Clean Architecture

| Concept | Agents Understanding |
|---------|---------------------|
| clean-architecture/layers | abp-developer, abp-code-reviewer |
| clean-architecture/dependency-rule | abp-developer, abp-code-reviewer |
| clean-architecture/smells | abp-code-reviewer |

### Code Smells

| Concept | Agents Understanding |
|---------|---------------------|
| code-smells/taxonomy | abp-code-reviewer |

### Testing

| Concept | Agents Understanding |
|---------|---------------------|
| testing/tdd-principles | qa-engineer |
| testing/first | qa-engineer |
| testing/test-smells | abp-code-reviewer, qa-engineer |

---

## Implementation Coverage

Shows which implementations are applied by at least one agent.

| Implementation | Agents Applying |
|----------------|-----------------|
| dotnet/solid | abp-developer, abp-code-reviewer |
| dotnet/clean-code | abp-developer, abp-code-reviewer |
| dotnet/code-smells | abp-code-reviewer |
| dotnet/xunit-tdd | qa-engineer |

---

## Skill-to-Knowledge Mapping

Shows which skills reference which knowledge.

| Skill | Concepts | Implementations |
|-------|----------|-----------------|
| clean-code-dotnet | solid/*, clean-code/*, code-smells/* | dotnet/solid, dotnet/clean-code, dotnet/code-smells |
| abp-framework-patterns | solid/srp, solid/dip, clean-architecture/layers | *(inline examples)* |
| xunit-testing-patterns | testing/* | dotnet/xunit-tdd |
| code-review-excellence | clean-code/*, testing/test-smells | dotnet/clean-code |
| debugging-patterns | code-smells/taxonomy | dotnet/code-smells |

---

## Coverage Gaps

### Agents Without Profiles

The following agents need knowledge profiles added:

| Agent | Category | Suggested Concepts |
|-------|----------|-------------------|
| react-developer | engineers | clean-code/*, testing/test-smells |
| devops-engineer | engineers | *(minimal - infrastructure focus)* |
| backend-architect | architects | solid/*, clean-architecture/*, testing/test-pyramid |
| business-analyst | architects | *(domain-focused, less code)* |
| react-code-reviewer | reviewers | clean-code/*, testing/test-smells |
| security-engineer | reviewers | *(security-specific concepts)* |
| debugger | specialists | code-smells/taxonomy |
| database-migrator | specialists | *(minimal - infrastructure focus)* |

### Concepts Without Agent Coverage

| Concept | Recommendation |
|---------|----------------|
| refactoring/* | Add to abp-developer, debugger |
| package-design/* | Add to backend-architect |

### Implementations Without Agent Coverage

| Implementation | Recommendation |
|----------------|----------------|
| react/clean-code | Add to react-developer, react-code-reviewer |
| react/jest-tdd | Add to qa-engineer |

---

## How to Update

### Adding a Knowledge Profile to an Agent

1. Identify which concepts the agent needs to understand
2. Identify which implementations the agent applies
3. Add `understands:` and `applies:` to agent front matter
4. Update this matrix

### Adding a New Concept

1. Create concept in `knowledge/concepts/{topic}/{concept}.md`
2. Add to `knowledge/concepts/INDEX.md`
3. Create implementation in `knowledge/implementations/{lang}/{file}.md`
4. Add to `knowledge/implementations/INDEX.md`
5. Update relevant agent profiles
6. Update this matrix

---

## Validation

Check that all referenced paths exist:

```bash
# Verify concept paths
grep -h "understands:" .claude/agents/**/*.md -A 10 | grep "^\s*-" | sort -u

# Verify implementation paths
grep -h "applies:" .claude/agents/**/*.md -A 10 | grep "^\s*-" | sort -u
```

## Related Files

- [GUIDELINES.md](GUIDELINES.md#artifact-knowledge-rules) - Governance rules
- [SKILL-INDEX.md](SKILL-INDEX.md) - Skill discovery
- [knowledge/concepts/INDEX.md](knowledge/concepts/INDEX.md) - Concept registry
- [knowledge/implementations/INDEX.md](knowledge/implementations/INDEX.md) - Implementation registry
