# Antipatterns

> Common mistakes to avoid when creating Claude Code artifacts.

## Agent Antipatterns

### 1. Embedded Code Templates

```markdown
# BAD: Agent with 100+ lines of code templates
## Entity Pattern
```csharp
public class Patient : FullAuditedAggregateRoot<Guid>
{
    // 50 lines of code...
}
```

# GOOD: Reference a skill
## Implementation
Apply the `abp-entity-patterns` skill for entity templates.
```

**Why bad**: Agents become bloated, code not reusable, hard to maintain.

### 2. Hardcoded Project Names

```markdown
# BAD
Build: `dotnet build api/ClinicManagementSystem.slnx`
Path: `api/src/ClinicManagementSystem.Domain/`

# GOOD
Build: `dotnet build api/*.slnx` or use dynamic detection
Path: `api/src/{ProjectName}.Domain/` (read from CLAUDE.md)
```

**Why bad**: Agent only works for one project, not portable.

### 3. All Tools Granted

```yaml
# BAD: Reviewer agent with write access
name: code-reviewer
tools: Read, Write, Edit, Bash, Glob, Grep

# GOOD: Read-only for reviewers
name: code-reviewer
tools: Read, Glob, Grep
```

**Why bad**: Violates least privilege, reviewers shouldn't modify code.

### 4. Missing Trigger Description

```yaml
# BAD: No guidance on when to use
description: Reviews code

# GOOD: Clear triggers
description: |
  Code reviewer for .NET/ABP Framework backend. Reviews PRs for ABP patterns,
  DDD, EF Core, security vulnerabilities. Use PROACTIVELY after backend code changes.
```

**Why bad**: Claude won't know when to auto-invoke the agent.

---

## Skill Antipatterns

### 1. Verbose Explanations

```markdown
# BAD: Explaining what Claude knows
PDF (Portable Document Format) is a file format developed by Adobe in
the 1990s. It preserves document formatting across different platforms...

# GOOD: Jump to actionable content
## Extract PDF Text
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```
```

**Why bad**: Wastes tokens on information Claude already has.

### 2. Everything in SKILL.md

```markdown
# BAD: 800 line SKILL.md with all content

# GOOD: Progressive disclosure
## Quick Start
[Essential content - 50 lines]

## Advanced
See [advanced.md](references/advanced.md)
```

**Why bad**: All content loads every time skill triggers, wastes context.

### 3. Vague Description

```yaml
# BAD
description: Helps with documents

# GOOD
description: |
  Extract text and tables from PDF files, fill forms, merge documents.
  Use when: (1) working with PDFs, (2) extracting content, (3) filling forms.
```

**Why bad**: Won't auto-trigger appropriately, hard to discover.

### 4. Wrong Tech Stack Examples

```yaml
# BAD: Python examples in .NET skill
name: abp-framework-patterns
tech_stack: [dotnet, csharp, abp]

## Example
```python  # Wrong language!
def create_entity():
    pass
```

# GOOD: Matching tech stack
```csharp
public class Entity : AggregateRoot<Guid> { }
```
```

**Why bad**: Confusing, may cause wrong code generation.

---

## Command Antipatterns

### 1. Domain Knowledge in Commands

```markdown
# BAD: Command with embedded patterns
## Entity Pattern
```csharp
// 50 lines of code patterns
```

# GOOD: Reference skills
Apply the `abp-entity-patterns` skill, then scaffold using this command.
```

**Why bad**: Commands should be atomic actions, not knowledge repositories.

### 2. Missing $ARGUMENTS

```markdown
# BAD: Hardcoded values
Create an entity called Patient with properties Name and Email.

# GOOD: Dynamic arguments
Create an entity called $ARGUMENTS with the specified properties.
```

**Why bad**: Command only works for one specific case.

### 3. Too Complex for Command

```markdown
# BAD: Multi-stage workflow in command
1. Analyze requirements
2. Design API
3. Implement code
4. Write tests
5. Review

# GOOD: Use agent chain or simpler command
Use `/feature:add-feature` which orchestrates agents, OR
Keep command to single atomic action like `/generate:entity`
```

**Why bad**: Commands should be atomic; complex workflows need agents.

---

## Organization Antipatterns

### 1. Wrong Folder Structure

```
# BAD: Agents by action
agents/
├── code-review/
├── testing/
└── debugging/

# GOOD: Agents by role
agents/
├── reviewers/
├── engineers/
└── specialists/
```

**Why bad**: Agents ARE roles, not actions.

### 2. Commands by Role

```
# BAD: Commands by who uses them
commands/
├── developer/
├── reviewer/

# GOOD: Commands by action
commands/
├── generate/
├── review/
├── debug/
```

**Why bad**: Commands are ACTIONS, not personas.

### 3. Skills by File Type

```
# BAD
skills/
├── csharp-files/
├── typescript-files/

# GOOD: By topic/domain
skills/
├── abp-framework-patterns/
├── react-development-patterns/
```

**Why bad**: Skills are knowledge domains, not file processors.

---

## Content Antipatterns

### 1. Time-Sensitive Information

```markdown
# BAD
As of December 2024, the latest version is 10.0.1...

# GOOD
Use the current stable version. Check CLAUDE.md for project version.
```

**Why bad**: Becomes outdated, requires constant updates.

### 2. Duplicate Content

```markdown
# BAD: Same pattern in 3 files
# In agent-a.md, agent-b.md, skill-c.md:
```csharp
public class Entity : FullAuditedAggregateRoot<Guid> { }
```

# GOOD: Single source
# In skill, agents reference it:
Apply the `abp-entity-patterns` skill for entity templates.
```

**Why bad**: Maintenance nightmare, inconsistency risk.

### 3. First-Person Descriptions

```yaml
# BAD
description: I can help you process PDFs and extract text.

# GOOD
description: Processes PDFs and extracts text. Use when working with PDF files.
```

**Why bad**: Descriptions are injected into system prompts, third person reads better.

---

## Quick Reference

| Antipattern | Fix |
|-------------|-----|
| Embedded code in agents | Extract to skills |
| Hardcoded project names | Use placeholders |
| All tools for reviewers | Least privilege |
| Verbose skill content | Assume Claude knows |
| Everything in SKILL.md | Progressive disclosure |
| Vague descriptions | Specific + triggers |
| Domain knowledge in commands | Reference skills |
| Complex command workflows | Use agents |
| Duplicate content | Single source |
| Time-sensitive info | Remove or generalize |

## Related

- [Agent Examples](agent-examples.md)
- [Skill Examples](skill-examples.md)
- [Agent Separation Pattern](../patterns/agent-separation.md)
