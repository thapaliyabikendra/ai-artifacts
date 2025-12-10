# Template Patterns

Universal patterns for skills that generate output from templates, regardless of technology stack.

## Placeholder Conventions

When skills use placeholders that get replaced with user-provided values, define them clearly:

### Standard Naming Conventions

| Placeholder | Case Style | Example Input | Example Output |
|-------------|------------|---------------|----------------|
| `{Entity}` | PascalCase | user order | UserOrder |
| `{entity}` | camelCase | user order | userOrder |
| `{ENTITY}` | UPPER_SNAKE | user order | USER_ORDER |
| `{entity-name}` | kebab-case | user order | user-order |
| `{entity_name}` | snake_case | user order | user_order |
| `{Entities}` | PascalCase Plural | user order | UserOrders |

### Documenting Placeholders

Always include a conventions section when using placeholders:

```markdown
## Naming Conventions

This skill uses these placeholder patterns:
- `{Name}` = PascalCase singular
- `{name}` = camelCase singular
- `{Names}` = PascalCase plural
- `{NAME}` = UPPER_SNAKE_CASE

**Transformations:**
- Input: "order item"
- {Name} → OrderItem
- {name} → orderItem
- {Names} → OrderItems
- {NAME} → ORDER_ITEM
```

---

## Input Gathering Pattern

For skills that need user input before generating output:

```markdown
## User Input Required

Before proceeding, gather the following:

1. **Primary Identifier**
   - Name/Title: [What to call the generated artifact]
   - Type: text, PascalCase preferred

2. **Configuration Options**
   - Option A: [Description] (default: X)
   - Option B: [Description] (default: Y)

3. **Scope Definition**
   - Include: [What's in scope]
   - Exclude: [What's explicitly out of scope]
```

---

## Generation Steps Pattern

Structure generation as verifiable steps:

```markdown
## Generation Steps

### Step 1: [Preparation]
**Input:** [What's needed]
**Output:** [What's produced]
**Verification:** [How to confirm success]

### Step 2: [Core Generation]
**Input:** [What's needed]
**Output:** [What's produced]
**Verification:** [How to confirm success]

### Step 3: [Finalization]
**Input:** [What's needed]
**Output:** [What's produced]
**Verification:** [How to confirm success]
```

---

## Before/After Examples Pattern

Show transformations with concrete examples:

```markdown
## Transformation Examples

### Example 1: [Scenario Name]

**Input:**
```
[Raw input as user would provide]
```

**Output:**
```
[Generated result]
```

**Notes:** [Any special handling or edge cases]

### Example 2: [Another Scenario]
...
```

---

## Checklist Pattern

For verification and completeness:

```markdown
## Completion Checklist

### Required
- [ ] [Critical item 1]
- [ ] [Critical item 2]
- [ ] [Critical item 3]

### Recommended
- [ ] [Best practice 1]
- [ ] [Best practice 2]

### Optional
- [ ] [Enhancement 1]
- [ ] [Enhancement 2]
```

---

## Multi-Platform Pattern

When skills support multiple technologies or platforms:

```markdown
## Platform-Specific Instructions

### [Platform A]

**Prerequisites:**
- [Requirement 1]
- [Requirement 2]

**Steps:**
1. [Platform A specific step]
2. [Platform A specific step]

### [Platform B]

**Prerequisites:**
- [Requirement 1]
- [Requirement 2]

**Steps:**
1. [Platform B specific step]
2. [Platform B specific step]

### Common Steps (All Platforms)

1. [Universal step]
2. [Universal step]
```

---

## Error Recovery Pattern

Guide handling of common failures:

```markdown
## Troubleshooting

### [Error Category 1]

**Symptoms:**
- [What user observes]

**Causes:**
- [Root cause 1]
- [Root cause 2]

**Solutions:**
1. [Fix for cause 1]
2. [Fix for cause 2]

### [Error Category 2]
...
```

---

## File Structure Pattern

When generating multiple files:

```markdown
## Generated Structure

```
output/
├── [file1]          # [Purpose]
├── [file2]          # [Purpose]
├── [directory]/
│   ├── [file3]      # [Purpose]
│   └── [file4]      # [Purpose]
└── [config-file]    # [Purpose]
```

### File Descriptions

| File | Purpose | Required |
|------|---------|----------|
| [file1] | [Description] | Yes |
| [file2] | [Description] | Yes |
| [file3] | [Description] | No |
```

---

## Conditional Generation Pattern

When output varies based on options:

```markdown
## Generation Options

### Option: [Feature Flag]

**When enabled:**
- Generates [additional files/sections]
- Adds [functionality]

**When disabled:**
- Skips [files/sections]
- Uses [simpler approach]

### Decision Tree

```
Start
  ├─ Need [Feature A]?
  │   ├─ Yes → Include [Component 1]
  │   └─ No  → Skip [Component 1]
  └─ Need [Feature B]?
      ├─ Yes → Include [Component 2]
      └─ No  → Use [Default]
```
```

---

## Role-Specific Sections

Different team members may use the same skill differently:

```markdown
## Usage by Role

### For Developers
- Focus on: [Technical aspects]
- Key sections: [List relevant sections]
- Skip: [Sections not relevant]

### For QA/Testers
- Focus on: [Testing aspects]
- Key sections: [List relevant sections]
- Skip: [Sections not relevant]

### For DevOps
- Focus on: [Deployment aspects]
- Key sections: [List relevant sections]
- Skip: [Sections not relevant]

### For Managers/Leads
- Focus on: [Planning aspects]
- Key sections: [List relevant sections]
- Skip: [Sections not relevant]
```
