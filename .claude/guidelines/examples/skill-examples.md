# Skill Examples

> Good and bad examples of skill structure. Reference for creating effective skills.

## Good Example: Concise with Progressive Disclosure

```markdown
---
name: pdf-processing
description: |
  Extract text and tables from PDF files, fill forms, merge documents.
  Use when: (1) working with PDF files, (2) extracting document content,
  (3) filling or merging PDFs.
tech_stack: [python]
---

# PDF Processing

## Quick Start

Extract text from a PDF:

```python
import pdfplumber

with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

## Core Operations

### Extract Tables

```python
with pdfplumber.open("file.pdf") as pdf:
    tables = pdf.pages[0].extract_tables()
    for table in tables:
        print(table)
```

### Merge PDFs

```python
from PyPDF2 import PdfMerger

merger = PdfMerger()
merger.append("file1.pdf")
merger.append("file2.pdf")
merger.write("merged.pdf")
merger.close()
```

## Advanced Topics

**Form filling**: See [forms.md](references/forms.md)
**OCR extraction**: See [ocr.md](references/ocr.md)
**Large files**: See [performance.md](references/performance.md)
```

**Why it's good:**
- Quick Start section for immediate use
- Core operations cover 80% of use cases
- Advanced topics link to references (progressive disclosure)
- Under 500 lines
- Specific trigger scenarios in description

---

## Good Example: ABP Pattern Skill

```markdown
---
name: abp-entity-patterns
description: |
  ABP Framework domain layer patterns including entities, aggregates, repositories,
  domain services, and data seeding. Use when: (1) creating entities with proper
  base classes, (2) implementing custom repositories, (3) writing domain services.
tech_stack: [dotnet, csharp, abp]
---

# ABP Entity Patterns

## Entity Base Classes

| Base Class | Use When |
|------------|----------|
| `Entity<TKey>` | Simple entity without auditing |
| `AuditedEntity<TKey>` | Need creation/modification tracking |
| `FullAuditedEntity<TKey>` | Need soft delete + audit |
| `AggregateRoot<TKey>` | Root of an aggregate |
| `FullAuditedAggregateRoot<TKey>` | Aggregate root with full audit |

## Standard Entity Template

```csharp
public class {Entity} : FullAuditedAggregateRoot<Guid>
{
    public string Name { get; private set; }

    protected {Entity}() { } // EF Core constructor

    public {Entity}(Guid id, string name) : base(id)
    {
        SetName(name);
    }

    public void SetName(string name)
    {
        Name = Check.NotNullOrWhiteSpace(name, nameof(name), maxLength: 100);
    }
}
```

## Repository Pattern

```csharp
// Interface in Domain project
public interface I{Entity}Repository : IRepository<{Entity}, Guid>
{
    Task<{Entity}?> FindByNameAsync(string name);
}

// Implementation in EntityFrameworkCore project
public class {Entity}Repository : EfCoreRepository<{DbContext}, {Entity}, Guid>,
    I{Entity}Repository
{
    public async Task<{Entity}?> FindByNameAsync(string name)
    {
        return await (await GetDbSetAsync())
            .FirstOrDefaultAsync(x => x.Name == name);
    }
}
```

## Advanced Topics

**Domain services**: See [domain-services.md](references/domain-services.md)
**Specifications**: See [specifications.md](references/specifications.md)
**Data seeding**: See [data-seeding.md](references/data-seeding.md)
```

**Why it's good:**
- Uses `{Entity}` placeholder (portable)
- Table for quick reference
- Templates are concise
- Links to advanced topics

---

## Bad Example: Verbose and Bloated

```markdown
---
name: pdf-helper
description: Helps with documents    ← Too vague, no triggers
---

# PDF Helper

PDF (Portable Document Format) files are a common file format that was
developed by Adobe Systems in the 1990s. PDFs are widely used because
they preserve the formatting of documents regardless of the software,
hardware, or operating system used to view them. This makes PDFs ideal
for sharing documents that need to look the same on any device.

← Unnecessary explanation - Claude knows what PDFs are

To work with PDFs in Python, there are many libraries available. Some
popular options include:

1. PyPDF2 - A pure Python library for reading and writing PDFs
2. pdfplumber - Great for extracting text and tables
3. PyMuPDF - Fast and feature-rich
4. reportlab - For creating PDFs from scratch

Each library has its strengths and weaknesses. PyPDF2 is good for basic
operations but struggles with complex PDFs. pdfplumber is excellent for
text extraction but can be slow on large files...

← More unnecessary explanation

## Installing Libraries

First, you'll need to install the required libraries. Open your terminal
and run the following commands:

```bash
pip install pdfplumber
pip install PyPDF2
```

← Basic installation doesn't need to be here

## Extracting Text

Now let's look at how to extract text from a PDF file. First, we need to
import the library, then open the file, and finally extract the text...

← Overly verbose introduction

```python
# Import the pdfplumber library
import pdfplumber

# Open the PDF file
with pdfplumber.open("file.pdf") as pdf:
    # Get the first page
    first_page = pdf.pages[0]
    # Extract the text from the page
    text = first_page.extract_text()
    # Print the extracted text
    print(text)
```

← Comments explain obvious things

[... continues for 800+ lines with similar verbosity]
```

**Problems:**
- Vague description with no trigger scenarios
- Explains concepts Claude already knows
- Verbose prose instead of concise examples
- Over-commented code
- Way over 500 line limit
- No progressive disclosure

---

## Transformation Guide

| Bad Pattern | Good Pattern |
|-------------|--------------|
| Lengthy explanations | Assume Claude knows, show code |
| Over-commented code | Self-documenting code, minimal comments |
| All content in SKILL.md | Core in SKILL.md, advanced in references/ |
| Vague description | Specific + 3 trigger scenarios |
| Generic helper name | Descriptive action-based name |

## Related

- [Progressive Disclosure](../patterns/progressive-disclosure.md)
- [Skill Optimization](../patterns/skill-optimization.md)
- [Antipatterns](antipatterns.md)
