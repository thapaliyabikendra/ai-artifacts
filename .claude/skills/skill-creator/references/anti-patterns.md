# Skill Anti-Patterns

Common mistakes that reduce skill effectiveness. Avoid these patterns.

## 1. Vague Trigger Descriptions

The description is the primary mechanism for skill activation. Vague descriptions cause missed triggers or false activations.

**Bad:**
```yaml
description: Helps with documents
```

**Good:**
```yaml
description: Create, edit, and analyze Microsoft Word documents (.docx). Use when: (1) creating new documents from scratch, (2) modifying existing .docx files, (3) extracting text or metadata, (4) working with tracked changes or comments, (5) converting documents to other formats.
```

**Why it matters:** Claude scans descriptions to decide which skill to load. Specific trigger scenarios ensure the skill activates when needed.

---

## 2. Abstract Instructions Without Examples

Describing what to do without showing how leads to inconsistent outputs.

**Bad:**
```markdown
## Formatting Guidelines
Format the output professionally with proper structure.
```

**Good:**
```markdown
## Formatting Guidelines

**Example transformation:**

Input: "Add error handling to the function"

Output:
```typescript
try {
  const result = await fetchData();
  return result;
} catch (error) {
  logger.error('Failed to fetch data', { error });
  throw new ApplicationError('DATA_FETCH_FAILED', error);
}
```

Follow this pattern: wrap operations in try/catch, log with context, throw typed errors.
```

**Why it matters:** Examples communicate expectations more precisely than descriptions. Claude learns patterns from concrete instances.

---

## 3. Monolithic SKILL.md

Cramming everything into SKILL.md wastes context window and makes navigation difficult.

**Bad:**
```
skill/
├── SKILL.md (2000+ lines with everything)
```

**Good:**
```
skill/
├── SKILL.md (300 lines - core workflow + navigation)
└── references/
    ├── api-reference.md (detailed API docs)
    ├── examples.md (comprehensive examples)
    └── troubleshooting.md (edge cases)
```

**Why it matters:** SKILL.md loads entirely when triggered. Large files consume context needed for the actual task. References load on-demand.

---

## 4. Missing User Input Gathering

Jumping into execution without understanding scope leads to wasted effort and rework.

**Bad:**
```markdown
## Refactoring Process
1. Find all files with the pattern
2. Apply the transformation
3. Verify results
```

**Good:**
```markdown
## User Input Required

Before starting, clarify:
1. **Scope**: Which directories/files to include?
2. **Approach**: Aggressive refactoring or conservative changes?
3. **Priority**: Start with specific components?

## Refactoring Process
[After gathering input...]
```

**Why it matters:** Assumptions about scope or approach can invalidate entire workflows. Upfront questions prevent costly backtracking.

---

## 5. Over-Engineering Simple Tasks

Using scripts for tasks that are better as text instructions adds unnecessary complexity.

**Bad:**
```
skill/
├── SKILL.md
└── scripts/
    ├── format_text.py
    ├── validate_format.py
    └── apply_format.py
```
(For a skill that just formats commit messages)

**Good:**
```markdown
## Commit Message Format

Format: `type(scope): description`

Types: feat, fix, docs, style, refactor, test, chore

Examples:
- `feat(auth): add OAuth2 support`
- `fix(api): handle null response gracefully`
```

**Why it matters:** Scripts add maintenance burden and execution overhead. Text instructions are often sufficient and more flexible.

---

## 6. Duplicate Content

Same information in SKILL.md and references wastes tokens and creates sync issues.

**Bad:**
```markdown
# SKILL.md
## API Reference
[Full API documentation here...]

# references/api.md
## API Reference
[Same full API documentation here...]
```

**Good:**
```markdown
# SKILL.md
## API Reference
For complete API documentation, see [references/api.md](references/api.md).

Quick reference:
- `create()` - Create new resource
- `update()` - Modify existing resource
- `delete()` - Remove resource
```

**Why it matters:** Duplicates consume double context and diverge over time. Single source of truth with summaries in SKILL.md.

---

## 7. Kitchen Sink Skills

Skills that try to do everything become unfocused and unreliable.

**Bad:**
```yaml
name: document-processor
description: Handle all document types including PDF, DOCX, XLSX, PPTX, images, and text files. Also supports conversion, OCR, and data extraction.
```

**Good:**
```yaml
name: pdf-processor
description: Read, create, and manipulate PDF documents. Use for: form filling, text extraction, page manipulation, and PDF generation.
```

**Why it matters:** Focused skills have clearer triggers, simpler workflows, and more reliable outputs. Create multiple specialized skills instead.

---

## 8. Rigid Output Templates

Forcing exact templates when flexibility would produce better results.

**Bad:**
```markdown
ALWAYS use this EXACT format:
# Title
## Section 1
## Section 2
## Section 3
[No variations allowed]
```

**Good:**
```markdown
## Default Structure

Typical format (adapt as needed):
# Title
## Overview
[Key points]

## Details
[Expand based on content]

## Next Steps
[If applicable]

Adjust sections based on the specific content and user needs.
```

**Why it matters:** Real-world tasks vary. Over-rigid templates produce awkward outputs when content doesn't fit the mold.

---

## 9. Missing Validation Phase

Executing without verification leads to silent failures.

**Bad:**
```markdown
## Process
1. Analyze input
2. Apply transformation
3. Done!
```

**Good:**
```markdown
## Process
1. Analyze input
2. Apply transformation
3. **Validate results:**
   - Verify output format matches expectations
   - Check for regressions or side effects
   - Confirm all items processed
4. Report summary with any issues found
```

**Why it matters:** Validation catches errors before they propagate. Explicit verification steps ensure quality.

---

## 10. Hardcoded Assumptions

Embedding environment-specific details that don't generalize.

**Bad:**
```markdown
## Setup
Run: `cd /Users/john/projects/myapp && npm install`
Edit file at: `/Users/john/projects/myapp/config.json`
```

**Good:**
```markdown
## Setup
1. Navigate to project root
2. Install dependencies: `npm install`
3. Configure settings in `config.json` at project root

**Note:** Paths are relative to the project directory.
```

**Why it matters:** Skills should work across environments. Use relative paths and generic instructions.

---

## 11. Inconsistent Naming Conventions

Using placeholders without defining naming rules causes confusion and errors.

**Bad:** `{Entity}`, `{entity}`, `{ENTITY}` used interchangeably without definition

**Good:**
```markdown
## Naming Conventions

This skill uses the following placeholder conventions:
- `{Entity}` = PascalCase (e.g., "Consumer", "OrderItem")
- `{entity}` = camelCase (e.g., "consumer", "orderItem")
- `{ENTITY}` = UPPER_SNAKE (e.g., "CONSUMER", "ORDER_ITEM")
- `{entity-name}` = kebab-case (e.g., "consumer", "order-item")
- `{entity_name}` = snake_case (e.g., "consumer", "order_item")
```

**Why it matters:** Clear naming conventions prevent typos and maintain consistency across generated outputs.

---

## 12. Technology-Specific Assumptions

Embedding specific technology details that don't apply to all users.

**Bad:**
```markdown
## Setup
1. Install Node.js and npm
2. Run `npm install`
3. Add to your React component
```

**Good:**
```markdown
## Setup

**Prerequisites:** [List required tools/environment]

**Installation:** [Generic steps or multiple options]

**Integration:** [Platform-agnostic guidance OR separate sections per platform]
```

**Why it matters:** Skills should be adaptable. Provide options or keep instructions generic unless the skill is explicitly technology-specific.

---

## 13. Missing "When to Use" in Body

Putting trigger information only in the body, which isn't read until after triggering.

**Bad:**
```markdown
---
description: Helps with API design
---

# API Design

## When to Use This Skill
Use when designing REST APIs, reviewing OpenAPI specs, or...
```

**Good:**
```markdown
---
description: Design REST and GraphQL APIs with best practices. Use when: (1) designing new API endpoints, (2) reviewing OpenAPI specifications, (3) establishing API standards, (4) refactoring existing APIs for consistency.
---

# API Design

[Jump straight into the content - trigger info is in description]
```

**Why it matters:** The description is read for trigger matching. "When to use" sections in the body are never seen during trigger evaluation.

---

## 14. No Clear Entry Point

User doesn't know where to start or what to do first.

**Bad:**
```markdown
# Complex Skill

## Feature A
[Details about A]

## Feature B
[Details about B]

## Feature C
[Details about C]
```

**Good:**
```markdown
# Complex Skill

## Quick Start

1. Determine your goal → See Decision Tree below
2. Gather required input → See User Input Required
3. Follow the appropriate workflow

## Decision Tree

- Need Feature A? → Jump to [Feature A](#feature-a)
- Need Feature B? → Jump to [Feature B](#feature-b)
- Not sure? → Start with [Assessment](#assessment)
```

**Why it matters:** Clear entry points reduce cognitive load and help users (and Claude) navigate efficiently.

---

## 15. Outdated or Broken References

Links to non-existent files or outdated information.

**Bad:**
```markdown
See [detailed guide](references/old-guide.md) for more info.
<!-- File doesn't exist or is outdated -->
```

**Good:**
```markdown
See [detailed guide](references/current-guide.md) for more info.

<!-- Verify all links exist and are current -->
```

**Why it matters:** Broken references cause confusion and errors. Validate links during skill development.

---

## 16. No Error Recovery Guidance

Skills that only cover the happy path leave users stuck when things go wrong.

**Bad:**
```markdown
## Process
1. Run the script
2. Check output
3. Done
```

**Good:**
```markdown
## Process
1. Run the script
2. Check output
3. Done

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| FileNotFound | Input missing | Verify file path |
| PermissionDenied | Insufficient access | Run with elevated permissions |
| TimeoutError | Slow network | Increase timeout or retry |

## If All Else Fails
1. Check logs at [location]
2. Verify prerequisites
3. Try manual execution: [steps]
```

**Why it matters:** Error recovery guidance saves time and prevents abandonment when issues occur.

---

## 17. Assuming Claude Knows Project Context

Referencing project-specific details without explanation.

**Bad:**
```markdown
Use the standard AppService pattern.
Register in the module as usual.
```

**Good:**
```markdown
Use the AppService pattern:
```csharp
public class ProductAppService : ApplicationService, IProductAppService
{
    // Implementation
}
```

Register in the module:
```csharp
context.Services.AddTransient<IProductAppService, ProductAppService>();
```
```

**Why it matters:** Skills should be self-contained. Don't assume Claude remembers project conventions from previous conversations.

---

## Quick Reference: Pattern Detection

| If you see... | It might be... |
|--------------|----------------|
| Description under 50 characters | Vague triggers |
| No code blocks in SKILL.md | Abstract-only instructions |
| SKILL.md > 500 lines | Monolithic file |
| No "ask user" or "clarify" | Missing input gathering |
| Scripts for text formatting | Over-engineering |
| Same content in multiple files | Duplicate content |
| Description lists 5+ domains | Kitchen sink |
| "ALWAYS" and "EXACT" | Rigid templates |
| No "verify" or "validate" | Missing validation |
| Absolute paths | Hardcoded assumptions |
| Undefined placeholders | Inconsistent naming |
| Single technology assumed | Technology-specific assumptions |
| "When to use" in body only | Missing trigger info |
| No "start here" section | No clear entry point |
| Broken `[links](path)` | Outdated references |
| No error handling section | No error recovery |
| "As usual" or "standard way" | Assuming project context |

---

## Self-Check Checklist

Before finalizing a skill, verify:

- [ ] Description is 100+ characters with specific triggers
- [ ] SKILL.md < 500 lines with details in references
- [ ] At least one concrete example per major feature
- [ ] User input gathering for scope/approach decisions
- [ ] Scripts only where determinism is required
- [ ] No duplicate content between files
- [ ] Single focused purpose, not kitchen sink
- [ ] Flexible templates with adaptation guidance
- [ ] Validation/verification phase included
- [ ] Relative paths and generic instructions
- [ ] Placeholder conventions documented
- [ ] Framework-agnostic or multi-framework support
- [ ] Trigger info in description, not body
- [ ] Clear entry point and navigation
- [ ] All references exist and are current
- [ ] Error recovery guidance included
- [ ] Self-contained without project assumptions
