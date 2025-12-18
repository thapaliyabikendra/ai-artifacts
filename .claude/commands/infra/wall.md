---
description: Implement IP rate limiting with Redis in ABP AuthServer
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
argument-hint: [--dry-run] [--redis-host <host:port>]
model: sonnet
---

# Rate Limiting (Wall) Command

Implement IP-based rate limiting using AspNetCoreRateLimit and Redis distributed cache in the ABP Framework AuthServer.

**Arguments**: $ARGUMENTS

## Pre-flight

**Project**: !`basename $(pwd)`
**AuthServer Module**: !`find api/src -maxdepth 1 -type d -name "*AuthServer" 2>/dev/null | head -1`

Required context:
- Read `CLAUDE.md` for project conventions
- Read `docs/architecture/README.md` for project paths

## Overview

This command implements distributed rate limiting to protect your AuthServer from abuse and DoS attacks by:
- Limiting requests per IP address
- Configuring endpoint-specific limits
- Using Redis for distributed caching across multiple instances
- Providing 429 (Too Many Requests) responses when limits are exceeded

## Workflow

```
┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ 1. Verify    │ → │ 2. Install   │ → │ 3. Configure │ → │ 4. Update    │
│    Setup     │   │    Packages  │   │    Module    │   │    Settings  │
└──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘
```

## Execution

### 1. Verify AuthServer exists

```bash
# Find AuthServer project
AUTH_SERVER=$(find api/src -maxdepth 1 -type d -name "*AuthServer" 2>/dev/null | head -1)

if [ -z "$AUTH_SERVER" ]; then
  echo "❌ ERROR: AuthServer project not found in api/src/"
  echo "Expected: api/src/{ProjectName}.AuthServer/"
  exit 1
fi

echo "✓ Found AuthServer: $AUTH_SERVER"
```

### 2. Install required NuGet packages

```bash
# Navigate to AuthServer project
cd "$AUTH_SERVER"

# Install AspNetCoreRateLimit
dotnet add package AspNetCoreRateLimit

# Install Redis support
dotnet add package AspNetCoreRateLimit.Redis

# Install StackExchange.Redis if not already present
dotnet add package StackExchange.Redis

cd ../../..
```

### 3. Configure HostModule

**File**: `{AuthServer}/ClinicManagementSystemAuthServerModule.cs` (or similar)

**Add using statements** at the top of the file:
```csharp
using AspNetCoreRateLimit;
using StackExchange.Redis;
```

**Add rate limiting configuration** in `ConfigureServices` method:
```csharp
// Rate Limiting Configuration
if (configuration.GetValue<bool>("Features:RateLimiting", false))
{
    context.Services.AddOptions();
    context.Services.Configure<IpRateLimitOptions>(configuration.GetSection("IpRateLimiting"));
    context.Services.AddSingleton<IRateLimitConfiguration, RateLimitConfiguration>();
    context.Services.AddSingleton<IIpPolicyStore, DistributedCacheIpPolicyStore>();

    // Configure Redis connection
    var redisOptions = ConfigurationOptions.Parse(configuration["Redis:Configuration"]);
    context.Services.AddSingleton<IConnectionMultiplexer>(provider =>
        ConnectionMultiplexer.Connect(redisOptions));

    // Add Redis rate limiting
    context.Services.AddRedisRateLimiting();
}
```

**Add middleware** in `OnApplicationInitialization` method (before `app.UseRouting()`):
```csharp
// Add rate limiting middleware (must be before UseRouting)
if (app.ApplicationServices.GetService<IIpPolicyStore>() != null)
{
    app.UseIpRateLimiting();
}
```

### 4. Update appsettings.json

**File**: `{AuthServer}/appsettings.json`

**Add configuration**:
```json
{
  "Features": {
    "RateLimiting": true
  },
  "Redis": {
    "Configuration": "localhost:6379"
  },
  "IpRateLimiting": {
    "EnableEndpointRateLimiting": true,
    "StackBlockedRequests": false,
    "HttpStatusCode": 429,
    "RealIpHeader": "X-Real-IP",
    "ClientIdHeader": "X-ClientId",
    "GeneralRules": [
      {
        "Endpoint": "*",
        "Period": "1m",
        "Limit": 100
      },
      {
        "Endpoint": "*",
        "Period": "1h",
        "Limit": 1000
      },
      {
        "Endpoint": "POST:/connect/token",
        "Period": "1m",
        "Limit": 10
      },
      {
        "Endpoint": "POST:/api/account/register",
        "Period": "1h",
        "Limit": 5
      }
    ]
  }
}
```

### 5. Add environment-specific overrides (optional)

**File**: `{AuthServer}/appsettings.Production.json`

```json
{
  "Redis": {
    "Configuration": "your-production-redis-host:6379,password=your-redis-password,ssl=true"
  },
  "IpRateLimiting": {
    "GeneralRules": [
      {
        "Endpoint": "*",
        "Period": "1m",
        "Limit": 200
      },
      {
        "Endpoint": "*",
        "Period": "1h",
        "Limit": 2000
      }
    ]
  }
}
```

## Configuration Reference

### Rate Limit Periods

| Period | Format | Description |
|--------|--------|-------------|
| Per second | `1s` | Limit per second |
| Per minute | `1m` | Limit per minute |
| Per hour | `1h` | Limit per hour |
| Per day | `1d` | Limit per day |

### Endpoint Patterns

| Pattern | Matches |
|---------|---------|
| `*` | All endpoints |
| `GET:*` | All GET requests |
| `POST:*` | All POST requests |
| `*/api/*` | All API endpoints |
| `POST:/connect/token` | Specific OAuth token endpoint |
| `GET:/api/users/{id}` | Specific endpoint with route parameter |

### Common Rate Limits

| Endpoint | Suggested Limit | Reason |
|----------|----------------|--------|
| `POST:/connect/token` | 10/min | Prevent brute force login |
| `POST:/api/account/register` | 5/hour | Prevent spam registration |
| `POST:/api/password/reset` | 3/hour | Prevent abuse |
| `GET:*` | 100/min | General read operations |
| `POST:*` | 50/min | General write operations |

## Testing

### Test rate limiting is working:

```bash
# Make multiple requests to trigger rate limit
for i in {1..15}; do
  curl -X POST https://localhost:44300/connect/token \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "grant_type=client_credentials&client_id=test&client_secret=test"
  echo "\nRequest $i"
done

# Should see 429 (Too Many Requests) after limit exceeded
```

### Check Redis keys:

```bash
# Connect to Redis CLI
redis-cli

# List all rate limit keys
KEYS "AspNetCoreRateLimit:*"

# Check specific key value
GET "AspNetCoreRateLimit:192.168.1.100:POST:/connect/token:1m"
```

## Options

| Option | Effect |
|--------|--------|
| `--dry-run` | Show what would be changed without making changes |
| `--redis-host <host:port>` | Override Redis host (default: localhost:6379) |
| `--disable-endpoint-limiting` | Use general rate limiting only |
| `--status-code <code>` | HTTP status code for blocked requests (default: 429) |

## Build Verification

```bash
# Build AuthServer
dotnet build api/src/*AuthServer/*.csproj

# Run AuthServer (requires Redis running)
dotnet run --project api/src/*AuthServer/

# Verify Redis connection in logs
# Look for: "Rate limiting enabled with Redis"
```

## Output Summary

```
## Rate Limiting Configured

### Packages Installed
- AspNetCoreRateLimit (v5.x)
- AspNetCoreRateLimit.Redis (v1.x)
- StackExchange.Redis (v2.x)

### Files Modified
- {AuthServer}/ClinicManagementSystemAuthServerModule.cs (or similar)
- {AuthServer}/appsettings.json
- {AuthServer}/*.csproj (package references)

### Configuration
- **Feature Enabled**: Yes (Features:RateLimiting)
- **Redis Host**: {redis-host}
- **General Limit**: 100 requests/min, 1000 requests/hour
- **Token Endpoint**: 10 requests/min
- **Registration**: 5 requests/hour
- **HTTP Status**: 429 (Too Many Requests)

### Rate Limit Rules Applied
{list configured rules}

### Next Steps
1. Ensure Redis is running: `docker run -d -p 6379:6379 redis:latest`
2. Test rate limiting with multiple requests
3. Monitor Redis keys for rate limit counters
4. Adjust limits based on production traffic patterns
5. Consider adding whitelist for trusted IPs
```

## Checkpoint

- [ ] AuthServer project located
- [ ] NuGet packages installed successfully
- [ ] Module configured with rate limiting services
- [ ] Middleware added to request pipeline
- [ ] appsettings.json updated with rate limit rules
- [ ] Redis connection string configured
- [ ] Build succeeds without errors
- [ ] Redis is running and accessible
- [ ] Rate limiting triggers 429 responses when exceeded

## Troubleshooting

### Redis connection fails
```bash
# Check Redis is running
docker ps | grep redis

# Start Redis if not running
docker run -d -p 6379:6379 --name redis redis:latest

# Test connection
redis-cli ping
# Should return: PONG
```

### Rate limiting not working
- Verify `Features:RateLimiting` is set to `true`
- Check middleware order (UseIpRateLimiting before UseRouting)
- Check Redis connection string is correct
- View logs for rate limiting errors
- Verify `IpRateLimitOptions` configuration is loaded

### Wrong IP address logged
- Check reverse proxy configuration
- Set `RealIpHeader` to match proxy header (e.g., "X-Forwarded-For")
- Ensure proxy forwards client IP correctly

## Security Notes

⚠️ **IMPORTANT**: Rate limiting is a defense-in-depth measure, not a complete security solution.

- **Use HTTPS**: Always use TLS in production
- **Whitelist trusted IPs**: Add internal/monitoring IPs to whitelist
- **Monitor logs**: Track blocked requests for attack patterns
- **Adjust limits**: Start conservative, increase based on real usage
- **Distributed cache**: Redis ensures limits work across multiple server instances
- **Client identification**: Consider using authenticated user IDs instead of just IPs

## Advanced Configuration

### Whitelist specific IPs

```json
{
  "IpRateLimiting": {
    "IpWhitelist": [ "127.0.0.1", "::1", "192.168.1.0/24" ],
    "ClientWhitelist": [ "trusted-client-id" ]
  }
}
```

### Custom response

```json
{
  "IpRateLimiting": {
    "QuotaExceededResponse": {
      "Content": "{{ \"error\": \"Rate limit exceeded. Retry after {0} seconds\" }}",
      "ContentType": "application/json"
    }
  }
}
```

### Per-client limits

```json
{
  "IpRateLimiting": {
    "ClientRules": [
      {
        "ClientId": "premium-client",
        "Endpoint": "*",
        "Period": "1m",
        "Limit": 1000
      }
    ]
  }
}
```

## References

- [AspNetCoreRateLimit Documentation](https://github.com/stefanprodan/AspNetCoreRateLimit)
- [Redis Documentation](https://redis.io/docs/)
- [ABP Framework - Custom Middleware](https://docs.abp.io/en/abp/latest/AspNetCore-Middleware)
- [OWASP Rate Limiting](https://owasp.org/www-community/controls/Blocking_Brute_Force_Attacks)
