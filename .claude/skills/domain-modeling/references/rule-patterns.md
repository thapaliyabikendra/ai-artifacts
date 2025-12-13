# Business Rule Patterns

Common patterns for business rules in domain-driven applications.

## Rule Categories

| Category | Code | Description |
|----------|------|-------------|
| Patient | PAT | Patient-related rules |
| Doctor | DOC | Doctor-related rules |
| Appointment | APT | Scheduling rules |
| Schedule | SCH | Working hours rules |
| Medical | MED | Medical record rules |
| System | SYS | Cross-cutting rules |

---

## Uniqueness Rules

### Pattern

```markdown
**BR-{CAT}-XXX: Unique {Field}**

**Description**: {Entity} {field} must be unique across the system
**Trigger**: Create, Update
**Condition**: No other active {entity} exists with the same {field}
**Action**: Reject with "{Field} already exists"
**Exception**: Soft-deleted records are excluded
```

### Examples

| ID | Rule | Entity | Field |
|----|------|--------|-------|
| BR-PAT-001 | Unique email | Patient | Email |
| BR-DOC-001 | Unique license number | Doctor | LicenseNumber |
| BR-USR-001 | Unique username | User | Username |

---

## Referential Integrity Rules

### Pattern

```markdown
**BR-{CAT}-XXX: Cannot delete with {relationship}**

**Description**: Cannot delete {entity} that has related {related entities}
**Trigger**: Delete
**Condition**: No active related {entities} exist
**Action**: Reject with "Cannot delete {entity} with existing {related}"
**Exception**: Allow if all related are cancelled/completed
```

### Examples

| ID | Rule | Protected Entity | Blocking Relationship |
|----|------|------------------|----------------------|
| BR-PAT-003 | Cannot delete patient with future appointments | Patient | Appointments (future) |
| BR-DOC-002 | Cannot delete doctor with future appointments | Doctor | Appointments (future) |

---

## State Transition Rules

### Pattern

```markdown
**BR-{CAT}-XXX: {State} transition allowed**

**Description**: {Entity} can only transition to {target state} from {allowed states}
**Trigger**: Update (status change)
**Condition**: Current status in [{allowed states}]
**Action**: Update status to {target state}
**Exception**: Admin can force transition
```

### State Machine Example

```
Appointment States:
┌─────────────┐
│  Scheduled  │─────────────────────────┐
└──────┬──────┘                         │
       │ BR-APT-010                     │ BR-APT-013
       ▼                                ▼
┌─────────────┐                   ┌───────────┐
│  Confirmed  │───────────────────│ Cancelled │
└──────┬──────┘  BR-APT-012       └───────────┘
       │ BR-APT-011
       ▼
┌─────────────┐
│  Completed  │
└─────────────┘
```

### Examples

| ID | From States | To State | Notes |
|----|-------------|----------|-------|
| BR-APT-010 | Scheduled | Confirmed | Patient/staff confirms |
| BR-APT-011 | Confirmed | Completed | Doctor completes visit |
| BR-APT-012 | Confirmed | Cancelled | Patient/staff cancels |
| BR-APT-013 | Scheduled | Cancelled | Early cancellation |

---

## Date/Time Rules

### Pattern

```markdown
**BR-{CAT}-XXX: {Field} must be {constraint}**

**Description**: {Entity} {field} must satisfy temporal constraint
**Trigger**: Create, Update
**Condition**: {Field} {operator} {reference point}
**Action**: Reject with "{Field} must be {constraint description}"
**Exception**: None
```

### Examples

| ID | Rule | Field | Constraint |
|----|------|-------|------------|
| BR-PAT-002 | Date of birth must be in past | DateOfBirth | < Today |
| BR-APT-003 | Appointment must be in future | AppointmentDate | > Now |
| BR-SCH-001 | End time must be after start | EndTime | > StartTime |

---

## Range/Limit Rules

### Pattern

```markdown
**BR-{CAT}-XXX: {Field} must be within range**

**Description**: {Entity} {field} must be between {min} and {max}
**Trigger**: Create, Update
**Condition**: {min} <= {field} <= {max}
**Action**: Reject with "{Field} must be between {min} and {max}"
**Exception**: None
```

### Examples

| ID | Rule | Field | Min | Max |
|----|------|-------|-----|-----|
| BR-APT-005 | Duration 15-120 minutes | Duration | 15 min | 120 min |
| BR-INV-001 | Quantity 1-999 | Quantity | 1 | 999 |

---

## No-Overlap Rules

### Pattern

```markdown
**BR-{CAT}-XXX: No overlapping {entities}**

**Description**: {Entity} time ranges cannot overlap for same {grouping}
**Trigger**: Create, Update
**Condition**: No other {entity} exists where:
  - Same {grouping key}
  - Time ranges overlap (start1 < end2 AND start2 < end1)
**Action**: Reject with "Time slot conflicts with existing {entity}"
**Exception**: Cancelled records excluded
```

### Examples

| ID | Rule | Entity | Grouping Key |
|----|------|--------|--------------|
| BR-APT-001 | No overlapping appointments | Appointment | DoctorId + Date |
| BR-SCH-002 | No overlapping schedules | DoctorSchedule | DoctorId + DayOfWeek |

---

## Cross-Entity Rules

### Pattern

```markdown
**BR-{CAT}-XXX: {Entity} must satisfy {related entity} constraint**

**Description**: {Entity} operation requires condition on {related entity}
**Trigger**: Create, Update
**Condition**: {Related entity} satisfies {condition}
**Action**: Reject with "{Constraint description}"
**Exception**: {Exception if any}
```

### Examples

| ID | Rule | Primary Entity | Related Entity | Constraint |
|----|------|----------------|----------------|------------|
| BR-APT-002 | Within doctor schedule | Appointment | DoctorSchedule | Time within working hours |
| BR-APT-006 | Patient must be active | Appointment | Patient | IsActive = true |

---

## Rule Documentation Template

```markdown
**BR-{CAT}-{NNN}: {Rule Name}**

**Description**: [What the rule enforces - one sentence]

**Trigger**: [Create | Update | Delete | {Custom action}]

**Condition**: [Logic expression that must be true]

**Action**: [What happens when rule is violated]
- Error code: {Project}:{NNNNNN}
- Message: "{User-friendly message}"

**Exception**: [When this rule can be bypassed]

**Related**:
- BR-XXX-YYY: [Related rule]
- {Entity}: [Related entity]

**Implementation**:
- FluentValidation: `{ValidatorClass}`
- Domain Service: `{DomainServiceMethod}`
```
