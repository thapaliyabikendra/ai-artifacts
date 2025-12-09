# Export/Import Templates

Optional functionality for data export and import operations.

## Table of Contents
- [Export Method](#export-method)
- [Import Method](#import-method)
- [Additional DTOs](#additional-dtos)
- [Dependencies](#dependencies)

## Export Method

Add to `{EntityName}AppService.cs`:

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
```

## Import Method

Add to `{EntityName}AppService.cs`:

```csharp
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

## Additional DTOs

### ExportRequestDto

File: `{EntityName}ExportRequestDto.cs`

```csharp
namespace {Namespace}.{EntityNamePlural};

public class {EntityName}ExportRequestDto
{
    public string Format { get; set; } = "xlsx";
    public bool IncludeHeaders { get; set; } = true;
    public {EntityName}Filter Filter { get; set; }
}
```

### ImportResponseDto

File: `{EntityName}ImportResponseDto.cs`

```csharp
namespace {Namespace}.{EntityNamePlural};

public class {EntityName}ImportResponseDto
{
    public int TotalCount { get; set; }
    public int SuccessCount { get; set; }
    public int FailedCount { get; set; }
    public List<string> Errors { get; set; } = new();
}
```

## Dependencies

Add to AppService constructor:

```csharp
private readonly IMapperService _mapperService;

public {EntityName}AppService(
    // ... existing dependencies ...
    IMapperService mapperService)
{
    // ... existing assignments ...
    _mapperService = mapperService;
}
```

Add to interface:

```csharp
Task<ResponseDataDto<ExportFileBlobDto>> ExportAsync({EntityName}ExportRequestDto request);
Task<ResponseDataDto<{EntityName}ImportResponseDto>> ImportAsync(BulkImportFileDto input, bool skipHeaderRow = false);
```

## IMapperService Methods to Implement

```csharp
Task<byte[]> Export{EntityNamePlural}DataAsync(List<{EntityName}Dto> data, string format, bool includeHeaders);
Task<{EntityName}ImportResponseDto> Import{EntityNamePlural}DataAsync(IFormFile file, bool skipHeaderRow, string correlationId);
```
