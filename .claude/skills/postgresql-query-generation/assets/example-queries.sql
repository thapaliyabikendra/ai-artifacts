-- PostgreSQL Query Generation Examples
-- Generated for ACMS project
-- This file demonstrates common query patterns

-- ========================================
-- Example 1: Get Workflow Instances with Full Context
-- ========================================
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
LIMIT @maxResultCount OFFSET @skipCount;

-- ========================================
-- Example 2: Get Operations with User Account Types
-- ========================================
SELECT DISTINCT
  o."Id",
  o."SystemName",
  o."DisplayName",
  uat."Name" as "UserAccountType",
  ovat."ExecutionOrder"
FROM "Operations" o
JOIN "OperationUserAccountTypes" ovat ON ovat."OperationId" = o."Id"
  AND ovat."TenantId" = o."TenantId"
JOIN "UserAccountTypes" uat ON uat."Id" = ovat."UserAccountTypeId"
  AND uat."TenantId" = ovat."TenantId"
WHERE o."TenantId" = @tenantId
  AND o."IsDeleted" = false
  AND o."IsActive" = true
  AND uat."Id" = @userAccountTypeId
ORDER BY ovat."ExecutionOrder";

-- ========================================
-- Example 3: JSONB Query - Extract Form Field Names
-- ========================================
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

-- ========================================
-- Example 4: Recursive Workflow Configuration Tree
-- ========================================
WITH RECURSIVE workflow_tree AS (
  SELECT
    wc."Id",
    wc."ParentId",
    wc."Code",
    wc."ExecutionOrder",
    1 as "Level"
  FROM "OperationWorkflowConfigurations" wc
  WHERE wc."ParentId" IS NULL
    AND wc."TenantId" = @tenantId
    AND wc."IsDeleted" = false

  UNION ALL

  SELECT
    child."Id",
    child."ParentId",
    child."Code",
    child."ExecutionOrder",
    tree."Level" + 1
  FROM "OperationWorkflowConfigurations" child
  INNER JOIN workflow_tree tree ON child."ParentId" = tree."Id"
  WHERE child."TenantId" = @tenantId
    AND child."IsDeleted" = false
)
SELECT * FROM workflow_tree
ORDER BY "Level", "ExecutionOrder";

-- ========================================
-- Example 5: Count Workflow Instances by Stage
-- ========================================
SELECT
  ws."DisplayName" as "Stage",
  ws."SystemName" as "StageCode",
  COUNT(*) as "InstanceCount"
FROM "OperationWorkflowInstances" owfi
JOIN "WorkflowStages" ws ON ws."Id" = owfi."WorkflowStageId"
  AND ws."TenantId" = owfi."TenantId"
WHERE owfi."TenantId" = @tenantId
  AND owfi."IsDeleted" = false
  AND owfi."WorkflowStageDate" >= @startDate
  AND owfi."WorkflowStageDate" < @endDate
GROUP BY ws."DisplayName", ws."SystemName", ws."ExecutionOrder"
ORDER BY ws."ExecutionOrder";

-- ========================================
-- Example 6: Get Active Webhooks for Event
-- ========================================
SELECT
  ws."Id",
  ws."ConsumerId",
  ac."SystemName" as "ApiClient",
  we."EventName",
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
  AND ws."IsActive" = true;

-- ========================================
-- Example 7: Find Applications with Business Rules
-- ========================================
SELECT
  app."Id",
  app."SystemName",
  app."DisplayName",
  array_agg(DISTINCT br."SystemName") as "BusinessRules"
FROM "Applications" app
JOIN "ApplicationTasks" at ON at."ApplicationId" = app."Id"
  AND at."TenantId" = app."TenantId"
JOIN "ApplicationTaskRules" atr ON atr."ApplicationTaskId" = at."Id"
JOIN "BusinessRules" br ON br."Id" = atr."BusinessRuleId"
WHERE app."TenantId" = @tenantId
  AND app."IsDeleted" = false
  AND br."SystemName" IN ('Rule1', 'Rule2')
GROUP BY app."Id", app."SystemName", app."DisplayName"
HAVING COUNT(DISTINCT br."Id") = 2;

-- ========================================
-- Example 8: Configuration Fallback Pattern
-- ========================================
SELECT
  COALESCE(ttenant."Value", ssystem."Value") as "EffectiveValue"
FROM (
  SELECT "Value"
  FROM "Configurations"
  WHERE "TenantId" = @tenantId
    AND "Key" = @configKey
    AND "IsDeleted" = false
    AND "IsActive" = true
) ttenant
FULL OUTER JOIN (
  SELECT "Value"
  FROM "Configurations"
  WHERE "TenantId" IS NULL
    AND "Key" = @configKey
    AND "IsDeleted" = false
    AND "IsActive" = true
) ssystem ON true;

-- ========================================
-- Notes
-- ========================================
-- - All queries include multi-tenancy filters (TenantId)
-- - Soft delete filter (IsDeleted = false) is standard
-- - Replace @parameters with actual values
-- - Add LIMIT/OFFSET for pagination on large result sets
-- - Consider adding indexes for frequently queried columns
