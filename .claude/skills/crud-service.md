# Dynamic CRUD Service Generator

Generate a complete CRUD service following the TeacherAppService.cs pattern with all standard operations, logging, validation, and export/import capabilities.

## Instructions

When this skill is invoked, ask the user for the following information:

1. **Entity Name** (singular, e.g., "Product", "Student", "Order")
2. **Entity Properties** (comma-separated, e.g., "Name:string, Price:decimal, CategoryId:Guid")
3. **Related Entities** (for joins, e.g., "Category, Supplier")
4. **Namespace** (e.g., "NotificationBuilder" or "ProductManagement")
5. **Include Import/Export** (yes/no)

## Generation Template

Generate the following files:

### 1. AppService Class ({EntityName}AppService.cs)

```csharp
using AutoMapper;
using FluentValidation;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using {Namespace}.AppServices.Helpers;
using {Namespace}.BlobDto;
using {Namespace}.Dtos;
using {Namespace}.Helpers;
using {Namespace}.Responses;
using {Namespace}.{EntityNamePlural};
using ProductManagement.Constants;
using ProductManagement.Entities.{EntityNamePlural};
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Linq.Dynamic.Core;
using System.Threading.Tasks;
using Volo.Abp;
using Volo.Abp.Application.Dtos;
using Volo.Abp.Application.Services;
using Volo.Abp.Domain.Repositories;
using Volo.Abp.Users;

namespace {Namespace}.AppServices.{EntityNamePlural};

[ApiVersion("1.0")]
[Route("api/v{version:apiVersion}/app/{entity-name-lowercase}")]
public class {EntityName}AppService : ApplicationService, I{EntityName}AppService
{
    private readonly IRepository<{EntityName}, Guid> _{entityName}Repository;
    private readonly ILogger<{EntityName}AppService> _logger;
    private readonly ICurrentUser _currentUser;
    private readonly IMapper _mapper;
    private readonly IValidator<CreateUpdate{EntityName}Dto> _validator;
    // Add related entity repositories here

    public {EntityName}AppService(
        IRepository<{EntityName}, Guid> {entityName}Repository,
        ILogger<{EntityName}AppService> logger,
        ICurrentUser currentUser,
        IMapper mapper,
        IValidator<CreateUpdate{EntityName}Dto> validator)
    {
        _{entityName}Repository = {entityName}Repository;
        _logger = logger;
        _currentUser = currentUser;
        _mapper = mapper;
        _validator = validator;
    }

    /// <summary>
    /// Creates a new {entity-name} record.
    /// </summary>
    public async Task<ResponseDataDto<{EntityName}ResponseDto>> CreateAsync(CreateUpdate{EntityName}Dto input)
    {
        try
        {
            _logger.LogInformation("Starting {entity-name} creation process");

            // FluentValidation
            var validationResult = await _validator.ValidateAsync(input);
            if (!validationResult.IsValid)
            {
                var errorMessages = string.Join("; ", validationResult.Errors.Select(e => e.ErrorMessage));
                _logger.LogWarning("Validation failed for {entity-name} creation. Errors: {ValidationErrors}", errorMessages);
                throw new UserFriendlyException(errorMessages, "400");
            }

            var {entityName} = _mapper.Map<CreateUpdate{EntityName}Dto, {EntityName}>(input);
            await _{entityName}Repository.InsertAsync({entityName});

            _logger.LogInformation("{EntityName} created successfully with ID: {Id}", {entityName}.Id);

            return new ResponseDataDto<{EntityName}ResponseDto>
            {
                Success = true,
                Code = 200,
                Message = "{EntityName} created successfully.",
                Data = new {EntityName}ResponseDto
                {
                    Id = {entityName}.Id
                }
            };
        }
        catch (Exception ex) when (!(ex is UserFriendlyException))
        {
            _logger.LogError(ex, "Failed to create {entity-name}. Error: {ErrorMessage}", ex.Message);
            throw new UserFriendlyException(ErrorConsts.ServerError, "500");
        }
    }

    /// <summary>
    /// Updates an existing {entity-name} record.
    /// </summary>
    public async Task<ResponseDataDto<{EntityName}ResponseDto>> UpdateAsync(
        [Required(ErrorMessage = "Id is required.")] Guid id,
        CreateUpdate{EntityName}Dto input)
    {
        try
        {
            _logger.LogInformation("Starting {entity-name} update process for ID: {Id}", id);

            // FluentValidation
            var validationResult = await _validator.ValidateAsync(input);
            if (!validationResult.IsValid)
            {
                var errorMessages = string.Join("; ", validationResult.Errors.Select(e => e.ErrorMessage));
                _logger.LogWarning("Validation failed for {entity-name} update. ID: {Id}, Errors: {ValidationErrors}",
                    id, errorMessages);
                throw new UserFriendlyException(errorMessages, "400");
            }

            var {entityName} = await _{entityName}Repository.FindAsync(id);
            if ({entityName} == null)
            {
                _logger.LogWarning("{EntityName} with ID: {Id} not found for update operation", id);
                throw new UserFriendlyException(ErrorConsts.NotFound, "404");
            }

            _mapper.Map(input, {entityName});
            await _{entityName}Repository.UpdateAsync({entityName});

            _logger.LogInformation("{EntityName} updated successfully with ID: {Id}", id);

            return new ResponseDataDto<{EntityName}ResponseDto>
            {
                Success = true,
                Code = 200,
                Message = "{EntityName} updated successfully.",
                Data = new {EntityName}ResponseDto
                {
                    Id = {entityName}.Id
                }
            };
        }
        catch (Exception ex) when (!(ex is UserFriendlyException))
        {
            _logger.LogError(ex, "Failed to update {entity-name} ID {Id}. Error: {ErrorMessage}",
                id, ex.Message);
            throw new UserFriendlyException(ErrorConsts.ServerError, "500");
        }
    }

    /// <summary>
    /// Deletes a {entity-name} record.
    /// </summary>
    public async Task<ResponseDataDto<{EntityName}ResponseDto>> DeleteAsync(
        [Required(ErrorMessage = "Id is required.")] Guid id)
    {
        try
        {
            _logger.LogInformation("Starting {entity-name} deletion process for ID: {Id}", id);

            var {entityName} = await _{entityName}Repository.FindAsync(id);
            if ({entityName} == null)
            {
                _logger.LogWarning("{EntityName} with ID: {Id} not found.", id);
                throw new UserFriendlyException(ErrorConsts.NotFound, "404");
            }

            await _{entityName}Repository.DeleteAsync(id);
            _logger.LogInformation("{EntityName} deleted successfully with ID: {Id}", id);

            return new ResponseDataDto<{EntityName}ResponseDto>
            {
                Success = true,
                Code = 200,
                Message = "{EntityName} deleted successfully.",
                Data = new {EntityName}ResponseDto
                {
                    Id = id
                }
            };
        }
        catch (Exception ex) when (!(ex is UserFriendlyException))
        {
            _logger.LogError(ex, "Failed to delete {entity-name} ID {Id}. Error: {ErrorMessage}",
                id, ex.Message);
            throw new UserFriendlyException(ErrorConsts.ServerError, "500");
        }
    }

    /// <summary>
    /// Retrieves a paginated list of {entity-name-plural} with optional filtering and sorting.
    /// </summary>
    public async Task<ResponseDataDto<PagedResultDto<{EntityName}Dto>>> GetListAsync(
        PagedAndSortedResultRequestDto input,
        {EntityName}Filter filter)
    {
        try
        {
            _logger.LogInformation("Starting {entity-name} list retrieval process with filter: {@Filter}", filter);

            if (input.Sorting.IsNullOrWhiteSpace())
            {
                input.Sorting = "Id"; // Change to appropriate default sort field
            }

            var {entityNamePlural} = await Get{EntityNamePlural}Async(filter);

            var dtos = await AsyncExecuter.ToListAsync({entityNamePlural}
                .OrderBy(input.Sorting)
                .Skip(input.SkipCount)
                .Take(input.MaxResultCount));

            var totalCount = await AsyncExecuter.CountAsync({entityNamePlural});

            _logger.LogInformation("{EntityName} list retrieved successfully with {TotalCount} records.", totalCount);

            var result = new PagedResultDto<{EntityName}Dto>(totalCount, dtos);

            return new ResponseDataDto<PagedResultDto<{EntityName}Dto>>
            {
                Success = true,
                Code = 200,
                Message = "{EntityName} list retrieved successfully.",
                Data = result
            };
        }
        catch (Exception ex) when (!(ex is UserFriendlyException))
        {
            _logger.LogError(ex, "Failed to retrieve {entity-name} list. Error: {ErrorMessage}", ex.Message);
            throw new UserFriendlyException(ErrorConsts.ServerError, "500");
        }
    }

    /// <summary>
    /// Retrieves a specific {entity-name} by ID.
    /// </summary>
    public async Task<ResponseDataDto<{EntityName}Dto>> GetAsync(
        [Required(ErrorMessage = "Id is required.")] Guid id)
    {
        try
        {
            _logger.LogInformation("Starting {entity-name} retrieval process for ID: {Id}", id);

            var {entityName} = await _{entityName}Repository.FindAsync(id);
            if ({entityName} == null)
            {
                _logger.LogWarning("{EntityName} with ID: {Id} not found.", id);
                throw new UserFriendlyException(ErrorConsts.NotFound, "404");
            }

            var result = _mapper.Map<{EntityName}, {EntityName}Dto>({entityName});
            _logger.LogInformation("{EntityName} retrieved successfully with ID: {Id}", id);

            return new ResponseDataDto<{EntityName}Dto>
            {
                Success = true,
                Code = 200,
                Message = "{EntityName} retrieved successfully.",
                Data = result
            };
        }
        catch (Exception ex) when (!(ex is UserFriendlyException))
        {
            _logger.LogError(ex, "Failed to retrieve {entity-name} ID {Id}. Error: {ErrorMessage}",
                id, ex.Message);
            throw new UserFriendlyException(ErrorConsts.ServerError, "500");
        }
    }

    #region Private Methods

    private async Task<IQueryable<{EntityName}Dto>> Get{EntityNamePlural}Async({EntityName}Filter filter)
    {
        filter.SearchKeyword = filter.SearchKeyword?.Trim()?.ToLower();

        var {entityNamePlural} = await _{entityName}Repository.GetQueryableAsync();

        var query = {entityNamePlural}
            .Select(x => new {EntityName}Dto
            {
                Id = x.Id,
                // Map properties here
            })
            .WhereIf(!string.IsNullOrWhiteSpace(filter.SearchKeyword),
                x => false // Add search conditions here
            );

        return query;
    }

    #endregion
}
```

### 2. Interface (I{EntityName}AppService.cs)

```csharp
using Microsoft.AspNetCore.Mvc;
using {Namespace}.Dtos;
using {Namespace}.Responses;
using {Namespace}.{EntityNamePlural};
using System;
using System.ComponentModel.DataAnnotations;
using System.Threading.Tasks;
using Volo.Abp.Application.Dtos;
using Volo.Abp.Application.Services;

namespace {Namespace}.{EntityNamePlural};

public interface I{EntityName}AppService : IApplicationService
{
    Task<ResponseDataDto<{EntityName}ResponseDto>> CreateAsync(CreateUpdate{EntityName}Dto input);
    Task<ResponseDataDto<{EntityName}ResponseDto>> UpdateAsync([Required] Guid id, CreateUpdate{EntityName}Dto input);
    Task<ResponseDataDto<{EntityName}ResponseDto>> DeleteAsync([Required] Guid id);
    Task<ResponseDataDto<PagedResultDto<{EntityName}Dto>>> GetListAsync(PagedAndSortedResultRequestDto input, {EntityName}Filter filter);
    Task<ResponseDataDto<{EntityName}Dto>> GetAsync([Required] Guid id);
}
```

### 3. DTOs

Create the following DTO files:

#### {EntityName}Dto.cs
```csharp
using System;

namespace {Namespace}.{EntityNamePlural};

public class {EntityName}Dto
{
    public Guid Id { get; set; }
    // Add entity properties here
}
```

#### CreateUpdate{EntityName}Dto.cs
```csharp
using System;

namespace {Namespace}.{EntityNamePlural};

public class CreateUpdate{EntityName}Dto
{
    // Add entity properties here (without Id)
}
```

#### {EntityName}ResponseDto.cs
```csharp
using System;

namespace {Namespace}.{EntityNamePlural};

public class {EntityName}ResponseDto
{
    public Guid Id { get; set; }
}
```

#### {EntityName}Filter.cs
```csharp
namespace {Namespace}.{EntityNamePlural};

public class {EntityName}Filter
{
    public string SearchKeyword { get; set; }
    // Add additional filter properties
}
```

### 4. Validator ({EntityName}Validator.cs)

```csharp
using FluentValidation;
using {Namespace}.{EntityNamePlural};

namespace {Namespace}.Validators;

public class {EntityName}Validator : AbstractValidator<CreateUpdate{EntityName}Dto>
{
    public {EntityName}Validator()
    {
        // Add validation rules here
        // Example:
        // RuleFor(x => x.Name)
        //     .NotEmpty().WithMessage("Name is required.")
        //     .MaximumLength(100).WithMessage("Name cannot exceed 100 characters.");
    }
}
```

## Optional: Export/Import Functionality

If export/import is requested, add these methods to the AppService:

```csharp
/// <summary>
/// Exports {entity-name} data in different formats.
/// </summary>
public async Task<ResponseDataDto<ExportFileBlobDto>> ExportAsync([FromQuery] {EntityName}ExportRequestDto request)
{
    try
    {
        _logger.LogInformation("Starting {entity-name} export process with format: {Format}", request.Format);

        var data = await Get{EntityNamePlural}Async(request.Filter ?? default);
        var list = await AsyncExecuter.ToListAsync(data);

        if (!list.Any())
        {
            _logger.LogWarning("No {entity-name} data found for export");
            throw new UserFriendlyException("No data found to export.", "404");
        }

        var fileContent = await _mapperService.Export{EntityNamePlural}DataAsync(list, request.Format, request.IncludeHeaders);

        var response = new ExportFileBlobDto
        {
            Name = MapperService.GetSheetName(),
            Content = fileContent
        };

        _logger.LogInformation("{EntityName} export completed successfully. Format: {Format}, Records: {Count}",
            request.Format, list.Count);

        return new ResponseDataDto<ExportFileBlobDto>
        {
            Success = true,
            Message = "Export completed successfully.",
            Code = 200,
            Data = response
        };
    }
    catch (Exception ex) when (!(ex is UserFriendlyException))
    {
        _logger.LogError(ex, "Failed to export {entity-name} data. Error: {ErrorMessage}", ex.Message);
        throw new UserFriendlyException("An error occurred during export.", "500");
    }
}

/// <summary>
/// Imports {entity-name} data from Excel file.
/// </summary>
public async Task<ResponseDataDto<{EntityName}ImportResponseDto>> ImportAsync([FromForm] BulkImportFileDto input, [FromQuery] bool skipHeaderRow = false)
{
    var correlationId = Guid.NewGuid().ToString();
    var startTime = DateTime.UtcNow;

    try
    {
        _logger.LogInformation("Starting {entity-name} import process for file: {FileName}", input.File?.FileName);

        if (input?.File == null || input.File.Length == 0)
        {
            _logger.LogWarning("Import failed: No file provided or file is empty");
            throw new UserFriendlyException("No file provided or file is empty.", "400");
        }

        var fileExtension = Path.GetExtension(input.File.FileName)?.ToLowerInvariant();
        if (fileExtension != ".xlsx" && fileExtension != ".xls")
        {
            throw new UserFriendlyException("Only Excel files (.xlsx, .xls) are supported for import.", "400");
        }

        var response = await _mapperService.Import{EntityNamePlural}DataAsync(input.File, skipHeaderRow, correlationId);

        var totalDuration = DateTime.UtcNow - startTime;
        _logger.LogInformation("{EntityName} import completed in {TotalDuration}ms", totalDuration.TotalMilliseconds);

        return new ResponseDataDto<{EntityName}ImportResponseDto>
        {
            Success = true,
            Code = 200,
            Message = $"Import completed. {response.SuccessCount} records processed successfully.",
            Data = response
        };
    }
    catch (Exception ex) when (!(ex is UserFriendlyException))
    {
        _logger.LogError(ex, "Failed to import {entity-name} data. Error: {ErrorMessage}", ex.Message);
        throw new UserFriendlyException("An error occurred during import.", "500");
    }
}
```

## Usage Instructions

After generating the files:

1. Register the validator in your dependency injection container
2. Configure AutoMapper mappings for the entity and DTOs
3. Add the service to your module's ConfigureServices method
4. Implement the IMapperService methods if using export/import
5. Adjust the filtering logic in the private Get{EntityNamePlural}Async method
6. Update the default sorting field in GetListAsync
7. Add any additional business logic as needed

## Placeholders to Replace

- `{EntityName}` - Singular entity name (e.g., "Teacher")
- `{EntityNamePlural}` - Plural entity name (e.g., "Teachers")
- `{entityName}` - Camel case entity name (e.g., "teacher")
- `{entityNamePlural}` - Camel case plural (e.g., "teachers")
- `{entity-name}` - Lowercase with hyphens (e.g., "teacher")
- `{entity-name-plural}` - Lowercase plural with hyphens (e.g., "teachers")
- `{entity-name-lowercase}` - Lowercase for route (e.g., "teacher")
- `{Namespace}` - The application namespace

## Implementation Steps

1. Gather entity information from the user
2. Generate all necessary files with proper naming
3. Replace all placeholders with actual values
4. Create the directory structure if it doesn't exist
5. Save all files in their appropriate locations
6. Provide a summary of generated files and next steps
