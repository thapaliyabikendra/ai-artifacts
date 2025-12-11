# Feature: {{Feature Name}}

**Created**: {{Date}}
**Author**: product-architect
**Status**: Draft | Review | Approved

---

## 1. Feature Overview

### 1.1 Summary
{{Brief description of the feature and its purpose}}

### 1.2 Business Value
{{Why this feature is needed and what business problem it solves}}

### 1.3 Success Metrics
- {{Metric 1}}
- {{Metric 2}}

---

## 2. User Stories

### US-001: {{Story Title}}

**As a** {{role}}
**I want to** {{capability}}
**So that** {{benefit}}

**Acceptance Criteria:**
- [ ] Given {{context}}, when {{action}}, then {{expected result}}
- [ ] Given {{context}}, when {{action}}, then {{expected result}}

**Priority**: Must Have | Should Have | Could Have
**Effort**: S | M | L | XL

---

### US-002: {{Story Title}}

**As a** {{role}}
**I want to** {{capability}}
**So that** {{benefit}}

**Acceptance Criteria:**
- [ ] Given {{context}}, when {{action}}, then {{expected result}}

**Priority**: Must Have | Should Have | Could Have
**Effort**: S | M | L | XL

---

## 3. Data Model

### 3.1 Entity: {{Entity Name}}

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| Id | Guid | PK, Required | Unique identifier |
| {{Field}} | {{Type}} | {{Constraints}} | {{Description}} |

### 3.2 Relationships

| From | To | Type | Description |
|------|-----|------|-------------|
| {{Entity}} | {{Entity}} | 1:N / N:1 / N:N | {{Description}} |

---

## 4. Business Rules

| ID | Rule | Validation |
|----|------|------------|
| BR-001 | {{Rule description}} | {{How to validate}} |
| BR-002 | {{Rule description}} | {{How to validate}} |

---

## 5. Permission Requirements

| Permission | Description | Roles |
|------------|-------------|-------|
| {{Feature}}.Default | View {{feature}} | All authenticated |
| {{Feature}}.Create | Create new {{feature}} | Admin, {{Role}} |
| {{Feature}}.Edit | Edit existing {{feature}} | Admin, {{Role}} |
| {{Feature}}.Delete | Delete {{feature}} | Admin |

---

## 6. UI/UX Notes

### 6.1 Screens/Pages
- {{Screen 1}}: {{Description}}
- {{Screen 2}}: {{Description}}

### 6.2 User Flow
1. User navigates to {{page}}
2. User clicks {{action}}
3. System displays {{result}}

---

## 7. Non-Functional Requirements

- **Performance**: {{Requirements}}
- **Security**: {{Requirements}}
- **Accessibility**: {{Requirements}}

---

## 8. Open Questions

- [ ] {{Question 1}}
- [ ] {{Question 2}}

---

## 9. Out of Scope

- {{Explicit exclusion 1}}
- {{Explicit exclusion 2}}

---

## 10. Dependencies

| Dependency | Type | Status |
|------------|------|--------|
| {{Dependency}} | Feature / Service / External | Pending / Complete |
