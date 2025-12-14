# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2025-12-15

### Added

#### Agents (11)
- **Architects**
  - `backend-architect` - Designs REST APIs, database schemas, and technical specifications
  - `business-analyst` - Analyzes requirements, manages domain knowledge and business rules

- **Engineers**
  - `abp-developer` - Implements backend modules using ABP Framework
  - `react-developer` - Implements React frontend components and UX flows
  - `devops-engineer` - CI/CD pipelines, Docker containerization, deployment automation

- **Reviewers**
  - `abp-code-reviewer` - Reviews backend code for ABP patterns, DDD, security
  - `react-code-reviewer` - Reviews frontend code for React patterns, TypeScript, a11y
  - `qa-engineer` - Creates test plans, writes xUnit and Playwright tests
  - `security-engineer` - Security audits, threat modeling (STRIDE), OWASP compliance

- **Specialists**
  - `debugger` - Root cause analysis for errors and test failures
  - `database-migrator` - EF Core migrations, SQL review, data seeding

#### Skills (47)
- **Backend**: abp-framework-patterns, abp-entity-patterns, abp-service-patterns, abp-infrastructure-patterns, abp-api-implementation, abp-contract-scaffolding, efcore-patterns, ef-core-advanced-patterns, fluentvalidation-patterns, csharp-advanced-patterns, dotnet-async-patterns, linq-optimization-patterns
- **Architecture**: api-design-principles, api-response-patterns, domain-modeling, requirements-engineering, system-design-patterns, technical-design-patterns, mermaid-diagram-patterns
- **Testing**: xunit-testing-patterns, api-integration-testing, e2e-testing-patterns, javascript-testing-patterns, test-data-generation
- **Frontend**: react-development-patterns, react-code-review-patterns, modern-javascript-patterns, typescript-advanced-types
- **Security**: security-patterns, openiddict-authorization, authentication-authorization-patterns
- **Microservices**: distributed-events-advanced, grpc-integration-patterns, bulk-operations-patterns
- **Quality**: clean-code-dotnet, code-review-excellence, actionable-review-format-standards, debugging-patterns, error-handling-patterns
- **DevOps**: docker-dotnet-containerize, git-advanced-workflows
- **Meta**: claude-artifact-creator, content-retrieval, feature-development-workflow, knowledge-discovery, markdown-optimization

#### Commands (27)
- **Architecture**: `/arch:adr`, `/arch:api-contract`, `/arch:system-design`
- **Business Analysis**: `/ba:impact-analysis`, `/ba:release-notes`, `/ba:user-story`
- **Debug**: `/debug:smart-debug`
- **Documentation**: `/docs:optimize-md`, `/docs:validate-qmd`
- **Explain**: `/explain:code-explain`
- **Feature**: `/feature:add-feature`
- **Generate**: `/generate:doc-generate`, `/generate:entity`, `/generate:filter`, `/generate:migration`
- **Git**: `/git:generate-commit-msg`
- **QA**: `/qa:coverage-report`, `/qa:generate-tests`, `/qa:test-plan`
- **Refactor**: `/refactor:deps-audit`, `/refactor:refactor-clean`, `/refactor:tech-debt`
- **Review**: `/review:permissions`, `/review:pre-push`
- **TDD**: `/tdd:tdd-cycle`
- **Team**: `/team:issue`, `/team:standup-notes`

#### Supporting Files
- Knowledge base with 35+ concept files (SOLID, Clean Code, Testing, etc.)
- Guidelines for artifact creation and usage
- Workflow documentation
- Index files for quick discovery (AGENT-INDEX.md, SKILL-INDEX.md, COMMAND-INDEX.md)
- Context graph showing skill relationships

#### Installation
- Node.js CLI installer (`claude-abp`)
- Bash install script for Unix/macOS/WSL
- PowerShell install script for Windows
- Support for git clone, npx, curl one-liner, and manual copy

### Supported ABP Framework Versions
- ABP Framework 8.x
- ABP Framework 9.x
- ABP Framework 10.x (primary target)

[Unreleased]: https://github.com/thapaliyabikendra/ai-artifacts/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/thapaliyabikendra/ai-artifacts/releases/tag/v1.0.0
