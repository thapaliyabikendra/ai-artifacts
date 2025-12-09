---
name: crud-service
description: Generate complete ABP Framework CRUD services following established patterns with AppService, Interface, DTOs, and FluentValidation. Use when creating new entity services for Volo.Abp projects that need standard CRUD operations (Create, Read, Update, Delete, List), logging, validation, and optional import/export capabilities. Triggers on requests like "create CRUD for Product entity", "generate service for Order", or "scaffold CRUD operations for Student".
---

# Dynamic CRUD Service Generator

Generate ABP Framework CRUD services with standard operations, logging, validation, and export/import.

## Workflow

1. **Gather entity information** from user:
   - Entity Name (singular, e.g., "Product", "Student", "Order")
   - Entity Properties (e.g., "Name:string, Price:decimal, CategoryId:Guid")
   - Related Entities for joins (optional, e.g., "Category, Supplier")
   - Namespace (e.g., "ProductManagement")
   - Include Import/Export (yes/no)

2. **Generate files** using templates:
   - `{EntityName}AppService.cs` - [appservice-template.md](references/appservice-template.md)
   - `I{EntityName}AppService.cs` - [appservice-template.md](references/appservice-template.md#interface)
   - DTOs - [dto-templates.md](references/dto-templates.md)
   - Validator - [validator-template.md](references/validator-template.md)
   - Export/Import (if requested) - [export-import.md](references/export-import.md)

3. **Replace placeholders**:
   | Placeholder | Format | Example |
   |-------------|--------|---------|
   | `{EntityName}` | PascalCase singular | Teacher |
   | `{EntityNamePlural}` | PascalCase plural | Teachers |
   | `{entityName}` | camelCase singular | teacher |
   | `{entityNamePlural}` | camelCase plural | teachers |
   | `{entity-name-lowercase}` | lowercase (for routes) | teacher |
   | `{Namespace}` | Application namespace | ProductManagement |

4. **Create directory structure** and save files in appropriate locations.

## Post-Generation Steps

1. Register validator in DI container
2. Configure AutoMapper mappings for entity and DTOs
3. Add service to module's ConfigureServices method
4. Implement IMapperService methods if using export/import
5. Adjust filtering logic in Get{EntityNamePlural}Async method
6. Update default sorting field in GetListAsync
