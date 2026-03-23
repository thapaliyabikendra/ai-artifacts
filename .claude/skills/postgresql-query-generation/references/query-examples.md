# Query Examples

20+ real-world PostgreSQL query examples for the ACMS project and similar ABP Framework applications.

These examples demonstrate patterns discovered by the skill. **Replace entity/column names** to match your domain.

---

## Multi-Tenant Queries

### 1. Get Active Records for Tenant

**Natural language:** "Get all active applications for tenant"

```sql
SELECT
  "Id",
  "SystemName",
  "DisplayName",
  "CreationTime"
FROM "Applications"
WHERE "TenantId" = @tenantId
  AND "IsDeleted" = false
  AND "IsActive" = true
ORDER BY "CreationTime" DESC
LIMIT @maxCount OFFSET @skip;
```

---

### 2. Get System-Wide Records (No Tenant)

**Natural language:** "Get system-wide configuration"

```sql
SELECT
  "Id",
  "Key",
  "Value"
FROM "Configurations"
WHERE "TenantId" IS NULL
  AND "IsDeleted" = false
  AND "IsActive" = true;
```

---

### 3. Tenant + System Records (Fallback Pattern)

**Natural language:** "Get configuration with tenant fallback"

```sql
SELECT
  COALESCE(tt."Value", ss."Value") as "EffectiveValue"
FROM (
  SELECT "Value"
  FROM "Configurations"
  WHERE "TenantId" = @tenantId
    AND "Key" = @configKey
    AND "IsDeleted" = false
    AND "IsActive" = true
) tt
FULL OUTER JOIN (
  SELECT "Value"
  FROM "Configurations"
  WHERE "TenantId" IS NULL
    AND "Key" = @configKey
    AND "IsDeleted" = false
    AND "IsActive" = true
) ss ON true;
```

---

## Workflow Queries (ACMS)

### 4. Get Workflow Instances with Full Context

**Natural language:** "Get application workflow instances with stage, operation, and substage"

```sql
SELECT
  awi."Id",
  awi."TaskNumber",
  awi."WorkflowStageDate",
  app."Name" as "ApplicationName",
  task."Name" as "TaskName",
  stage."DisplayName" as "StageName",
  substage."DisplayName" as "SubStageName",
  owf."RequestNumber" as "OperationRequestNumber",
  u."UserName" as "RequestedByUser"
FROM "ApplicationWorkflowInstances" awi
JOIN "Applications" app ON app."Id" = awi."ApplicationWorkflowConfigurationId"
  AND app."TenantId" = awi."TenantId"
JOIN "OperationWorkflowInstances" owf ON owf."Id" = awi."OperationWorkflowInstanceId"
  AND owf."TenantId" = awi."TenantId"
JOIN "WorkflowStages" stage ON stage."Id" = awi."StageId"
  AND stage."TenantId" = awi."TenantId"
LEFT JOIN "WorkflowSubStages" substage ON substage."Id" = awi."SubStageId"
  AND substage."TenantId" = awi."TenantId"
LEFT JOIN "AbpIdentity"."Users" u ON u."Id" = awi."RequestedBy"::uuid
WHERE awi."TenantId" = @tenantId
  AND awi."IsDeleted" = false
ORDER BY awi."WorkflowStageDate" DESC
LIMIT @maxCount OFFSET @skip;
```

---

### 5. Get Pending Tasks by User Role

**Natural language:** "Get pending approval tasks for user's account types"

```sql
SELECT DISTINCT
  at."Id",
  at."Name" as "TaskName",
  at."Code" as "TaskCode",
  ws."DisplayName" as "CurrentStage",
  owfi."RequestNumber",
  app."DisplayName" as "ApplicationName"
FROM "ApplicationTasks" at
JOIN "OperationWorkflowConfigurations" owc ON owc."ApplicationTaskId" = at."Id"
  AND owc."TenantId" = at."TenantId"
JOIN "OperationWorkflowInstances" owfi ON owfi."WorkflowStageId" = owc."WorkflowStageId"
  AND owfi."TenantId" = owc."TenantId"
  AND owfi."IsDeleted" = false
JOIN "WorkflowStages" ws ON ws."Id" = owfi."WorkflowStageId"
  AND ws."IsActive" = true
JOIN "OperationUserAccountTypes" ouat ON ouat."WorkflowStageId" = ws."Id"
  AND ouat."UserAccountTypeId" = @userAccountTypeId
JOIN "Applications" app ON app."Id" = at."ApplicationId"
  AND app."IsActive" = true
WHERE at."TenantId" = @tenantId
  AND at."IsActive" = true
ORDER BY owfi."WorkflowStageDate" DESC;
```

---

### 6. Workflow Timeline for Request Number

**Natural language:** "Show complete workflow timeline for request #12345"

```sql
SELECT
  owfi."RequestNumber",
  owfi."WorkflowStageDate",
  ws."DisplayName" as "Stage",
  wss."DisplayName" as "SubStage",
  u."UserName" as "ProcessedBy",
  awil."LogMessage" as "Comment"
FROM "OperationWorkflowInstances" owfi
JOIN "WorkflowStages" ws ON ws."Id" = owfi."WorkflowStageId"
  AND ws."TenantId" = owfi."TenantId"
LEFT JOIN "WorkflowSubStages" wss ON wss."Id" = owfi."SubStageId"
  AND wss."TenantId" = owfi."TenantId"
LEFT JOIN "AbpIdentity"."Users" u ON u."Id" = owfi."WorkflowStageBy"::uuid
  AND u."TenantId" = owfi."TenantId"
LEFT JOIN "ApplicationWorkflowInstanceLogs" awil ON awil."ApplicationWorkflowInstanceId" = owfi."Id"
  AND awil."StageId" = owfi."WorkflowStageId"
WHERE owfi."RequestNumber" = @requestNumber
  AND owfi."TenantId" = @tenantId
ORDER BY owfi."WorkflowStageDate" ASC;
```

---

### 7. Find Applications with Specific Business Rules

**Natural language:** "Find applications that have all of these business rules: Rule1, Rule2, Rule3"

```sql
SELECT
  app."Id",
  app."SystemName",
  app."DisplayName",
  array_agg(DISTINCT br."SystemName") as "MatchedRules"
FROM "Applications" app
JOIN "ApplicationTasks" at ON at."ApplicationId" = app."Id"
  AND at."TenantId" = app."TenantId"
  AND at."IsActive" = true
JOIN "OperationWorkflowConfigurations" owc ON owc."ApplicationTaskId" = at."Id"
  AND owc."IsActive" = true
JOIN "ApplicationTaskRules" atr ON atr."ApplicationTaskId" = at."Id"
  AND atr."IsActive" = true
JOIN "BusinessRules" br ON br."Id" = atr."BusinessRuleId"
  AND br."IsActive" = true
WHERE app."TenantId" = @tenantId
  AND app."IsDeleted" = false
  AND br."SystemName" IN ('Rule1', 'Rule2', 'Rule3')
GROUP BY app."Id", app."SystemName", app."DisplayName"
HAVING COUNT(DISTINCT br."Id") = 3;  -- All 3 rules matched
```

---

## JSONB Queries

### 8. Search JSONB for Specific Field

**Natural language:** "Find forms with field 'department' in schema"

```sql
SELECT
  df."Id",
  df."Name",
  df."JsonSchema"
FROM "DynamicForms" df
WHERE df."TenantId" = @tenantId
  AND df."IsDeleted" = false
  AND df."JsonSchema" ? 'properties'
  AND df."JsonSchema" @> '{"type": "object"}';
```

---

### 9. Extract Value from JSONB

**Natural language:** "Get all form field names from schema"

```sql
SELECT
  df."Id",
  df."Name" as "FormName",
  jsonb_array_elements(
    jsonb_path_query_array(df."JsonSchema", '$.properties.*')
  ) ->> 'name' as "FieldName"
FROM "DynamicForms" df
WHERE df."TenantId" = @tenantId
  AND df."IsDeleted" = false
  AND df."JsonSchema" ? 'properties';
```

---

### 10. Filter by JSONB Array Content

**Natural language:** "Find jobs with 'urgent' in tags"

```sql
SELECT
  oj."Id",
  oj."OperationId",
  oj."OperationParameters"
FROM "OperationJobs" oj
WHERE oj."TenantId" = @tenantId
  AND oj."IsDeleted" = false
  AND oj."OperationParameters" @> '{"tags": ["urgent"]}';
```

---

### 11. Check if JSONB Contains Key-Value Pair

**Natural language:** "Find configurations with environment=production"

```sql
SELECT
  c."Id",
  c."Key",
  c."Value"
FROM "Configurations" c
WHERE c."TenantId" = @tenantId
  AND c."IsDeleted" = false
  AND c."Value" @> '{"environment": "production"}';
```

---

## Recursive Queries

### 12. Get Complete Category Tree

**Natural language:** "Show all categories in hierarchy"

```sql
WITH RECURSIVE category_tree AS (
  -- Anchor: root categories (no parent)
  SELECT
    c."Id",
    c."ParentId",
    c."Name",
    c."Code",
    c."ExecutionOrder",
    1 as "Level"
  FROM "Categories" c
  WHERE c."ParentId" IS NULL
    AND c."TenantId" = @tenantId
    AND c."IsDeleted" = false

  UNION ALL

  -- Recursive: children
  SELECT
    child."Id",
    child."ParentId",
    child."Name",
    child."Code",
    child."ExecutionOrder",
    tree."Level" + 1
  FROM "Categories" child
  INNER JOIN category_tree tree ON child."ParentId" = tree."Id"
  WHERE child."TenantId" = @tenantId
    AND child."IsDeleted" = false
)
SELECT * FROM category_tree
ORDER BY "Level", "ExecutionOrder";
```

---

### 13. Get Leaf Nodes Only

**Natural language:** "Find all leaf categories (no children)"

```sql
WITH RECURSIVE category_tree AS (
  SELECT c."Id", c."ParentId"
  FROM "Categories" c
  WHERE c."TenantId" = @tenantId
    AND c."IsDeleted" = false

  UNION ALL

  SELECT child."Id", child."ParentId"
  FROM "Categories" child
  INNER JOIN category_tree tree ON child."ParentId" = tree."Id"
)
SELECT c.*
FROM "Categories" c
LEFT JOIN category_tree children ON children."ParentId" = c."Id"
WHERE c."TenantId" = @tenantId
  AND c."IsDeleted" = false
  AND children."Id" IS NULL;  -- No children
```

---

## Permission & Security

### 14. Get User's Accessible Operations

**Natural language:** "Show all operations user can access"

```sql
SELECT DISTINCT
  o."Id",
  o."SystemName",
  o."DisplayName",
  uat."Name" as "UserAccountType"
FROM "Operations" o
JOIN "OperationUserAccountTypes" ovat ON ovat."OperationId" = o."Id"
  AND ovat."TenantId" = o."TenantId"
JOIN "UserAccountTypes" uat ON uat."Id" = ovat."UserAccountTypeId"
  AND uat."TenantId" = ovat."TenantId"
JOIN "AbpIdentity"."Users" u ON u."UserName" = @userName
  AND u."TenantId" = @tenantId
JOIN "AbpIdentity"."UserRoles" ur ON ur."UserId" = u."Id"
  AND ur."TenantId" = u."TenantId"
JOIN "AbpIdentity"."Roles" r ON r."Id" = ur."RoleId"
  AND r."TenantId" = ur."TenantId"
WHERE o."TenantId" = @tenantId
  AND o."IsDeleted" = false
  AND uat."Name" IN (
    SELECT "Name"
    FROM "Roles"
    WHERE "Id" IN (
      SELECT "RoleId"
      FROM "UserRoles"
      WHERE "UserId" = u."Id"
    )
  );
```

---

### 15. Check User Has Permission for Operation

**Natural language:** "Does user have permission to operate on X?"

```sql
SELECT EXISTS (
  SELECT 1
  FROM "Operations" o
  JOIN "OperationUserAccountTypes" ovat ON ovat."OperationId" = o."Id"
  JOIN "UserAccountTypes" uat ON uat."Id" = ovat."UserAccountTypeId"
  JOIN "AbpIdentity"."UserRoles" ur ON ur."UserId" = @userId
  JOIN "AbpIdentity"."Roles" r ON r."Id" = ur."RoleId" AND r."Name" = uat."Name"
  WHERE o."Id" = @operationId
    AND o."IsDeleted" = false
    AND r."IsActive" = true
) as "HasPermission";
```

---

## Window Functions

### 16. Get Latest Record per Group

**Natural language:** "Get most recent workflow instance for each operation"

```sql
SELECT DISTINCT ON ("OperationId")
  "OperationId",
  "RequestNumber",
  "WorkflowStageId",
  "WorkflowStageDate",
  FIRST_VALUE("Status") OVER (
    PARTITION BY "OperationId"
    ORDER BY "WorkflowStageDate" DESC
  ) as "CurrentStatus"
FROM "OperationWorkflowInstances"
WHERE "TenantId" = @tenantId
  AND "IsDeleted" = false;
```

---

### 17. Rank Records by Date

**Natural language:** "Show top 5 most recent applications per task"

```sql
SELECT
  app."TaskId",
  app."SystemName",
  app."CreationTime",
  ROW_NUMBER() OVER (
    PARTITION BY app."TaskId"
    ORDER BY app."CreationTime" DESC
  ) as "RankInTask"
FROM "Applications" app
WHERE app."TenantId" = @tenantId
  AND app."IsDeleted" = false
QUALIFY ROW_NUMBER() <= 5;
-- Note: Use subquery for PostgreSQL < 15 or:
-- WHERE rank <= 5 in outer query
```

---

## Date/Time Queries

### 18. Applications by Month

**Natural language:** "Count of applications created each month"

```sql
SELECT
  date_trunc('month', "CreationTime") as "Month",
  count(*) as "ApplicationCount"
FROM "Applications"
WHERE "TenantId" = @tenantId
  AND "IsDeleted" = false
  AND "CreationTime" >= '2024-01-01'
GROUP BY date_trunc('month', "CreationTime")
ORDER BY "Month" DESC;
```

---

### 19. Applications Created Today

**Natural language:** "Show today's applications"

```sql
SELECT
  "Id",
  "SystemName",
  "CreationTime"
FROM "Applications"
WHERE "TenantId" = @tenantId
  AND "IsDeleted" = false
  AND DATE("CreationTime") = CURRENT_DATE
ORDER BY "CreationTime" DESC;
```

---

## Dynamic Forms

### 20. Extract Field Definitions from JSON Schema

**Natural language:** "Get all field names from form schema"

```sql
SELECT
  df."Id",
  df."Name" as "FormName",
  jsonb_path_query(
    df."JsonSchema",
    '$.properties.*'
  ) as "FieldSchema"
FROM "DynamicForms" df
WHERE df."TenantId" = @tenantId
  AND df."IsDeleted" = false
  AND df."JsonSchema" ? 'properties';
```

---

### 21. Find Forms with Conditional Logic

**Natural language:** "Find forms that have conditional rules"

```sql
SELECT
  df."Id",
  df."Name",
  df."JsonSchema"
FROM "DynamicForms" df
WHERE df."TenantId" = @tenantId
  AND df."IsDeleted" = false
  AND jsonb_path_exists(
    df."JsonSchema",
    '$.properties[*].conditional'
  );
```

---

## Webhook & Integration

### 22. Get Active Webhook Subscriptions

**Natural language:** "Show active webhooks for 'application.created' event"

```sql
SELECT
  ws."Id",
  ws."ConsumerId",
  ac."SystemName" as "ApiClient",
  ws."RetryCount",
  ws."MaxRetryCount"
FROM "WebhookSubscriptions" ws
JOIN "ApiClients" ac ON ac."Id" = ws."ApiClientId"
  AND ac."TenantId" = ws."TenantId"
JOIN "WebhookEvents" we ON we."Id" = ws."WebhookEventId"
  AND we."TenantId" = ws."TenantId"
WHERE we."EventName" = @eventName
  AND ws."TenantId" = @tenantId
  AND ws."IsDeleted" = false
  AND ws."IsActive" = true
  AND ws."RetryCount" < ws."MaxRetryCount";
```

---

### 23. Failed Webhooks Needing Retry

**Natural language:** "Get failed webhooks from last hour"

```sql
SELECT
  wl."Id",
  wl."WebhookSubscriptionId",
  wl."AttemptedAt",
  wl."ErrorMessage",
  ac."SystemName" as "ClientName",
  ws."EventId"
FROM "WebhookLogs" wl
JOIN "WebhookSubscriptions" ws ON ws."Id" = wl."WebhookSubscriptionId"
JOIN "ApiClients" ac ON ac."Id" = ws."ApiClientId"
WHERE wl."Succeeded" = false
  AND wl."RetryCount" < wl."MaxRetryCount"
  AND wl."AttemptedAt" > NOW() - INTERVAL '1 hour'
ORDER BY wl."AttemptedAt" ASC;
```

---

## Bulk Operations

### 24. Update Multiple Records by IDs

**Natural language:** "Mark multiple records as inactive"

```sql
UPDATE "DynamicTables"
SET
  "IsActive" = false,
  "LastModificationTime" = NOW()
WHERE "Id" IN (@id1, @id2, @id3)
  AND "TenantId" = @tenantId
  AND "IsDeleted" = false
RETURNING "Id", "SystemName";
```

---

### 25. Batch Insert with ExecuteMany

**Natural language:** "Insert multiple configuration records"

```sql
INSERT INTO "Configurations" ("Id", "TenantId", "Key", "Value", "IsActive")
VALUES
  (@id1, @tenantId, @key1, @value1, true),
  (@id2, @tenantId, @key2, @value2, true),
  (@id3, @tenantId, @key3, @value3, true)
ON CONFLICT ("TenantId", "Key")
WHERE "IsDeleted" = false
DO UPDATE SET
  "Value" = EXCLUDED."Value",
  "LastModificationTime" = NOW();
```

---

## Analytics & Reporting

### 26. Workflow Stage Distribution

**Natural language:** "Count of instances per stage"

```sql
SELECT
  ws."DisplayName" as "Stage",
  count(*) as "InstanceCount"
FROM "OperationWorkflowInstances" owfi
JOIN "WorkflowStages" ws ON ws."Id" = owfi."WorkflowStageId"
  AND ws."TenantId" = owfi."TenantId"
WHERE owfi."TenantId" = @tenantId
  AND owfi."IsDeleted" = false
  AND owfi."WorkflowStageDate" >= @startDate
  AND owfi."WorkflowStageDate" < @endDate
GROUP BY ws."DisplayName", ws."ExecutionOrder"
ORDER BY ws."ExecutionOrder";
```

---

### 27. Average Time per Stage

**Natural language:** "Average time spent in each workflow stage"

```sql
WITH stage_transitions AS (
  SELECT
    owfi."OperationId",
    owfi."WorkflowStageId",
    owfi."WorkflowStageDate",
    LEAD(owfi."WorkflowStageDate") OVER (
      PARTITION BY owfi."OperationId"
      ORDER BY owfi."WorkflowStageDate"
    ) as "NextStageDate"
  FROM "OperationWorkflowInstances" owfi
  WHERE owfi."TenantId" = @tenantId
    AND owfi."IsDeleted" = false
)
SELECT
  ws."DisplayName" as "Stage",
  count(*) as "Transitions",
  AVG("NextStageDate" - "WorkflowStageDate") as "AvgDuration"
FROM stage_transitions st
JOIN "WorkflowStages" ws ON ws."Id" = st."WorkflowStageId"
WHERE "NextStageDate" IS NOT NULL
GROUP BY ws."DisplayName", ws."ExecutionOrder"
ORDER BY ws."ExecutionOrder";
```

---

### 28. Busiest Workflow Stages

**Natural language:** "Top 10 most used workflow stages"

```sql
SELECT
  ws."Id",
  ws."DisplayName",
  count(*) as "InstanceCount"
FROM "WorkflowStages" ws
JOIN "OperationWorkflowInstances" owfi ON owfi."WorkflowStageId" = ws."Id"
  AND owfi."TenantId" = ws."TenantId"
WHERE owfi."TenantId" = @tenantId
  AND owfi."IsDeleted" = false
  AND owfi."WorkflowStageDate" >= NOW() - INTERVAL '30 days'
GROUP BY ws."Id", ws."DisplayName"
ORDER BY count(*) DESC
LIMIT 10;
```

---

## Dynamic Tables & Forms

### 29. Get Dynamic Table with Column Definitions

**Natural language:** "Get dynamic table and its column definitions"

```sql
SELECT
  dt."Id",
  dt."TableName",
  dt."TableSchema",
  jsonb_array_elements(dt."TableSchema"->'columns') as "ColumnDefinition"
FROM "DynamicTables" dt
WHERE dt."TenantId" = @tenantId
  AND dt."IsDeleted" = false
  AND dt."IsActive" = true;
```

---

### 30. Dynamic Form with Validation Rules

**Natural language:** "Get form with its validation rules"

```sql
SELECT
  df."Id",
  df."Name",
  df."JsonSchema"->'properties' as "Fields",
  jsonb_agg(
    jsonb_build_object(
      'ruleName', br."SystemName",
      'ruleType', br."RuleType"
    )
  ) as "ValidationRules"
FROM "DynamicForms" df
LEFT JOIN "DynamicFormRules" dfr ON dfr."DynamicFormId" = df."Id"
LEFT JOIN "BusinessRules" br ON br."Id" = dfr."BusinessRuleId"
WHERE df."TenantId" = @tenantId
  AND df."IsDeleted" = false
GROUP BY df."Id", df."Name", df."JsonSchema";
```

---

## Performance Optimization

### 31. Find Queries Missing Indexes

**Natural language:** "Show tables with high sequential scans"

```sql
SELECT
  schemaname,
  tablename,
  seq_scan,
  idx_scan,
  round(seq_scan::numeric / nullif(seq_scan + idx_scan, 0) * 100, 2) as "SeqScanPercent"
FROM pg_stat_user_tables
WHERE schemaname = 'public'
  AND seq_scan + idx_scan > 1000
ORDER BY seq_scan DESC;
```

---

## Parameter Reference

When using generated queries, these parameters are typical:

| Parameter | Type | Description |
|-----------|------|-------------|
| `@tenantId` | `UUID` | Current tenant identifier |
| `@userId` | `UUID` | Current user identifier |
| `@maxResultCount` | `INTEGER` | Page size (e.g., 20, 50, 100) |
| `@skipCount` | `INTEGER` | Offset for pagination |
| `@id` | `UUID` | Record ID |
| `@search` | `VARCHAR` | Search term |
| `@startDate` | `TIMESTAMPTZ` | Start date for date range |
| `@endDate` | `TIMESTAMPTZ` | End date for date range |
| `@status` | `VARCHAR` or `INTEGER` | Status value |
| `@userAccountTypeId` | `UUID` | User account type identifier |
| `@operationId` | `UUID` | Operation identifier |
| `@applicationId` | `UUID` | Application identifier |
| `@stageId` | `UUID` | Workflow stage identifier |
| `@requestNumber` | `VARCHAR` | Request reference number |

---

## Converting to Entity Framework

Generated SQL can be converted to EF Core queries:

```sql
-- SQL
SELECT a.*, b."Name" as "BranchName"
FROM "Applications" a
JOIN "Branches" b ON b."Id" = a."BranchId"
WHERE a."TenantId" = @tenantId;

-- EF Core Equivalent
var query = _dbContext.Applications
    .Where(a => a.TenantId == tenantId)
    .Select(a => new {
        Application = a,
        BranchName = a.Branch.Name
    });
```

---

## See Also

- **[Query Patterns](query-patterns.md)** - Pattern reference for manual query writing
- **[Entity Discovery](entity-discovery.md)** - Understanding schema discovery
- **[Type Mappings](type-mappings.md)** - PostgreSQL type reference
