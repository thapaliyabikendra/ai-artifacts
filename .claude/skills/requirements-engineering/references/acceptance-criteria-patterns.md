# Acceptance Criteria Patterns

Reusable patterns for writing testable acceptance criteria using Given-When-Then format.

## CRUD Patterns

### Create - Happy Path

```gherkin
Given I am logged in as {Role}
And I have the {Resource}.Create permission
When I submit a valid create request with {required fields}
Then the {resource} is created successfully
And I receive a 201 response with the created {resource}
And the {resource} has a unique ID assigned
```

### Create - Validation Error

```gherkin
Given I am logged in as {Role}
When I submit a create request with {invalid field: reason}
Then I receive a 400 response
And the error message indicates "{validation message}"
And no {resource} is created
```

### Create - Duplicate Prevention

```gherkin
Given a {resource} with {unique field} "{value}" already exists
When I submit a create request with the same {unique field}
Then I receive a 400 response
And the error message indicates "{field} already exists"
```

### Read - Single Item

```gherkin
Given a {resource} with ID "{id}" exists
And I have the {Resource} permission
When I request the {resource} by ID
Then I receive a 200 response
And the response contains the {resource} details
```

### Read - Not Found

```gherkin
Given no {resource} with ID "{id}" exists
When I request the {resource} by ID
Then I receive a 404 response
And the error message indicates "{Resource} not found"
```

### Read - List with Pagination

```gherkin
Given {N} {resources} exist in the system
When I request the {resource} list with page size {size}
Then I receive a 200 response
And the response contains {size} items
And the response includes total count of {N}
And the response includes pagination metadata
```

### Read - List with Filter

```gherkin
Given {resources} exist with various {filter field} values
When I request the {resource} list filtered by {filter field} = "{value}"
Then I receive only {resources} matching the filter
And non-matching {resources} are excluded
```

### Update - Happy Path

```gherkin
Given a {resource} with ID "{id}" exists
And I have the {Resource}.Edit permission
When I submit a valid update request with {changed fields}
Then the {resource} is updated successfully
And I receive a 200 response with the updated {resource}
And the changes are persisted
```

### Update - Concurrent Modification

```gherkin
Given a {resource} was modified by another user
When I submit an update based on stale data
Then I receive a 409 response
And the error message indicates "Concurrent modification detected"
```

### Delete - Happy Path

```gherkin
Given a {resource} with ID "{id}" exists
And I have the {Resource}.Delete permission
When I submit a delete request
Then the {resource} is soft-deleted
And I receive a 204 response
And the {resource} no longer appears in list queries
```

### Delete - With Dependencies

```gherkin
Given a {resource} has related {dependent resources}
When I attempt to delete the {resource}
Then I receive a 400 response
And the error message indicates "Cannot delete {resource} with existing {dependencies}"
```

---

## Authorization Patterns

### Missing Permission

```gherkin
Given I am logged in as {Role}
And I do NOT have the {Resource}.{Action} permission
When I attempt to {action} a {resource}
Then I receive a 403 Forbidden response
And the operation is not performed
```

### Role-Based Access

```gherkin
Given I am logged in as {Role}
When I access the {resource} list
Then I see only {resources} I am authorized to view
And other {resources} are not visible
```

### Owner-Only Access

```gherkin
Given I am the owner of {resource} "{id}"
When I attempt to {action} the {resource}
Then the operation succeeds

Given I am NOT the owner of {resource} "{id}"
When I attempt to {action} the {resource}
Then I receive a 403 Forbidden response
```

---

## Validation Patterns

### Required Field

```gherkin
Given I am creating/updating a {resource}
When I omit the required field "{field}"
Then I receive a 400 response
And the error indicates "{field} is required"
```

### Max Length

```gherkin
Given I am creating/updating a {resource}
When I provide "{field}" with {N+1} characters (max is {N})
Then I receive a 400 response
And the error indicates "{field} cannot exceed {N} characters"
```

### Format Validation

```gherkin
Given I am creating/updating a {resource}
When I provide "{field}" with invalid format "{invalid value}"
Then I receive a 400 response
And the error indicates "Invalid {field} format"
```

### Range Validation

```gherkin
Given I am creating/updating a {resource}
When I provide "{field}" with value {out of range value}
Then I receive a 400 response
And the error indicates "{field} must be between {min} and {max}"
```

---

## Business Rule Patterns

### State Transition

```gherkin
Given a {resource} in "{current state}" status
When I attempt to transition to "{target state}"
Then the transition {succeeds/fails}
And the status is updated to "{expected state}"
```

### No Overlap

```gherkin
Given an existing {resource} from {start} to {end}
When I attempt to create a {resource} that overlaps this time range
Then I receive a 400 response
And the error indicates "Time slot conflicts with existing {resource}"
```

### Temporal Constraint

```gherkin
Given today is {date}
When I attempt to create a {resource} with {date field} in the {past/future}
Then the operation {succeeds/fails}
And the error indicates "{field} must be in the {future/past}"
```

---

## Edge Case Patterns

### Empty List

```gherkin
Given no {resources} exist in the system
When I request the {resource} list
Then I receive a 200 response
And the items array is empty
And the total count is 0
```

### Boundary Values

```gherkin
Given I am creating a {resource}
When I provide "{field}" at the maximum allowed value
Then the {resource} is created successfully

When I provide "{field}" at minimum allowed value
Then the {resource} is created successfully
```

### Special Characters

```gherkin
Given I am creating a {resource}
When I provide "{field}" with special characters "{special chars}"
Then the {resource} is created successfully
And the special characters are preserved
```

---

## Async/Background Patterns

### Background Job Triggered

```gherkin
Given a {resource} is created/updated
When the operation completes
Then a background job is queued for {job purpose}
And the job executes within {timeout}
```

### Email Notification

```gherkin
Given a {trigger event} occurs
When the system processes the event
Then an email notification is sent to {recipient}
And the email contains {expected content}
```

---

## Template Usage

When writing acceptance criteria:

1. **Be specific** - Use concrete values, not vague descriptions
2. **Be testable** - Each criterion should be verifiable
3. **Cover paths** - Happy path, error cases, edge cases
4. **Consider auth** - Include permission checks
5. **Think state** - Consider state transitions
6. **Check audit** - Verify audit trail when applicable
