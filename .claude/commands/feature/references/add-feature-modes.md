# Add Feature - Execution Modes

Detailed execution scripts for each mode of the `/add-feature` command.

## Execution: --minimal Mode

For simple CRUD features, skip documentation and use direct scaffolding.

Use Task tool with `subagent_type="abp-developer"` and `model="sonnet"`:

```
Implement CRUD feature for {feature-name}.

Requirements: {requirements-text}
Context: Read CLAUDE.md, docs/architecture/README.md
Skills: Apply abp-framework-patterns, efcore-patterns, fluentvalidation-patterns

Generate ALL files in a single pass:
1. Entity in Domain layer
2. DTOs in Application.Contracts
3. AppService interface + implementation
4. FluentValidation validator
5. EF Core configuration
6. Permissions

Build and verify: dotnet build api/*.slnx
```

**Output**: List created files. Done.

---

## Execution: --fast Mode

Skip business-analyst when requirements are detailed. Backend-architect parses requirements directly.

### Step 1: Design + Contracts

Use Task tool with `subagent_type="backend-architect"`, `model="haiku"`:

```
Create technical design AND generate contracts for {feature-name}.

Requirements (parse directly): {requirements-text}
Context: Read CLAUDE.md, docs/architecture/README.md, docs/domain/permissions.md
Skills: Apply technical-design-patterns, abp-contract-scaffolding

Output:
1. docs/features/{feature-name}/technical-design.md (max 150 lines)
2. docs/domain/entities/{entity}.md (entity definition)
3. Application.Contracts/{Feature}/I{Entity}AppService.cs
4. Application.Contracts/{Feature}/{Entity}Dto.cs
5. Application.Contracts/{Feature}/Create{Entity}Dto.cs
6. Application.Contracts/{Feature}/Update{Entity}Dto.cs
7. Application.Contracts/{Feature}/Get{Entity}sInput.cs
8. Application.Contracts/Permissions/{Entity}Permissions.cs
9. Update docs/domain/permissions.md
```

**Checkpoint**: Contracts exist.

### Step 2: Parallel Implementation + Testing

Launch BOTH agents simultaneously using multiple Task tool calls in ONE message:

**Agent A** - Task with `subagent_type="abp-developer"`, `model="sonnet"`:
```
Implement {feature-name} using generated contracts.

Input: Application.Contracts/{Feature}/ (interface + DTOs exist)
Skills: Apply abp-framework-patterns, efcore-patterns, fluentvalidation-patterns

Generate:
1. Domain/{Feature}/{Entity}.cs
2. Domain.Shared/{Feature}/{Entity}Consts.cs
3. Application/{Feature}/{Entity}AppService.cs
4. Application/{Feature}/{Entity}ApplicationMappers.cs
5. Application/{Feature}/*Validator.cs
6. EntityFrameworkCore/EntityTypeConfigurations/{Entity}Configuration.cs
7. Update DbContext, PermissionDefinitionProvider

DO NOT recreate contracts - they exist.
Build: dotnet build api/*.slnx
```

**Agent B** - Task with `subagent_type="qa-engineer"`, `model="sonnet"`:
```
Create tests for {feature-name} using generated contracts.

Input: Application.Contracts/{Feature}/ (interface + DTOs exist)
Skills: Apply xunit-testing-patterns

Output:
1. test/TestBase/{Feature}/{Entity}TestData.cs
2. test/TestBase/{Feature}/{Entity}TestDataSeedContributor.cs
3. test/Application.Tests/{Feature}/{Entity}AppService_Tests.cs

Write tests against INTERFACE - implementation is parallel.
```

**Checkpoint**: Both complete. Build succeeds.

---

## Execution: Default Mode (Progressive Handoff)

### Phase 1a: Entity Definition (Priority Output)

Use Task tool with `subagent_type="business-analyst"`, `model="haiku"`:

```
Analyze {feature-name} and produce PRIORITY outputs first.

Requirements: {requirements-text}
Context: Read docs/domain/*, docs/architecture/README.md

PRIORITY OUTPUT (produce these FIRST, max 60 lines total):
1. docs/domain/entities/{entity}.md - Entity definition with:
   - Properties table (Type, Required, Constraints)
   - API Access table (Permission names)
2. Update docs/domain/permissions.md - Add permission entries

After writing entity.md, IMMEDIATELY emit signal:
🟢 ENTITY_READY: docs/domain/entities/{entity}.md

Then continue with secondary outputs (don't block on these):

SECONDARY OUTPUT:
3. docs/features/{feature-name}/requirements.md - User stories (max 80 lines)
4. Update docs/domain/business-rules.md - Add BR-XXX rules

DO NOT generate:
- ANALYSIS.md (redundant summary)
- impact-analysis.md (use --impact flag if needed)

Skills: Apply requirements-engineering, domain-modeling
```

### Phase 1b: Contracts + QA-Data (Parallel on ENTITY_READY)

On `🟢 ENTITY_READY` signal, launch BOTH agents in parallel:

**Agent A** - Task with `subagent_type="backend-architect"`, `model="haiku"`:
```
Generate technical design AND contracts for {feature-name}.

Input: docs/domain/entities/{entity}.md (just created)
Context: docs/architecture/README.md, docs/domain/permissions.md
Skills: Apply technical-design-patterns, abp-contract-scaffolding

Output:
1. docs/features/{feature-name}/technical-design.md (max 150 lines)
2. Application.Contracts/{Feature}/I{Entity}AppService.cs
3. Application.Contracts/{Feature}/{Entity}Dto.cs
4. Application.Contracts/{Feature}/Create{Entity}Dto.cs
5. Application.Contracts/{Feature}/Update{Entity}Dto.cs
6. Application.Contracts/{Feature}/Get{Entity}sInput.cs
7. Application.Contracts/Permissions/{Entity}Permissions.cs

After writing contracts, emit signal:
🟢 CONTRACTS_READY: Application.Contracts/{Feature}/
```

**Agent B** - Task with `subagent_type="qa-engineer"`, `model="haiku"`:
```
Create test data scaffolding for {feature-name}.

Input: docs/domain/entities/{entity}.md (entity properties)
Skills: Apply xunit-testing-patterns, test-data-generation

Output (test data only - tests come later):
1. test/TestBase/{Feature}/{Entity}TestData.cs - Test constants
2. test/TestBase/{Feature}/{Entity}TestDataSeedContributor.cs - Data seeder

Use entity properties from entity.md. Does NOT need contracts.
```

**Checkpoint**: Contracts exist AND test data scaffolding ready. BA may still be completing (that's OK).

### Phase 2: Implementation + Tests (Parallel on CONTRACTS_READY)

On `🟢 CONTRACTS_READY` signal, launch BOTH agents in parallel:

**Agent A** - Task with `subagent_type="abp-developer"`, `model="sonnet"`:
```
Implement {feature-name} using generated contracts.

Input:
- docs/features/{feature-name}/technical-design.md
- Application.Contracts/{Feature}/ (contracts exist)

Skills: Apply abp-framework-patterns, efcore-patterns, fluentvalidation-patterns

Generate implementation files:
1. Domain/{Feature}/{Entity}.cs
2. Domain.Shared/{Feature}/{Entity}Consts.cs
3. Application/{Feature}/{Entity}AppService.cs
4. Application/{Feature}/{Entity}ApplicationMappers.cs
5. Application/{Feature}/Create{Entity}DtoValidator.cs
6. Application/{Feature}/Update{Entity}DtoValidator.cs
7. EntityFrameworkCore/EntityTypeConfigurations/{Entity}Configuration.cs
8. Update DbContext with DbSet<{Entity}>
9. Update PermissionDefinitionProvider

DO NOT recreate contracts - they exist.
Build: dotnet build api/*.slnx
```

**Agent B** - Task with `subagent_type="qa-engineer"`, `model="sonnet"`:
```
Create tests for {feature-name}.

Input:
- docs/features/{feature-name}/requirements.md (if exists)
- docs/features/{feature-name}/technical-design.md
- Application.Contracts/{Feature}/ (contracts exist)
- test/TestBase/{Feature}/ (TestData + Seeder already exist from Phase 1b)

Skills: Apply xunit-testing-patterns

Output:
1. docs/features/{feature-name}/test-cases.md (max 80 lines)
2. test/Application.Tests/{Feature}/{Entity}AppService_Tests.cs

TestData and Seeder already exist - DO NOT recreate them.
Write tests against INTERFACE.
Include: Happy path (5), Validation errors (3), Auth checks (2), Edge cases (3).
```

**Checkpoint**: Both complete. Build succeeds.

---

## Execution: --full-review Mode

Run default mode, then add review phase.

### Phase 3: Parallel Review + Security

Launch BOTH agents simultaneously:

**Agent A** - Task with `subagent_type="abp-code-reviewer"`, `model="haiku"`:
```
Review {feature-name} backend implementation. Be CONCISE.

Input: All source code from Phase 2
Output: docs/features/{feature-name}/review-report.md (max 50 lines)

Checklist: ABP patterns, async usage, validation, authorization, naming.
```

**Agent B** - Task with `subagent_type="security-engineer"`, `model="haiku"`:
```
Security audit for {feature-name}. Be CONCISE.

Input: All source code from Phase 2
Output: docs/features/{feature-name}/security-audit.md (max 50 lines)

Checklist: Authorization, input validation, OWASP top 10, error handling.
```
