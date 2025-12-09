# AppService Template

## Table of Contents
- [AppService Class](#appservice-class)
- [Interface](#interface)

## AppService Class

File: `{EntityName}AppService.cs`

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

## Interface

File: `I{EntityName}AppService.cs`

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
