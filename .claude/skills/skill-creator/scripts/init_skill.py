#!/usr/bin/env python3
"""
Skill Initializer - Creates a new skill from template

Usage:
    init_skill.py <skill-name> --path <path> [--template <type>]

Templates:
    default     - Generic template (default)
    tool        - For file format/tool processing skills (heavy scripts)
    workflow    - For multi-phase process skills (phased execution)
    domain      - For business logic/knowledge skills (heavy references)
    analysis    - For audit/assessment skills (classification frameworks)
    integration - For API/service connection skills (auth + error handling)
    generator   - For code/file generation skills (templates + placeholders)
    pattern     - For best practices documentation (before/after examples)

Examples:
    init_skill.py pdf-processor --path skills/public --template tool
    init_skill.py code-review --path skills/public --template workflow
    init_skill.py company-db --path skills/private --template domain
    init_skill.py security-audit --path skills/public --template analysis
    init_skill.py api-connector --path skills/public --template integration
    init_skill.py crud-service --path skills/public --template generator
    init_skill.py error-handling --path skills/public --template pattern
    init_skill.py my-skill --path skills/public
"""

import sys
import os
from pathlib import Path


# ==================== TEMPLATE DEFINITIONS ====================

SKILL_TEMPLATE_DEFAULT = """---
name: {skill_name}
description: [TODO: Complete and informative explanation of what the skill does and when to use it. Include WHEN to use this skill - specific scenarios, file types, or tasks that trigger it.]
---

# {skill_title}

## Overview

[TODO: 1-2 sentences explaining what this skill enables]

## Structuring This Skill

[TODO: Choose the structure that best fits this skill's purpose. Common patterns:

**1. Workflow-Based** (best for sequential processes)
- Works well when there are clear step-by-step procedures
- Example: DOCX skill with "Workflow Decision Tree" → "Reading" → "Creating" → "Editing"
- Structure: ## Overview → ## Workflow Decision Tree → ## Step 1 → ## Step 2...

**2. Task-Based** (best for tool collections)
- Works well when the skill offers different operations/capabilities
- Example: PDF skill with "Quick Start" → "Merge PDFs" → "Split PDFs" → "Extract Text"
- Structure: ## Overview → ## Quick Start → ## Task Category 1 → ## Task Category 2...

**3. Reference/Guidelines** (best for standards or specifications)
- Works well for brand guidelines, coding standards, or requirements
- Example: Brand styling with "Brand Guidelines" → "Colors" → "Typography" → "Features"
- Structure: ## Overview → ## Guidelines → ## Specifications → ## Usage...

**4. Capabilities-Based** (best for integrated systems)
- Works well when the skill provides multiple interrelated features
- Example: Product Management with "Core Capabilities" → numbered capability list
- Structure: ## Overview → ## Core Capabilities → ### 1. Feature → ### 2. Feature...

Patterns can be mixed and matched as needed. Most skills combine patterns (e.g., start with task-based, add workflow for complex operations).

Delete this entire "Structuring This Skill" section when done - it's just guidance.]

## [TODO: Replace with the first main section based on chosen structure]

[TODO: Add content here. See examples in existing skills:
- Code samples for technical skills
- Decision trees for complex workflows
- Concrete examples with realistic user requests
- References to scripts/templates/references as needed]

## Resources

This skill includes example resource directories that demonstrate how to organize different types of bundled resources:

### scripts/
Executable code (Python/Bash/etc.) that can be run directly to perform specific operations.

**Examples from other skills:**
- PDF skill: `fill_fillable_fields.py`, `extract_form_field_info.py` - utilities for PDF manipulation
- DOCX skill: `document.py`, `utilities.py` - Python modules for document processing

**Appropriate for:** Python scripts, shell scripts, or any executable code that performs automation, data processing, or specific operations.

**Note:** Scripts may be executed without loading into context, but can still be read by Claude for patching or environment adjustments.

### references/
Documentation and reference material intended to be loaded into context to inform Claude's process and thinking.

**Examples from other skills:**
- Product management: `communication.md`, `context_building.md` - detailed workflow guides
- BigQuery: API reference documentation and query examples
- Finance: Schema documentation, company policies

**Appropriate for:** In-depth documentation, API references, database schemas, comprehensive guides, or any detailed information that Claude should reference while working.

### assets/
Files not intended to be loaded into context, but rather used within the output Claude produces.

**Examples from other skills:**
- Brand styling: PowerPoint template files (.pptx), logo files
- Frontend builder: HTML/React boilerplate project directories
- Typography: Font files (.ttf, .woff2)

**Appropriate for:** Templates, boilerplate code, document templates, images, icons, fonts, or any files meant to be copied or used in the final output.

---

**Any unneeded directories can be deleted.** Not every skill requires all three types of resources.
"""

SKILL_TEMPLATE_TOOL = """---
name: {skill_name}
description: [TODO: Process, manipulate, and transform [FILE_TYPE] files. Use when: (1) reading/extracting content from [FILE_TYPE], (2) creating new [FILE_TYPE] files, (3) modifying existing [FILE_TYPE] files, (4) converting [FILE_TYPE] to other formats.]
---

# {skill_title}

Process and manipulate [FILE_TYPE] files with deterministic scripts.

## Quick Start

**Common operations:**

```bash
# Extract content
python scripts/extract.py input.file output.txt

# Create new file
python scripts/create.py --template default output.file

# Transform/convert
python scripts/convert.py input.file --format target_format
```

## Operation Selection

What do you need to do?

| Task | Script | Example |
|------|--------|---------|
| Extract content | `extract.py` | `python scripts/extract.py doc.file` |
| Create new | `create.py` | `python scripts/create.py output.file` |
| Modify existing | `modify.py` | `python scripts/modify.py doc.file --changes ...` |
| Convert format | `convert.py` | `python scripts/convert.py doc.file --format pdf` |

## Detailed Operations

### Extracting Content

[TODO: Add detailed instructions for extraction operations]

### Creating Files

[TODO: Add detailed instructions for creation operations]

### Modifying Files

[TODO: Add detailed instructions for modification operations]

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| FileNotFound | Input doesn't exist | Verify file path |
| InvalidFormat | Corrupted file | Check file integrity |
| PermissionDenied | File locked | Close other applications |

## References

- [API Reference](references/api-reference.md) - Complete function documentation
- [Troubleshooting](references/troubleshooting.md) - Common issues and solutions
"""

SKILL_TEMPLATE_WORKFLOW = """---
name: {skill_name}
description: [TODO: Guide the [PROCESS_NAME] process. Use when: (1) starting a new [PROCESS], (2) continuing an in-progress [PROCESS], (3) reviewing [PROCESS] results, (4) troubleshooting [PROCESS] issues.]
---

# {skill_title}

Guide multi-phase [PROCESS_NAME] with clear checkpoints and validation.

## User Input Required

Before starting, clarify:

1. **Scope**: What's included in this [PROCESS]?
2. **Approach**: What strategy to use? (Conservative / Standard / Aggressive)
3. **Priority**: Where to focus first?

## Process Overview

```
Phase 1: Assessment     → Understand current state, identify issues
Phase 2: Planning       → Design approach, prioritize tasks
Phase 3: Implementation → Execute changes incrementally
Phase 4: Validation     → Verify results, document outcomes
```

---

## Phase 1: Assessment

### 1.1 Analyze Current State

Examine to understand:
- Current patterns and approaches
- Areas needing attention
- Existing constraints

### 1.2 Create Inventory

Classify findings:

**High Priority:** [Define criteria]
**Medium Priority:** [Define criteria]
**Low Priority:** [Define criteria]

---

## Phase 2: Planning

Based on assessment, determine approach and create task list.

---

## Phase 3: Implementation

For each task:
1. Verify preconditions
2. Apply change
3. Verify postconditions
4. Document what changed

---

## Phase 4: Validation

**Deliverables:**
- [ ] All planned changes applied
- [ ] No regressions introduced
- [ ] Documentation updated
"""

SKILL_TEMPLATE_DOMAIN = """---
name: {skill_name}
description: [TODO: Provide [DOMAIN] knowledge and guidelines. Use when: (1) querying [DOMAIN] data, (2) following [DOMAIN] conventions, (3) understanding [DOMAIN] relationships, (4) applying [DOMAIN] rules.]
---

# {skill_title}

[DOMAIN] knowledge base with schemas, conventions, and guidelines.

## Overview

[TODO: 2-3 sentences about what this domain covers]

## Quick Reference

### Common Patterns

**[Pattern 1]:**
```
[TODO: Add example]
```

**[Pattern 2]:**
```
[TODO: Add example]
```

## Schema References

| Area | Reference | Description |
|------|-----------|-------------|
| [Area 1] | [references/area1.md](references/area1.md) | [Description] |
| [Area 2] | [references/area2.md](references/area2.md) | [Description] |

## Conventions

- [Convention 1]: [Description]
- [Convention 2]: [Description]

## Relationships

[TODO: Document key relationships between domain entities]

## Important Notes

[TODO: Add domain-specific notes, gotchas, or warnings]
"""

SKILL_TEMPLATE_ANALYSIS = """---
name: {skill_name}
description: [TODO: Analyze and assess [TARGET] for [PURPOSE]. Use when: (1) auditing [TARGET], (2) identifying issues, (3) generating assessment reports, (4) prioritizing remediation efforts.]
---

# {skill_title}

Systematic analysis with classification and actionable recommendations.

## Scope Definition

Before starting, define:
1. **Target**: What to analyze?
2. **Depth**: Quick scan / Standard / Deep dive
3. **Focus**: All categories or specific ones

## Analysis Checklist

### Category 1: [Name]
- [ ] [Check item 1]
- [ ] [Check item 2]

### Category 2: [Name]
- [ ] [Check item 1]
- [ ] [Check item 2]

## Classification Framework

### Critical (P0)
Immediate attention required:
- [Criteria]

### High (P1)
Address soon:
- [Criteria]

### Medium (P2)
Plan to address:
- [Criteria]

### Low (P3)
Address when convenient:
- [Criteria]

## Report Template

```markdown
# [Analysis Type] Report

## Executive Summary
[Overview of key findings]

## Findings by Severity

### Critical (P0)
### High (P1)
### Medium (P2)
### Low (P3)

## Detailed Findings

### [Finding Title]
- **Severity:** [P0/P1/P2/P3]
- **Location:** [Where found]
- **Description:** [What was found]
- **Impact:** [Consequences]
- **Remediation:** [How to fix]

## Recommendations
[Prioritized action items]
```
"""

SKILL_TEMPLATE_INTEGRATION = """---
name: {skill_name}
description: [TODO: Integrate with [SERVICE/API]. Use when: (1) connecting to [SERVICE], (2) fetching data from [API], (3) performing [OPERATIONS], (4) handling [SERVICE] authentication or webhooks.]
---

# {skill_title}

Connect and interact with [SERVICE/API] with proper authentication and error handling.

## Authentication

**Required credentials:**
- [Credential 1]: [Description]
- [Credential 2]: [Description]

**Setup:**
```bash
# Environment variables
export SERVICE_API_KEY=your_api_key
export SERVICE_URL=https://api.service.com
```

## Common Operations

| Operation | Method | Description |
|-----------|--------|-------------|
| Fetch data | GET | Retrieve records |
| Create record | POST | Create new entry |
| Update record | PUT | Modify existing entry |
| Delete record | DELETE | Remove entry |

## API Endpoints

### [Endpoint Category 1]

**GET /resource**
```
Request: GET /api/resource?param=value
Response: {{ "data": [...], "total": 100 }}
```

### [Endpoint Category 2]

**POST /resource**
```
Request: POST /api/resource
Body: {{ "field": "value" }}
Response: {{ "id": "123", "status": "created" }}
```

## Error Handling

| Code | Meaning | Resolution |
|------|---------|------------|
| 400 | Bad request | Validate input parameters |
| 401 | Unauthorized | Check API key/token |
| 403 | Forbidden | Verify permissions |
| 404 | Not found | Check resource ID |
| 429 | Rate limited | Implement backoff strategy |
| 500 | Server error | Retry with exponential backoff |

## Rate Limits

- Requests per minute: [N]
- Requests per day: [N]
- Burst limit: [N]

**Handling rate limits:**
```
Wait time = min(base_delay * 2^attempt, max_delay)
```

## Webhooks (if applicable)

**Receiving webhooks:**
1. Configure endpoint URL in [SERVICE] settings
2. Verify webhook signature
3. Respond with 200 OK within timeout

## References

- [API Reference](references/api-reference.md) - Complete endpoint documentation
- [Authentication Guide](references/authentication.md) - Detailed auth setup
"""

SKILL_TEMPLATE_GENERATOR = """---
name: {skill_name}
description: [TODO: Generate [ARTIFACT_TYPE] from templates. Use when: (1) creating new [ARTIFACT], (2) scaffolding [COMPONENT], (3) generating boilerplate for [PURPOSE], (4) automating [TASK] creation.]
---

# {skill_title}

Generate [ARTIFACT_TYPE] from templates with consistent patterns and structure.

## Workflow

1. **Gather information** from user:
   - Name (e.g., "Product", "UserProfile")
   - Properties/Fields (e.g., "name:string, price:decimal")
   - Options (e.g., include tests, include documentation)

2. **Generate files** using templates:
   - `[Primary file]` - [references/primary-template.md](references/primary-template.md)
   - `[Secondary file]` - [references/secondary-template.md](references/secondary-template.md)
   - `[Test file]` (if requested) - [references/test-template.md](references/test-template.md)

3. **Replace placeholders:**

| Placeholder | Format | Example |
|-------------|--------|---------|
| `{{Name}}` | PascalCase singular | Product |
| `{{name}}` | camelCase singular | product |
| `{{Names}}` | PascalCase plural | Products |
| `{{names}}` | camelCase plural | products |
| `{{name-kebab}}` | kebab-case | product |
| `{{NAME}}` | UPPER_SNAKE | PRODUCT |

4. **Create files** in appropriate locations.

## Generated Structure

```
output/
├── [PrimaryFile]          # Main generated file
├── [SecondaryFile]        # Supporting file
└── [TestFile]             # Test file (optional)
```

## Post-Generation Steps

1. [Integration step 1]
2. [Integration step 2]
3. [Verification step]

## Options

| Option | Default | Description |
|--------|---------|-------------|
| Include tests | Yes | Generate test files |
| Include docs | No | Generate documentation |
| [Custom option] | [Default] | [Description] |

## Examples

**Example 1: Basic generation**
```
Generate a Product with name:string, price:decimal
```

**Example 2: With options**
```
Generate a UserProfile with firstName:string, lastName:string, email:string
Include tests and documentation
```

## References

- [Primary Template](references/primary-template.md)
- [Secondary Template](references/secondary-template.md)
- [Test Template](references/test-template.md)
"""

SKILL_TEMPLATE_PATTERN = """---
name: {skill_name}
description: [TODO: Document [PATTERN_TYPE] best practices. Use when: (1) implementing [PATTERN], (2) reviewing code for [PATTERN] compliance, (3) learning [PATTERN] approaches, (4) establishing [PATTERN] standards.]
---

# {skill_title}

Best practices and patterns for [DOMAIN/TOPIC].

## When to Use

| Scenario | Recommended Pattern | Why |
|----------|-------------------|-----|
| [Scenario 1] | [Pattern A] | [Reason] |
| [Scenario 2] | [Pattern B] | [Reason] |
| [Scenario 3] | [Pattern C] | [Reason] |

## Pattern Overview

### Pattern A: [Name]

**When to use:** [Conditions]

**Before:**
```[language]
// Problem code
[bad example]
```

**After:**
```[language]
// Solution code
[good example]
```

**Key points:**
- [Point 1]
- [Point 2]
- [Point 3]

### Pattern B: [Name]

**When to use:** [Conditions]

**Before:**
```[language]
// Problem code
[bad example]
```

**After:**
```[language]
// Solution code
[good example]
```

## Language-Specific Examples

### [Language 1]

```[language1]
// [Language 1] implementation
[example]
```

### [Language 2]

```[language2]
// [Language 2] implementation
[example]
```

## Anti-Patterns

### Anti-Pattern 1: [Name]

**Problem:**
```[language]
// What NOT to do
[bad example]
```

**Why it's bad:** [Explanation]

**Solution:**
```[language]
// What to do instead
[good example]
```

### Anti-Pattern 2: [Name]

**Problem:**
```[language]
// What NOT to do
[bad example]
```

**Why it's bad:** [Explanation]

## Decision Tree

```
Start
  ├── [Condition 1]?
  │   ├── Yes → Use Pattern A
  │   └── No  → Continue...
  ├── [Condition 2]?
  │   ├── Yes → Use Pattern B
  │   └── No  → Use Pattern C
```

## Checklist

When implementing [PATTERN]:

- [ ] [Verification item 1]
- [ ] [Verification item 2]
- [ ] [Verification item 3]
- [ ] [Verification item 4]

## References

- [Detailed Pattern A](references/pattern-a.md)
- [Detailed Pattern B](references/pattern-b.md)
- [Common Mistakes](references/common-mistakes.md)
"""

# Map template names to content
TEMPLATES = {
    'default': SKILL_TEMPLATE_DEFAULT,
    'tool': SKILL_TEMPLATE_TOOL,
    'workflow': SKILL_TEMPLATE_WORKFLOW,
    'domain': SKILL_TEMPLATE_DOMAIN,
    'analysis': SKILL_TEMPLATE_ANALYSIS,
    'integration': SKILL_TEMPLATE_INTEGRATION,
    'generator': SKILL_TEMPLATE_GENERATOR,
    'pattern': SKILL_TEMPLATE_PATTERN,
}

EXAMPLE_SCRIPT = '''#!/usr/bin/env python3
"""
Example helper script for {skill_name}

This is a placeholder script that can be executed directly.
Replace with actual implementation or delete if not needed.

Example real scripts from other skills:
- pdf/scripts/fill_fillable_fields.py - Fills PDF form fields
- pdf/scripts/convert_pdf_to_images.py - Converts PDF pages to images
"""

def main():
    print("This is an example script for {skill_name}")
    # TODO: Add actual script logic here
    # This could be data processing, file conversion, API calls, etc.

if __name__ == "__main__":
    main()
'''

EXAMPLE_REFERENCE = """# Reference Documentation for {skill_title}

This is a placeholder for detailed reference documentation.
Replace with actual reference content or delete if not needed.

Example real reference docs from other skills:
- product-management/references/communication.md - Comprehensive guide for status updates
- product-management/references/context_building.md - Deep-dive on gathering context
- bigquery/references/ - API references and query examples

## When Reference Docs Are Useful

Reference docs are ideal for:
- Comprehensive API documentation
- Detailed workflow guides
- Complex multi-step processes
- Information too lengthy for main SKILL.md
- Content that's only needed for specific use cases

## Structure Suggestions

### API Reference Example
- Overview
- Authentication
- Endpoints with examples
- Error codes
- Rate limits

### Workflow Guide Example
- Prerequisites
- Step-by-step instructions
- Common patterns
- Troubleshooting
- Best practices
"""

EXAMPLE_ASSET = """# Example Asset File

This placeholder represents where asset files would be stored.
Replace with actual asset files (templates, images, fonts, etc.) or delete if not needed.

Asset files are NOT intended to be loaded into context, but rather used within
the output Claude produces.

Example asset files from other skills:
- Brand guidelines: logo.png, slides_template.pptx
- Frontend builder: hello-world/ directory with HTML/React boilerplate
- Typography: custom-font.ttf, font-family.woff2
- Data: sample_data.csv, test_dataset.json

## Common Asset Types

- Templates: .pptx, .docx, boilerplate directories
- Images: .png, .jpg, .svg, .gif
- Fonts: .ttf, .otf, .woff, .woff2
- Boilerplate code: Project directories, starter files
- Icons: .ico, .svg
- Data files: .csv, .json, .xml, .yaml

Note: This is a text placeholder. Actual assets can be any file type.
"""


def title_case_skill_name(skill_name):
    """Convert hyphenated skill name to Title Case for display."""
    return ' '.join(word.capitalize() for word in skill_name.split('-'))


def init_skill(skill_name, path, template_type='default'):
    """
    Initialize a new skill directory with template SKILL.md.

    Args:
        skill_name: Name of the skill
        path: Path where the skill directory should be created
        template_type: Type of template to use (default, tool, workflow, domain, analysis)

    Returns:
        Path to created skill directory, or None if error
    """
    # Validate template type
    if template_type not in TEMPLATES:
        print(f"❌ Error: Unknown template type '{template_type}'")
        print(f"   Available templates: {', '.join(TEMPLATES.keys())}")
        return None

    # Determine skill directory path
    skill_dir = Path(path).resolve() / skill_name

    # Check if directory already exists
    if skill_dir.exists():
        print(f"❌ Error: Skill directory already exists: {skill_dir}")
        return None

    # Create skill directory
    try:
        skill_dir.mkdir(parents=True, exist_ok=False)
        print(f"✅ Created skill directory: {skill_dir}")
    except Exception as e:
        print(f"❌ Error creating directory: {e}")
        return None

    # Create SKILL.md from template
    skill_title = title_case_skill_name(skill_name)
    template_content = TEMPLATES[template_type]
    skill_content = template_content.format(
        skill_name=skill_name,
        skill_title=skill_title
    )

    skill_md_path = skill_dir / 'SKILL.md'
    try:
        skill_md_path.write_text(skill_content)
        print("✅ Created SKILL.md")
    except Exception as e:
        print(f"❌ Error creating SKILL.md: {e}")
        return None

    # Create resource directories with example files
    try:
        # Create scripts/ directory with example script
        scripts_dir = skill_dir / 'scripts'
        scripts_dir.mkdir(exist_ok=True)
        example_script = scripts_dir / 'example.py'
        example_script.write_text(EXAMPLE_SCRIPT.format(skill_name=skill_name))
        # Set executable permission on Unix-like systems
        if os.name != 'nt':  # Not Windows
            example_script.chmod(0o755)
        print("✅ Created scripts/example.py")

        # Create references/ directory with example reference doc
        references_dir = skill_dir / 'references'
        references_dir.mkdir(exist_ok=True)
        example_reference = references_dir / 'api_reference.md'
        example_reference.write_text(EXAMPLE_REFERENCE.format(skill_title=skill_title))
        print("✅ Created references/api_reference.md")

        # Create assets/ directory with example asset placeholder
        assets_dir = skill_dir / 'assets'
        assets_dir.mkdir(exist_ok=True)
        example_asset = assets_dir / 'example_asset.txt'
        example_asset.write_text(EXAMPLE_ASSET)
        print("✅ Created assets/example_asset.txt")
    except Exception as e:
        print(f"❌ Error creating resource directories: {e}")
        return None

    # Print next steps
    print(f"\n✅ Skill '{skill_name}' initialized successfully at {skill_dir}")
    print("\nNext steps:")
    print("1. Edit SKILL.md to complete the TODO items and update the description")
    print("2. Customize or delete the example files in scripts/, references/, and assets/")
    print("3. Run the validator when ready to check the skill structure")

    return skill_dir


def main():
    if len(sys.argv) < 4 or '--path' not in sys.argv:
        print("Usage: init_skill.py <skill-name> --path <path> [--template <type>]")
        print("\nSkill name requirements:")
        print("  - Hyphen-case identifier (e.g., 'data-analyzer')")
        print("  - Lowercase letters, digits, and hyphens only")
        print("  - Max 64 characters")
        print("  - Must match directory name exactly")
        print("\nAvailable templates:")
        for name in TEMPLATES.keys():
            print(f"  - {name}")
        print("\nExamples:")
        print("  init_skill.py my-new-skill --path skills/public")
        print("  init_skill.py api-helper --path skills/private --template integration")
        print("  init_skill.py code-review --path skills/public --template workflow")
        sys.exit(1)

    skill_name = sys.argv[1]

    # Parse --path argument
    path_idx = sys.argv.index('--path')
    if path_idx + 1 >= len(sys.argv) or sys.argv[path_idx + 1].startswith('--'):
        print("Error: --path requires a value")
        sys.exit(1)
    path = sys.argv[path_idx + 1]

    # Parse optional --template argument
    template_type = 'default'
    if '--template' in sys.argv:
        template_idx = sys.argv.index('--template')
        if template_idx + 1 >= len(sys.argv) or sys.argv[template_idx + 1].startswith('--'):
            print("Error: --template requires a value")
            print(f"Available templates: {', '.join(TEMPLATES.keys())}")
            sys.exit(1)
        template_type = sys.argv[template_idx + 1]
        if template_type not in TEMPLATES:
            print(f"Error: Unknown template '{template_type}'")
            print(f"Available templates: {', '.join(TEMPLATES.keys())}")
            sys.exit(1)

    print(f"🚀 Initializing skill: {skill_name}")
    print(f"   Location: {path}")
    print(f"   Template: {template_type}")
    print()

    result = init_skill(skill_name, path, template_type)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
