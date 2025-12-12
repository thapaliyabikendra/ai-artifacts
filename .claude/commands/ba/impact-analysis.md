---
name: impact-analysis
description: "Analyze change impact on system entities, permissions, and dependencies"
args:
  - name: change
    description: "Description of proposed change or path to requirements"
    required: true
  - name: scope
    description: "Analysis scope: quick | full"
    required: false
    default: "full"
---

# Impact Analysis

Change: **$ARGUMENTS.change**
Scope: **$ARGUMENTS.scope**

## Instructions

### Step 1: Understand the Change

1. If path provided, read the requirements/feature file
2. Extract:
   - New entities being added
   - Existing entities being modified
   - New permissions required
   - Business rules affected
   - API changes

### Step 2: Analyze Domain Impact

Search and analyze:

```
docs/domain/entities/*.md - Entity definitions
docs/domain/permissions.md - Permission structure
docs/domain/business-rules.md - Business rules
api/src/**/Entities/*.cs - Entity implementations
api/src/**/Permissions/*.cs - Permission definitions
```

### Step 3: Generate Impact Report

```markdown
# Impact Analysis: [Change Title]

**Date**: [YYYY-MM-DD]
**Analyst**: Claude
**Status**: Draft | Reviewed | Approved

## Executive Summary

[2-3 sentence summary of the change and its overall impact]

**Impact Level**: 🟢 Low | 🟡 Medium | 🔴 High

## Change Overview

### What's Changing
- [Bullet point summary of changes]

### Why It's Changing
- [Business drivers]

## Entity Impact

### New Entities

| Entity | Base Class | Relationships | Notes |
|--------|------------|---------------|-------|
| [Name] | FullAuditedAggregateRoot | [Relations] | [Notes] |

### Modified Entities

| Entity | Change Type | Fields Affected | Migration Required |
|--------|-------------|-----------------|-------------------|
| [Name] | Add Field | [field1, field2] | Yes |
| [Name] | Modify Field | [field] | Yes |
| [Name] | Add Relation | [FK to Entity] | Yes |

### Unchanged but Affected

| Entity | Impact | Reason |
|--------|--------|--------|
| [Name] | Query changes | New join required |

## Database Impact

### Schema Changes

```sql
-- New tables
CREATE TABLE [TableName] (...)

-- Altered tables
ALTER TABLE [TableName] ADD COLUMN [column] [type];

-- New indexes
CREATE INDEX IX_[name] ON [table]([columns]);
```

### Migration Complexity
- **New Tables**: [count]
- **Altered Tables**: [count]
- **Data Migration**: Required | Not Required
- **Estimated Downtime**: None | < 5 min | > 5 min

## Permission Impact

### New Permissions

| Permission | Description | Default Roles |
|------------|-------------|---------------|
| [Module].[Entity].Create | Create [entity] | Admin, Manager |
| [Module].[Entity].Update | Update [entity] | Admin, Manager |
| [Module].[Entity].Delete | Delete [entity] | Admin |

### Modified Permissions

| Permission | Change | Affected Roles |
|------------|--------|----------------|
| [Existing] | [What changed] | [Roles] |

## API Impact

### New Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | /api/[entity] | [Permission] | List [entities] |
| POST | /api/[entity] | [Permission] | Create [entity] |

### Modified Endpoints

| Endpoint | Change Type | Breaking |
|----------|-------------|----------|
| /api/[existing] | New parameter | No |
| /api/[existing] | Response change | Yes |

### Breaking Changes

| Change | Impact | Migration Path |
|--------|--------|----------------|
| [Description] | [Who's affected] | [How to migrate] |

## Code Impact

### Files to Create

| File | Type | Location |
|------|------|----------|
| [Entity].cs | Entity | Domain/Entities |
| [Entity]Dto.cs | DTO | Contracts/Dtos |
| [Entity]AppService.cs | Service | Application |
| [Entity]Validator.cs | Validator | Application |

### Files to Modify

| File | Change | Risk |
|------|--------|------|
| [File] | [Description] | Low/Med/High |

### Tests Required

| Test Type | Count | Priority |
|-----------|-------|----------|
| Unit Tests | [N] | P1 |
| Integration Tests | [N] | P1 |
| E2E Tests | [N] | P2 |

## Dependency Analysis

### Upstream Dependencies
[Systems/modules this change depends on]

| Dependency | Type | Status |
|------------|------|--------|
| [Name] | API | Ready |
| [Name] | Database | Needs update |

### Downstream Impact
[Systems/modules affected by this change]

| Consumer | Impact | Action Required |
|----------|--------|-----------------|
| [Name] | [Description] | [Action] |

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | Low/Med/High | Low/Med/High | [Strategy] |
| [Risk 2] | Low/Med/High | Low/Med/High | [Strategy] |

## Implementation Checklist

### Phase 1: Preparation
- [ ] Database migration script created
- [ ] Entity definitions reviewed
- [ ] Permission structure approved

### Phase 2: Implementation
- [ ] Entities created
- [ ] DTOs and validators implemented
- [ ] AppServices implemented
- [ ] Permissions configured

### Phase 3: Testing
- [ ] Unit tests written
- [ ] Integration tests written
- [ ] Manual testing completed

### Phase 4: Deployment
- [ ] Migration tested in staging
- [ ] Rollback plan documented
- [ ] Monitoring configured

## Recommendations

1. **[Recommendation 1]**: [Details]
2. **[Recommendation 2]**: [Details]
3. **[Recommendation 3]**: [Details]
```

### Step 4: Output

1. Write to `docs/features/[feature]/impact-analysis.md`
2. Summarize key findings to console
3. Highlight any high-risk items

## Related Skills

- `domain-modeling` - Entity and relationship analysis
- `technical-design-patterns` - Architecture decisions
