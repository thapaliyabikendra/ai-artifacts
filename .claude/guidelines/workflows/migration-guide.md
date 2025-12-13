# Migration Guide

> How to refactor bloated artifacts and reorganize existing files.

## Agent Refactoring

When agents grow too large (>150 lines), follow this process:

### Step 1: Audit Size

```bash
# Check all agent sizes
find .claude/agents -name "*.md" -exec wc -l {} \; | sort -n

# Identify over-limit agents (>150 lines)
find .claude/agents -name "*.md" -exec sh -c \
  'lines=$(wc -l < "$1"); [ "$lines" -gt 150 ] && echo "$1: $lines"' _ {} \;
```

### Step 2: Identify Extraction Candidates

| Find This | Lines | Extract To |
|-----------|-------|------------|
| Code blocks (```csharp, ```typescript) | >20 | Skill |
| Output format templates | >15 | Skill |
| Step-by-step procedures | >10 | Skill |
| CLI commands ("Run this:") | Any | Command |
| Project structure diagrams | Any | docs/ |
| Hardcoded project names | Any | Replace with placeholders |

### Step 3: Extract to Skills

1. Create skill folder: `skills/{pattern-name}/`
2. Move code patterns to `SKILL.md`
3. Replace placeholders: `Patient` → `{Entity}`
4. Update agent to reference skill:
   ```yaml
   skills: new-skill-name
   ```
5. Replace inline content with:
   ```markdown
   Apply the `new-skill-name` skill for [pattern type].
   ```

### Step 4: Extract to Commands

1. Identify atomic CLI operations
2. Create command: `commands/{category}/{command-name}.md`
3. Use `$ARGUMENTS` for parameters
4. Update agent:
   ```markdown
   Use `/command-name <args>` for [operation].
   ```

### Step 5: Verify

- [ ] Agent under 150 lines
- [ ] Produces same outputs
- [ ] Skills load correctly
- [ ] Commands work standalone

---

## Skill Refactoring

When SKILL.md exceeds 500 lines:

### Step 1: Identify Split Points

| Content Type | Move To |
|--------------|---------|
| Advanced topics | `references/advanced.md` |
| API details | `references/api.md` |
| Long examples | `references/examples.md` |
| Edge cases | `references/edge-cases.md` |

### Step 2: Extract to References

1. Create `references/` folder
2. Move content to appropriate file
3. Add link in SKILL.md:
   ```markdown
   ## Advanced Topics
   **Topic A**: See [topic-a.md](references/topic-a.md)
   ```

### Step 3: Verify Progressive Disclosure

- [ ] SKILL.md under 500 lines
- [ ] Core patterns remain in SKILL.md
- [ ] Advanced content in references/
- [ ] Links work correctly

---

## Repository Reorganization

When restructuring the entire `.claude/` folder:

### Checklist

- [ ] **Identify duplicates** - Find same content in multiple files
- [ ] **Consolidate** - Single source of truth for each pattern
- [ ] **Move agents to role-based categories**:
  - `architects/` - Design, planning
  - `reviewers/` - Code review, auditing
  - `engineers/` - Implementation
  - `specialists/` - Domain expertise
- [ ] **Move commands to action-based categories**:
  - `generate/` - Create new code
  - `review/` - Analyze code
  - `debug/` - Fix issues
  - `refactor/` - Improve code
- [ ] **Update cross-references** - Fix all links
- [ ] **Remove empty folders**
- [ ] **Update index files**:
  - SKILL-INDEX.md
  - COMMAND-INDEX.md
  - AGENT-QUICK-REF.md
  - CONTEXT-GRAPH.md

---

## Portability Migration

When making artifacts project-agnostic:

### Step 1: Find Hardcoded Values

```bash
# Search for project name
grep -r "ClinicManagementSystem" .claude/
grep -r "YourProjectName" .claude/

# Search for specific entity names
grep -r "Patient\|Doctor\|Invoice" .claude/skills/ .claude/agents/
```

### Step 2: Replace with Placeholders

| Find | Replace With |
|------|--------------|
| `ClinicManagementSystem` | `{ProjectName}` |
| `Patient` (in examples) | `{Entity}` |
| `api/src/ClinicManagementSystem.Domain/` | Dynamic detection |
| `ClinicPermissions.Patients.Create` | `{Project}Permissions.{Feature}.{Action}` |

### Step 3: Add Dynamic Detection

For commands that need paths:

```bash
# Find solution file
SOLUTION=$(find api -maxdepth 1 -name "*.slnx" -o -name "*.sln" | head -1)

# Find EF project
EF_PROJECT=$(find api/src -maxdepth 1 -type d -name "*EntityFrameworkCore" | head -1)
```

### Step 4: Add Context Loading

```markdown
## Project Context
Before proceeding, read:
1. `CLAUDE.md` - Project name and conventions
2. `docs/architecture/README.md` - Project structure
```

---

## Quality Checklist

### Before Migration

- [ ] Backup current state (git commit)
- [ ] Document current structure
- [ ] Identify all cross-references

### After Migration

- [ ] All agents under 150 lines
- [ ] All skills under 500 lines
- [ ] No hardcoded project names
- [ ] No duplicate content
- [ ] All links work
- [ ] Index files updated
- [ ] Test key workflows:
  - [ ] `/feature:add-feature` works
  - [ ] `/generate:entity` works
  - [ ] Agent chains work

---

## Common Issues

### Broken Links After Move

```bash
# Find broken markdown links
grep -r "\[.*\](.*\.md)" .claude/ | while read line; do
  file=$(echo "$line" | cut -d: -f1)
  link=$(echo "$line" | grep -oP '\]\(\K[^)]+')
  # Check if link target exists
done
```

### Circular Skill Dependencies

If skill A depends on skill B which depends on skill A:
1. Extract common content to shared knowledge file
2. Both skills reference the shared file
3. Remove direct dependency

### Large Index Files

If SKILL-INDEX.md or COMMAND-INDEX.md grows too large:
1. Keep quick lookup tables
2. Move detailed descriptions to the artifacts themselves
3. Index should be for discovery, not documentation

## Related

- [Creating Artifacts](creating-artifacts.md)
- [Agent Separation Pattern](../patterns/agent-separation.md)
- [Portability Patterns](../patterns/portability-patterns.md)
