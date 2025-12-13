# Skill Anti-Patterns

Common mistakes that reduce skill effectiveness. Avoid these patterns.

## Table of Contents

1. [Vague Trigger Descriptions](#1-vague-trigger-descriptions)
2. [Abstract Instructions Without Examples](#2-abstract-instructions-without-examples)
3. [Monolithic SKILL.md](#3-monolithic-skillmd)
4. [Missing User Input Gathering](#4-missing-user-input-gathering)
5. [Over-Engineering Simple Tasks](#5-over-engineering-simple-tasks)
6. [Duplicate Content](#6-duplicate-content)
7. [Kitchen Sink Skills](#7-kitchen-sink-skills)
8. [Rigid Output Templates](#8-rigid-output-templates)
9. [Missing Validation Phase](#9-missing-validation-phase)
10. [Hardcoded Assumptions](#10-hardcoded-assumptions)
11. [Inconsistent Naming Conventions](#11-inconsistent-naming-conventions)
12. [Technology-Specific Assumptions](#12-technology-specific-assumptions)
13. [Missing Trigger Info in Description](#13-missing-trigger-info-in-description)
14. [No Clear Entry Point](#14-no-clear-entry-point)
15. [Outdated References](#15-outdated-references)
16. [No Error Recovery Guidance](#16-no-error-recovery-guidance)
17. [Assuming Project Context](#17-assuming-project-context)

---

## 1. Vague Trigger Descriptions

The description is the primary mechanism for skill activation.

| ❌ Bad | ✅ Good |
|--------|---------|
| `description: Helps with documents` | `description: Create, edit, and analyze Word documents (.docx). Use when: (1) creating documents, (2) modifying .docx files, (3) extracting text/metadata.` |

**Why**: Claude scans descriptions to decide which skill to load. Specific triggers ensure activation.

---

## 2. Abstract Instructions Without Examples

Describing what to do without showing how leads to inconsistent outputs.

| ❌ Bad | ✅ Good |
|--------|---------|
| "Format output professionally" | Show input/output example with concrete transformation |

**Why**: Examples communicate expectations more precisely than descriptions.

---

## 3. Monolithic SKILL.md

Cramming everything into SKILL.md wastes context window.

| ❌ Bad | ✅ Good |
|--------|---------|
| `SKILL.md (2000+ lines)` | `SKILL.md (~300 lines) + references/` |

**Why**: SKILL.md loads entirely when triggered. Large files consume context needed for the task.

---

## 4. Missing User Input Gathering

Jumping into execution without understanding scope leads to wasted effort.

| ❌ Bad | ✅ Good |
|--------|---------|
| Start with "1. Find files, 2. Apply changes" | Start with "Before starting, clarify: Scope? Approach? Priority?" |

**Why**: Assumptions about scope can invalidate entire workflows.

---

## 5. Over-Engineering Simple Tasks

Using scripts for tasks better as text instructions.

| ❌ Bad | ✅ Good |
|--------|---------|
| 3 Python scripts for commit message formatting | Markdown template with examples |

**Why**: Scripts add maintenance burden. Text instructions are often sufficient.

---

## 6. Duplicate Content

Same information in SKILL.md and references wastes tokens.

| ❌ Bad | ✅ Good |
|--------|---------|
| Full API docs in both SKILL.md and references/api.md | Summary in SKILL.md, details in references/ |

**Why**: Duplicates consume double context and diverge over time.

---

## 7. Kitchen Sink Skills

Skills that try to do everything become unfocused.

| ❌ Bad | ✅ Good |
|--------|---------|
| `document-processor` handling PDF, DOCX, XLSX, images, OCR | `pdf-processor` focused on PDFs only |

**Why**: Focused skills have clearer triggers and more reliable outputs.

---

## 8. Rigid Output Templates

Forcing exact templates when flexibility would produce better results.

| ❌ Bad | ✅ Good |
|--------|---------|
| "ALWAYS use this EXACT format" | "Typical format (adapt as needed)" |

**Why**: Real-world tasks vary. Over-rigid templates produce awkward outputs.

---

## 9. Missing Validation Phase

Executing without verification leads to silent failures.

| ❌ Bad | ✅ Good |
|--------|---------|
| "1. Analyze, 2. Transform, 3. Done!" | Include "4. Validate results, 5. Report summary" |

**Why**: Validation catches errors before they propagate.

---

## 10. Hardcoded Assumptions

Embedding environment-specific details that don't generalize.

| ❌ Bad | ✅ Good |
|--------|---------|
| `cd /Users/john/projects/myapp` | "Navigate to project root" with relative paths |

**Why**: Skills should work across environments.

---

## 11. Inconsistent Naming Conventions

Using placeholders without defining naming rules.

| ❌ Bad | ✅ Good |
|--------|---------|
| `{Entity}`, `{entity}`, `{ENTITY}` used interchangeably | Document conventions: `{Entity}` = PascalCase, `{entity}` = camelCase, etc. |

**Why**: Clear conventions prevent typos and maintain consistency.

---

## 12. Technology-Specific Assumptions

Embedding specific technology details that don't apply universally.

| ❌ Bad | ✅ Good |
|--------|---------|
| "Install Node.js, run npm install, add to React" | "Prerequisites: [list]. Installation: [generic or multi-platform]" |

**Why**: Skills should be adaptable unless explicitly technology-specific.

---

## 13. Missing Trigger Info in Description

Putting trigger information only in the body (not read during trigger matching).

| ❌ Bad | ✅ Good |
|--------|---------|
| Vague description + "When to Use" section in body | Specific triggers in description field |

**Why**: Body content isn't read during trigger evaluation.

---

## 14. No Clear Entry Point

User doesn't know where to start.

| ❌ Bad | ✅ Good |
|--------|---------|
| Jump straight to Feature A, B, C sections | Start with "Quick Start" or "Decision Tree" |

**Why**: Clear entry points reduce cognitive load.

---

## 15. Outdated References

Links to non-existent or outdated files.

| ❌ Bad | ✅ Good |
|--------|---------|
| `See [guide](references/old-guide.md)` (broken) | Verify all links exist and are current |

**Why**: Broken references cause confusion and errors.

---

## 16. No Error Recovery Guidance

Skills that only cover the happy path.

| ❌ Bad | ✅ Good |
|--------|---------|
| "Run script, check output, done" | Include troubleshooting table and "If All Else Fails" section |

**Why**: Error recovery guidance saves time when issues occur.

---

## 17. Assuming Project Context

Referencing project-specific details without explanation.

| ❌ Bad | ✅ Good |
|--------|---------|
| "Use the standard AppService pattern" | Show the pattern with code example |

**Why**: Skills should be self-contained.

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
