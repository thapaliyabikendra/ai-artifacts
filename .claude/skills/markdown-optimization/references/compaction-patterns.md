# Compaction Patterns

> Techniques for reducing markdown document size while preserving information.

## Quick Reference

| Technique | Typical Savings | Best For |
|-----------|-----------------|----------|
| Prose → Table | 50-70% | Lists, comparisons, definitions |
| Prose → Bullets | 40-60% | Sequential items, features |
| Extract Examples | 60-80% | Long code blocks |
| Remove Redundancy | 30-50% | Repeated explanations |
| Progressive Disclosure | 50-70% | Advanced content |
| Consolidate Sections | 30-40% | Similar content |

---

## Pattern 1: Prose to Table

### Detection

Look for:
- Paragraphs listing multiple items with descriptions
- "X is..., Y is..., Z is..." patterns
- Feature descriptions with attributes
- Role/permission descriptions

### Before (15 lines)

```markdown
## User Roles

The system supports three types of users. Administrators have full access
to all system features including user management, system configuration,
and comprehensive reporting capabilities. They can also manage other
administrators. Managers have access to team-level features including
viewing reports for their team, managing team members, and approving
requests. However, they cannot access system-wide configuration.
Regular users have limited access focused on their own work, including
viewing their own data, submitting requests, and accessing basic reports
relevant to their role.
```

### After (7 lines)

```markdown
## User Roles

| Role | Access Level | Capabilities |
|------|--------------|--------------|
| Admin | Full | User management, config, all reports, manage admins |
| Manager | Team | Team reports, member management, approvals |
| User | Self | Own data, submit requests, basic reports |
```

**Savings**: 53%

---

## Pattern 2: Prose to Bullets

### Detection

Look for:
- Paragraphs with comma-separated lists
- "First..., then..., finally..." patterns
- Step descriptions embedded in prose

### Before (10 lines)

```markdown
## Setup Process

To set up the development environment, you'll first need to install
Node.js version 18 or higher. After that, clone the repository from
GitHub using the standard git clone command. Once cloned, navigate
to the project directory and run npm install to install all dependencies.
You should also copy the .env.example file to .env and configure your
local settings. Finally, run the database migrations using npm run migrate
and start the development server with npm run dev.
```

### After (9 lines)

```markdown
## Setup Process

1. Install Node.js 18+
2. Clone repository: `git clone <repo-url>`
3. Install dependencies: `npm install`
4. Configure environment: `cp .env.example .env`
5. Run migrations: `npm run migrate`
6. Start server: `npm run dev`
```

**Savings**: 10% (but much more scannable)

---

## Pattern 3: Extract Examples

### Detection

Look for:
- Code blocks > 30 lines
- Multiple similar examples
- Tutorial-style inline code
- Complete implementation examples

### Before (60 lines inline)

```markdown
## API Usage

Here's a complete example of using the API:

```python
import requests
from typing import Optional

class APIClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })

    # ... 40 more lines of implementation
```
```

### After (8 lines)

```markdown
## API Usage

Quick example:
```python
client = APIClient(base_url, api_key)
response = client.get("/users")
```

**Complete implementation**: See [examples/api-client.py](examples/api-client.py)
```

**Savings**: 87%

---

## Pattern 4: Remove Redundancy

### Detection

Look for:
- Same concept explained multiple times
- Repeated disclaimers or warnings
- Copy-pasted sections
- Similar tables in different files

### Before (appears in 3 files)

```markdown
<!-- In architecture.md -->
## Entity Base Classes
ABP provides several base classes for entities...
[20 lines of explanation]

<!-- In patterns.md -->
## Entity Inheritance
When creating entities, ABP offers base classes...
[20 lines of similar explanation]

<!-- In entities.md -->
## Base Classes
ABP Framework includes entity base classes...
[20 lines of similar explanation]
```

### After (single source)

```markdown
<!-- In entities.md (authoritative source) -->
## Entity Base Classes
[Complete 20-line explanation]

<!-- In architecture.md -->
## Entity Base Classes
See [Entity Base Classes](entities.md#entity-base-classes) for inheritance patterns.

<!-- In patterns.md -->
## Entity Inheritance
Entity patterns use ABP base classes. See [entities.md](entities.md#entity-base-classes).
```

**Savings**: 67% (40 lines → 13 lines total)

---

## Pattern 5: Progressive Disclosure

### Detection

Look for:
- Long sections mixing basic and advanced content
- "For advanced users..." paragraphs
- Optional configuration details
- Edge cases and exceptions

### Before (200 lines)

```markdown
## Authentication

### Basic Setup
[30 lines - essential]

### Configuration Options
[50 lines - detailed config]

### Advanced: Custom Providers
[60 lines - advanced]

### Troubleshooting
[60 lines - edge cases]
```

### After (50 lines main + linked)

```markdown
## Authentication

### Basic Setup
[30 lines - essential]

### Configuration
Key options:
| Option | Default | Description |
[Table - 10 lines]

**All options**: See [auth-config.md](references/auth-config.md)

### Advanced Topics
- **Custom providers**: [auth-providers.md](references/auth-providers.md)
- **Troubleshooting**: [auth-troubleshooting.md](references/auth-troubleshooting.md)
```

**Savings**: 75% in main file

---

## Pattern 6: Consolidate Sections

### Detection

Look for:
- Multiple small sections on related topics
- Sections with only 1-2 paragraphs
- Fragmented information

### Before (25 lines)

```markdown
## Database Configuration

### PostgreSQL
Set `DATABASE_TYPE=postgresql` in your environment.

### Connection String
Use format: `Host=localhost;Database=mydb;Username=user;Password=pass`

### Connection Pooling
Default pool size is 100. Adjust with `MAX_POOL_SIZE`.

### Timeouts
Default timeout is 30 seconds. Set `COMMAND_TIMEOUT` to change.
```

### After (12 lines)

```markdown
## Database Configuration

| Setting | Default | Environment Variable |
|---------|---------|---------------------|
| Type | PostgreSQL | `DATABASE_TYPE` |
| Connection String | - | `DATABASE_URL` |
| Pool Size | 100 | `MAX_POOL_SIZE` |
| Timeout | 30s | `COMMAND_TIMEOUT` |

**Connection string format**: `Host=localhost;Database=mydb;Username=user;Password=pass`
```

**Savings**: 52%

---

## Pattern 7: Simplify Headings

### Detection

Look for:
- Deeply nested headings (h4, h5, h6)
- Single-item subsections
- Heading for every paragraph

### Before

```markdown
## API
### REST API
#### Endpoints
##### User Endpoints
###### GET /users
Returns list of users.
###### POST /users
Creates a user.
```

### After

```markdown
## REST API

### User Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/users` | List users |
| POST | `/users` | Create user |
```

---

## Pattern 8: Inline Code Context

### Detection

Look for:
- Short code snippets with long explanations
- Obvious code with comments explaining each line
- Code blocks surrounded by repetitive text

### Before (12 lines)

```markdown
To install the package, you need to use npm. Open your terminal and
navigate to your project directory. Then run the following command:

```bash
npm install my-package
```

This will download the package from the npm registry and add it to
your node_modules folder. It will also update your package.json file
to include the new dependency.
```

### After (3 lines)

```markdown
Install:
```bash
npm install my-package
```
```

**Savings**: 75%

---

## Compaction Decision Tree

```
Is content > threshold?
│
├─ No → Keep as-is
│
└─ Yes → What type?
    │
    ├─ Prose describing items → Pattern 1: Table
    │
    ├─ Sequential steps → Pattern 2: Bullets
    │
    ├─ Code > 30 lines → Pattern 3: Extract
    │
    ├─ Repeated elsewhere → Pattern 4: Single source
    │
    ├─ Mixed basic/advanced → Pattern 5: Progressive
    │
    ├─ Many small sections → Pattern 6: Consolidate
    │
    └─ Deeply nested → Pattern 7: Flatten
```

## Measuring Success

| Metric | Target | Method |
|--------|--------|--------|
| Line reduction | 30-50% | `wc -l before after` |
| Readability | Maintained | Manual review |
| Information | Preserved | Diff review |
| Scannability | Improved | Section lengths |
