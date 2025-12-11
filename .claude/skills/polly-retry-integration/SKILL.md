# Polly Retry Integration Skill

## Overview
A comprehensive, reusable skill for designing, developing, and integrating Polly retry mechanisms in .NET projects. This skill provides production-grade resilience patterns with feature flag support, configurable policies, and comprehensive logging.

## Skill Metadata
- **Complexity**: Advanced
- **Estimated Time**: 2-4 hours
- **Prerequisites**: .NET 6.0+, Basic understanding of async/await, Dependency injection
- **Dependencies**:
  - Polly (v8.0+)
  - Polly.Extensions.Http
  - Polly.Contrib.WaitAndRetry

## Phases

### Phase 1: Analysis & Planning

#### 1.1 Identify Integration Points
Analyze the codebase to identify services that need retry logic:

**Search Patterns:**
```bash
# Find HTTP client usages
grep -r "HttpClient" --include="*.cs"
grep -r "HttpRequestMessage" --include="*.cs"

# Find database operations
grep -r "SaveChangesAsync" --include="*.cs"
grep -r "DbContext" --include="*.cs"

# Find external API calls
grep -r "SendAsync" --include="*.cs"
grep -r "PostAsync\|GetAsync\|PutAsync" --include="*.cs"

# Find email sending operations
grep -r "IEmailSender\|SmtpClient" --include="*.cs"
```

**Create Integration Checklist:**
- [ ] HTTP/API clients
- [ ] Database operations (EF Core)
- [ ] Email services
- [ ] Message queue operations
- [ ] File I/O operations
- [ ] External service integrations

#### 1.2 Define Retry Requirements
Document requirements for each integration point:

| Service Type | Retry Count | Base Delay | Max Delay | Transient Errors |
|-------------|-------------|------------|-----------|------------------|
| HTTP APIs | 3 | 2s | 30s | 5xx, 429, 503, Timeout |
| Database | 3 | 1s | 10s | Deadlock, Connection, Concurrency |
| Email | 5 | 2s | 60s | SMTP timeout, Connection |
| File I/O | 3 | 1s | 5s | IOException, Access denied |

### Phase 2: Package Installation

#### 2.1 Add NuGet Packages
Add to your `.csproj` files:

```xml
<PackageReference Include="Polly" Version="8.2.0" />
<PackageReference Include="Polly.Extensions.Http" Version="3.0.0" />
<PackageReference Include="Polly.Contrib.WaitAndRetry" Version="1.1.1" />
<PackageReference Include="Microsoft.Extensions.Http.Polly" Version="8.0.0" />
```

Or via CLI:
```bash
dotnet add package Polly
dotnet add package Polly.Extensions.Http
dotnet add package Polly.Contrib.WaitAndRetry
dotnet add package Microsoft.Extensions.Http.Polly
```

### Phase 3: Core Implementation

#### 3.1 Create Interface
Location: `{Project}.Application.Contracts/RetryPolicy/IRetryPolicyService.cs`

```csharp
using Polly;
using System;
using System.Net.Http;
using System.Threading.Tasks;

namespace {YourProject}.RetryPolicy;

public interface IRetryPolicyService
{
    /// <summary>
    /// Builds an HTTP retry policy with exponential backoff and jitter.
    /// Handles transient HTTP errors, timeouts, and respects Retry-After headers.
    /// </summary>
    Task<IAsyncPolicy<HttpResponseMessage>> BuildHttpRetryPolicyAsync(string operationName);

    /// <summary>
    /// Builds a generic retry policy for any operation with custom result validation.
    /// </summary>
    Task<AsyncPolicy<TResult>> BuildRetryPolicyAsync<TResult>(
        string operationName,
        Func<TResult, bool>? shouldRetry = null);

    /// <summary>
    /// Builds a database retry policy for handling transient database exceptions.
    /// </summary>
    Task<IAsyncPolicy> BuildDatabaseRetryPolicyAsync(string operationName);
}
```

#### 3.2 Create Implementation
Location: `{Project}.Application/AppServices/RetryPolicy/RetryPolicyService.cs`

```csharp
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using Npgsql;
using Polly;
using Polly.Contrib.WaitAndRetry;
using Polly.Extensions.Http;
using System;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Net.Sockets;
using System.Threading.Tasks;
using Volo.Abp.Data;
using Volo.Abp.DependencyInjection;

namespace {YourProject}.AppServices.RetryPolicy;

public class RetryPolicyService : IRetryPolicyService, ITransientDependency
{
    private readonly ILogger<RetryPolicyService> _logger;
    private readonly IConfiguration _configuration;

    public RetryPolicyService(
        ILogger<RetryPolicyService> logger,
        IConfiguration configuration)
    {
        _logger = logger;
        _configuration = configuration;
    }

    /// <summary>
    /// Builds HTTP retry policy with exponential backoff and jitter
    /// </summary>
    public async Task<IAsyncPolicy<HttpResponseMessage>> BuildHttpRetryPolicyAsync(string operationName)
    {
        var (retryCount, _) = await GetRetryConfigurationAsync();

        return HttpPolicyExtensions
            .HandleTransientHttpError()
            .Or<TimeoutException>()
            .Or<TaskCanceledException>()
            .Or<IOException>()
            .Or<SocketException>()
            .Or<Polly.Timeout.TimeoutRejectedException>()
            .OrResult(msg => msg.StatusCode == HttpStatusCode.TooManyRequests)      // 429
            .OrResult(msg => msg.StatusCode == HttpStatusCode.BadGateway)           // 502
            .OrResult(msg => msg.StatusCode == HttpStatusCode.ServiceUnavailable)   // 503
            .OrResult(msg => msg.StatusCode == HttpStatusCode.GatewayTimeout)       // 504
            .WaitAndRetryAsync(
                retryCount: retryCount,
                sleepDurationProvider: retryAttempt =>
                {
                    // Exponential backoff with jitter
                    var exponentialDelay = TimeSpan.FromSeconds(Math.Pow(2, retryAttempt));
                    var jitter = TimeSpan.FromMilliseconds(Random.Shared.Next(0, 1000));
                    return exponentialDelay + jitter;
                },
                onRetryAsync: async (outcome, timespan, retryAttempt, context) =>
                {
                    var statusCode = outcome.Result?.StatusCode ?? HttpStatusCode.RequestTimeout;

                    // Check if Retry-After header is present
                    if (outcome.Result != null &&
                        (outcome.Result.StatusCode == HttpStatusCode.TooManyRequests ||
                         outcome.Result.StatusCode == HttpStatusCode.ServiceUnavailable) &&
                        outcome.Result.Headers.RetryAfter != null)
                    {
                        var retryAfter = outcome.Result.Headers.RetryAfter.Delta ?? TimeSpan.FromSeconds(5);
                        _logger.LogWarning(
                            "[HTTP Retry {RetryAttempt}/{TotalRetries}] '{OperationName}' - " +
                            "Status: {StatusCode}, Respecting Retry-After: {RetryAfter:F2}s",
                            retryAttempt, retryCount, operationName, statusCode, retryAfter.TotalSeconds);
                        await Task.Delay(retryAfter);
                    }
                    else
                    {
                        _logger.LogWarning(
                            "[HTTP Retry {RetryAttempt}/{TotalRetries}] '{OperationName}' - " +
                            "Status: {StatusCode}, Waiting: {RetryDelay:F2}s",
                            retryAttempt, retryCount, operationName, statusCode, timespan.TotalSeconds);
                    }
                });
    }

    /// <summary>
    /// Builds generic retry policy with custom result validation
    /// </summary>
    public async Task<AsyncPolicy<TResult>> BuildRetryPolicyAsync<TResult>(
        string operationName,
        Func<TResult, bool>? shouldRetry = null)
    {
        var (retryCount, _) = await GetRetryConfigurationAsync();

        var retryableExceptions = new[]
        {
            typeof(HttpRequestException),
            typeof(TaskCanceledException),
            typeof(TimeoutException),
            typeof(IOException),
            typeof(SocketException),
            typeof(Polly.Timeout.TimeoutRejectedException)
        };

        var policyBuilder = Policy<TResult>
            .Handle<Exception>(ex => retryableExceptions.Any(t => t.IsAssignableFrom(ex.GetType())));

        // Add result-based retry if custom validation is provided
        if (shouldRetry != null)
        {
            policyBuilder = policyBuilder.OrResult(result => shouldRetry(result));
        }

        return policyBuilder.WaitAndRetryAsync(
            retryCount: retryCount,
            sleepDurationProvider: (retryAttempt, delegateResult, context) =>
            {
                var exponentialDelay = TimeSpan.FromSeconds(Math.Pow(2, retryAttempt));
                var jitter = TimeSpan.FromMilliseconds(Random.Shared.Next(0, 1000));
                return exponentialDelay + jitter;
            },
            onRetryAsync: async (outcome, timespan, retryAttempt, context) =>
            {
                if (outcome.Exception != null)
                {
                    _logger.LogWarning(
                        outcome.Exception,
                        "[Generic Retry {RetryAttempt}/{TotalRetries}] '{OperationName}' - " +
                        "Waiting {RetryDelay:F1}s. Error: {ErrorMessage}",
                        retryAttempt, retryCount, operationName, timespan.TotalSeconds, outcome.Exception.Message);
                }
            });
    }

    /// <summary>
    /// Builds database retry policy for transient database exceptions
    /// </summary>
    public async Task<IAsyncPolicy> BuildDatabaseRetryPolicyAsync(string operationName)
    {
        var (retryCount, _) = await GetRetryConfigurationAsync();

        return Policy
            .Handle<DbUpdateConcurrencyException>()
            .Or<DbUpdateException>(ex =>
                ex.InnerException is NpgsqlException npgsqlEx && IsTransientPostgresException(npgsqlEx))
            .Or<NpgsqlException>(ex => IsTransientPostgresException(ex))
            .Or<TimeoutException>()
            .Or<InvalidOperationException>(ex => ex.Message.Contains("connection", StringComparison.OrdinalIgnoreCase))
            .WaitAndRetryAsync(
                retryCount: retryCount,
                sleepDurationProvider: (retryAttempt) =>
                {
                    var exponentialDelay = TimeSpan.FromSeconds(Math.Pow(2, retryAttempt));
                    var jitter = TimeSpan.FromMilliseconds(Random.Shared.Next(0, 1000));
                    return exponentialDelay + jitter;
                },
                onRetry: (exception, timespan, retryAttempt, context) =>
                {
                    _logger.LogWarning(
                        exception,
                        "[DB Retry {RetryAttempt}/{TotalRetries}] '{OperationName}' - " +
                        "Waiting {RetryDelay:F2}s. Error: {ErrorMessage}",
                        retryAttempt, retryCount, operationName, timespan.TotalSeconds, exception.Message);
                });
    }

    /// <summary>
    /// Determines if PostgreSQL exception is transient
    /// </summary>
    private static bool IsTransientPostgresException(NpgsqlException ex)
    {
        var transientSqlStates = new[]
        {
            "40001", // Serialization failure
            "40P01", // Deadlock detected
            "55P03", // Lock not available
            "57014", // Query canceled
            "53300", // Too many connections
            "57P03", // Cannot connect now
            "08000", // Connection exception
            "08003", // Connection does not exist
            "08006"  // Connection failure
        };

        return transientSqlStates.Contains(ex.SqlState);
    }

    /// <summary>
    /// Reads retry configuration from appsettings
    /// </summary>
    private Task<(int retryCount, TimeSpan[] delay)> GetRetryConfigurationAsync()
    {
        var featureFlagsSection = _configuration.GetSection("FeatureManagement:FeatureFlags");
        var retryPolicyFeature = featureFlagsSection.GetChildren()
            .FirstOrDefault(f => f["id"] == "RetryPolicy");

        int retryCount = 3;
        int baseDelaySeconds = 2;

        if (retryPolicyFeature != null)
        {
            retryCount = retryPolicyFeature.GetValue<int>("parameters:RetryCount", 3);
            baseDelaySeconds = retryPolicyFeature.GetValue<int>("parameters:BaseDelaySeconds", 2);
        }

        var delay = Backoff.DecorrelatedJitterBackoffV2(
            medianFirstRetryDelay: TimeSpan.FromSeconds(baseDelaySeconds),
            retryCount: retryCount
        ).ToArray();

        return Task.FromResult((retryCount, delay));
    }
}
```

### Phase 4: Configuration

#### 4.1 Add Feature Flag Configuration
Add to `appsettings.json`:

```json
{
  "FeatureManagement": {
    "FeatureFlags": [
      {
        "id": "RetryPolicy",
        "description": "Enable Polly retry policies for resilient operations",
        "requiresAll": false,
        "enabled": true,
        "parameters": {
          "RetryCount": 3,
          "BaseDelaySeconds": 2
        }
      }
    ]
  }
}
```

For environment-specific overrides, add to `appsettings.Production.json`:

```json
{
  "FeatureManagement": {
    "FeatureFlags": [
      {
        "id": "RetryPolicy",
        "enabled": true,
        "parameters": {
          "RetryCount": 5,
          "BaseDelaySeconds": 3
        }
      }
    ]
  }
}
```

### Phase 5: Integration Patterns

#### 5.1 HTTP Client Integration

**Pattern A: Typed HttpClient with Polly**
```csharp
// In Startup.cs or Module configuration
services.AddHttpClient<IMyApiClient, MyApiClient>()
    .AddPolicyHandler((serviceProvider, request) =>
    {
        var retryPolicy = serviceProvider.GetRequiredService<IRetryPolicyService>();
        return retryPolicy.BuildHttpRetryPolicyAsync("MyApiClient").GetAwaiter().GetResult();
    });
```

**Pattern B: Manual Integration**
```csharp
public class MyService
{
    private readonly HttpClient _httpClient;
    private readonly IRetryPolicyService _retryPolicyService;
    private readonly IFeatureManagementService _featureService;

    public async Task<HttpResponseMessage> CallExternalApiAsync(string url)
    {
        HttpResponseMessage response;

        if (await _featureService.IsEnabledAsync("RetryPolicy"))
        {
            var retryPolicy = await _retryPolicyService.BuildHttpRetryPolicyAsync("CallExternalApi");
            response = await retryPolicy.ExecuteAsync(async () =>
            {
                var request = new HttpRequestMessage(HttpMethod.Get, url);
                return await _httpClient.SendAsync(request);
            });
        }
        else
        {
            response = await _httpClient.GetAsync(url);
        }

        return response;
    }
}
```

#### 5.2 Database Operations Integration

```csharp
public class MyRepository
{
    private readonly DbContext _dbContext;
    private readonly IRetryPolicyService _retryPolicyService;
    private readonly IFeatureManagementService _featureService;
    private readonly IUnitOfWorkManager _unitOfWorkManager;

    public async Task<MyEntity> CreateAsync(MyEntity entity)
    {
        if (await _featureService.IsEnabledAsync("RetryPolicy"))
        {
            var dbPolicy = await _retryPolicyService.BuildDatabaseRetryPolicyAsync("CreateEntity");

            return await dbPolicy.ExecuteAsync(async () =>
            {
                using (var uow = _unitOfWorkManager.Begin(requiresNew: true))
                {
                    await _dbContext.MyEntities.AddAsync(entity);
                    await _dbContext.SaveChangesAsync();
                    await uow.CompleteAsync();
                    return entity;
                }
            });
        }
        else
        {
            await _dbContext.MyEntities.AddAsync(entity);
            await _dbContext.SaveChangesAsync();
            return entity;
        }
    }
}
```

#### 5.3 Email Service Integration

```csharp
public class EmailService
{
    private readonly IEmailSender _emailSender;
    private readonly IRetryPolicyService _retryPolicyService;
    private readonly IFeatureManagementService _featureService;

    public async Task<bool> SendEmailAsync(string to, string subject, string body)
    {
        if (await _featureService.IsEnabledAsync("RetryPolicy"))
        {
            var retryPolicy = await _retryPolicyService.BuildRetryPolicyAsync<bool>(
                operationName: $"SendEmail-{to}",
                shouldRetry: result => !result // Retry if send failed
            );

            return await retryPolicy.ExecuteAsync(async () =>
            {
                try
                {
                    await _emailSender.SendAsync(to, subject, body);
                    return true;
                }
                catch (SmtpException ex)
                {
                    _logger.LogError(ex, "Email send failed");
                    return false;
                }
            });
        }
        else
        {
            await _emailSender.SendAsync(to, subject, body);
            return true;
        }
    }
}
```

#### 5.4 NocoDB/External API Integration

```csharp
public class DynamicTableProxyService
{
    private readonly INocoApi _nocoApi;
    private readonly IRetryPolicyService _retryPolicyService;
    private readonly IFeatureManagementService _featureService;

    public async Task<object> CreateAsync(string tableName, object data)
    {
        object response;

        if (await _featureService.IsEnabledAsync("RetryPolicy"))
        {
            var retryPolicy = await _retryPolicyService.BuildRetryPolicyAsync<object>(
                operationName: $"NOCO_CREATE_{tableName}",
                shouldRetry: r => r == null // Retry if response is null
            );

            response = await retryPolicy.ExecuteAsync(async () =>
            {
                return await _nocoApi.CreateAsync(tableName, data);
            });
        }
        else
        {
            response = await _nocoApi.CreateAsync(tableName, data);
        }

        return response;
    }
}
```

### Phase 6: Testing Strategy

#### 6.1 Unit Tests

```csharp
public class RetryPolicyServiceTests
{
    [Fact]
    public async Task HttpRetryPolicy_Should_Retry_On_Transient_Errors()
    {
        // Arrange
        var mockLogger = new Mock<ILogger<RetryPolicyService>>();
        var mockConfig = new Mock<IConfiguration>();

        var service = new RetryPolicyService(mockLogger.Object, mockConfig.Object);
        var attemptCount = 0;

        // Act
        var policy = await service.BuildHttpRetryPolicyAsync("TestOperation");

        var result = await policy.ExecuteAsync(async () =>
        {
            attemptCount++;
            if (attemptCount < 3)
            {
                return new HttpResponseMessage(HttpStatusCode.ServiceUnavailable);
            }
            return new HttpResponseMessage(HttpStatusCode.OK);
        });

        // Assert
        Assert.Equal(3, attemptCount);
        Assert.Equal(HttpStatusCode.OK, result.StatusCode);
    }

    [Fact]
    public async Task DatabaseRetryPolicy_Should_Retry_On_Deadlock()
    {
        // Arrange
        var mockLogger = new Mock<ILogger<RetryPolicyService>>();
        var mockConfig = new Mock<IConfiguration>();

        var service = new RetryPolicyService(mockLogger.Object, mockConfig.Object);
        var attemptCount = 0;

        // Act
        var policy = await service.BuildDatabaseRetryPolicyAsync("TestDbOperation");

        await policy.ExecuteAsync(async () =>
        {
            attemptCount++;
            if (attemptCount < 2)
            {
                throw new DbUpdateException("Deadlock",
                    new NpgsqlException("", null, "", "40P01"));
            }
            return Task.CompletedTask;
        });

        // Assert
        Assert.Equal(2, attemptCount);
    }
}
```

#### 6.2 Integration Tests

```csharp
public class HttpClientWithRetryTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly WebApplicationFactory<Program> _factory;

    public HttpClientWithRetryTests(WebApplicationFactory<Program> factory)
    {
        _factory = factory;
    }

    [Fact]
    public async Task Api_Should_Retry_And_Succeed_On_Transient_Failure()
    {
        // Arrange
        var client = _factory.CreateClient();

        // Act
        var response = await client.GetAsync("/api/test-endpoint-with-retry");

        // Assert
        response.EnsureSuccessStatusCode();
    }
}
```

### Phase 7: Monitoring & Observability

#### 7.1 Add Structured Logging

Enhance logging in retry callbacks:

```csharp
onRetryAsync: async (outcome, timespan, retryAttempt, context) =>
{
    using (_logger.BeginScope(new Dictionary<string, object>
    {
        ["OperationName"] = operationName,
        ["RetryAttempt"] = retryAttempt,
        ["TotalRetries"] = retryCount,
        ["DelayMs"] = timespan.TotalMilliseconds,
        ["StatusCode"] = outcome.Result?.StatusCode,
        ["CorrelationId"] = context.CorrelationId
    }))
    {
        _logger.LogWarning(
            "Retry attempt {RetryAttempt}/{TotalRetries} for operation '{OperationName}'",
            retryAttempt, retryCount, operationName);
    }
}
```

#### 7.2 Add Metrics

```csharp
// Add to your metrics collector
public class RetryMetrics
{
    public static readonly Counter RetryAttempts = Metrics.CreateCounter(
        "retry_attempts_total",
        "Total number of retry attempts",
        new CounterConfiguration
        {
            LabelNames = new[] { "operation", "status" }
        });

    public static readonly Histogram RetryDuration = Metrics.CreateHistogram(
        "retry_duration_seconds",
        "Duration of retry operations",
        new HistogramConfiguration
        {
            LabelNames = new[] { "operation" }
        });
}

// In retry callback
RetryMetrics.RetryAttempts.WithLabels(operationName, statusCode.ToString()).Inc();
```

### Phase 8: Documentation

#### 8.1 Create Developer Guide

Add to your project's documentation:

```markdown
# Retry Policy Guide

## When to Use Retry Policies

✅ **Use retry policies for:**
- External HTTP API calls
- Database operations (deadlocks, transient failures)
- Email sending operations
- File I/O operations
- Any operation that may fail due to transient issues

❌ **Don't use retry policies for:**
- User authentication failures (not transient)
- Validation errors (not transient)
- Business logic errors (not transient)
- Operations that are not idempotent

## How to Integrate

See code examples in Phase 5 of this skill.

## Configuration

Retry behavior is controlled by feature flags in appsettings.json.
Default: 3 retries with 2 second base delay.

## Monitoring

Check application logs for retry warnings:
- Search for "Retry {RetryAttempt}" in logs
- Monitor retry metrics in your observability platform
```

### Phase 9: Rollout Checklist

- [ ] Install NuGet packages
- [ ] Create IRetryPolicyService interface
- [ ] Implement RetryPolicyService
- [ ] Add feature flag configuration to appsettings.json
- [ ] Integrate into HTTP clients
- [ ] Integrate into database operations
- [ ] Integrate into email service
- [ ] Integrate into external API calls
- [ ] Write unit tests
- [ ] Write integration tests
- [ ] Add monitoring/logging
- [ ] Update developer documentation
- [ ] Deploy to staging environment
- [ ] Verify retry behavior in staging
- [ ] Monitor staging for 24 hours
- [ ] Deploy to production
- [ ] Monitor production metrics

### Phase 10: Troubleshooting

#### Common Issues

**Issue 1: Retries not happening**
```
Solution: Check feature flag is enabled in appsettings.json
Verification: Add breakpoint in BuildHttpRetryPolicyAsync method
```

**Issue 2: Too many retries causing delays**
```
Solution: Reduce RetryCount in configuration
Recommendation: Start with 3, adjust based on monitoring
```

**Issue 3: Circuit not breaking on persistent failures**
```
Solution: Consider adding Circuit Breaker policy:
var circuitBreaker = Policy
    .Handle<HttpRequestException>()
    .CircuitBreakerAsync(5, TimeSpan.FromMinutes(1));

var combined = Policy.WrapAsync(retryPolicy, circuitBreaker);
```

**Issue 4: Database connection pool exhaustion**
```
Solution: Use requiresNew: true in UnitOfWork
Ensure proper disposal of connections
```

## Advanced Patterns

### Pattern: Retry + Circuit Breaker + Timeout

```csharp
public async Task<IAsyncPolicy<HttpResponseMessage>> BuildAdvancedHttpPolicyAsync(string operationName)
{
    var timeout = Policy.TimeoutAsync<HttpResponseMessage>(TimeSpan.FromSeconds(30));

    var retry = await BuildHttpRetryPolicyAsync(operationName);

    var circuitBreaker = HttpPolicyExtensions
        .HandleTransientHttpError()
        .CircuitBreakerAsync(
            handledEventsAllowedBeforeBreaking: 5,
            durationOfBreak: TimeSpan.FromSeconds(30));

    // Order matters: timeout -> retry -> circuit breaker
    return Policy.WrapAsync(timeout, retry, circuitBreaker);
}
```

### Pattern: Bulkhead Isolation

```csharp
public IAsyncPolicy<HttpResponseMessage> BuildBulkheadPolicy()
{
    return Policy.BulkheadAsync<HttpResponseMessage>(
        maxParallelization: 10,
        maxQueuingActions: 20,
        onBulkheadRejectedAsync: async context =>
        {
            _logger.LogWarning("Bulkhead rejected execution");
        });
}
```

## Success Metrics

Track these KPIs after implementation:
- **Retry Success Rate**: % of retried operations that eventually succeed
- **Mean Time Between Retries**: Average delay between retry attempts
- **Operations Requiring Retry**: % of total operations that needed retry
- **Retry Exhaustion Rate**: % of operations that failed after all retries

Target: >90% retry success rate, <5% retry exhaustion rate

## References

- [Polly Documentation](https://github.com/App-vNext/Polly)
- [Microsoft Resilience Patterns](https://docs.microsoft.com/en-us/azure/architecture/patterns/retry)
- [Circuit Breaker Pattern](https://martinfowler.com/bliki/CircuitBreaker.html)

## Version History

- v1.0.0 - Initial skill creation with comprehensive retry patterns
- Supports: HTTP, Database, Generic operations
- Includes: Feature flags, Monitoring, Testing

---

**Skill Status**: Production-Ready ✅
**Last Updated**: 2025-12-11
**Maintained By**: DevOps Team
