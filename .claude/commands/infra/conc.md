---
description: Implement concurrent login prevention in ABP Framework with OpenIddict
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
argument-hint: [--dry-run] [--middleware auth|redirect]
model: sonnet
---

# Concurrent Login Prevention Command

Implement concurrent login prevention in ABP Framework. When a user logs in from a new device/browser, all previous sessions are automatically invalidated.

**Arguments**: $ARGUMENTS

## Pre-flight

**Project**: !`basename $(pwd)`
**AuthServer**: !`find api/src -maxdepth 1 -type d -name "*AuthServer" -o -name "*IdentityServer" 2>/dev/null | head -1`
**HttpApi.Host**: !`find api/src -maxdepth 1 -type d -name "*HttpApi.Host" 2>/dev/null | head -1`
**Domain**: !`find api/src -maxdepth 1 -type d -name "*.Domain" ! -name "*Shared" 2>/dev/null | head -1`
**EntityFrameworkCore**: !`find api/src -maxdepth 1 -type d -name "*EntityFrameworkCore" 2>/dev/null | head -1`

Required context:
- Read `CLAUDE.md` for project conventions
- Read `docs/architecture/README.md` for project structure

## Overview

This command implements concurrent login prevention by:
- Generating unique tokens on each login
- Storing tokens in user entity extra properties
- Adding tokens to user claims
- Validating tokens on every request
- Invalidating sessions when token mismatch detected

### How It Works

```
┌─────────┐     ┌─────────────┐     ┌──────────────┐
│ Login   │ →   │ Generate    │ →   │ Store Token  │
│ Request │     │ New Token   │     │ in Database  │
└─────────┘     └─────────────┘     └──────────────┘
                                             ↓
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│ Invalidate  │ ←   │ Token        │ ←   │ Add Token to │
│ Old Session │     │ Mismatch?    │     │ Claims       │
└─────────────┘     └──────────────┘     └──────────────┘
```

## Workflow

```
┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ 1. Create    │ → │ 2. Create    │ → │ 3. Configure │ → │ 4. Configure │
│    Domain    │   │    OpenIddict│   │    AuthServer│   │    API Host  │
└──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘
```

## Execution

### 1. Verify Project Structure

```bash
# Find required projects
DOMAIN=$(find api/src -maxdepth 1 -type d -name "*.Domain" ! -name "*Shared" 2>/dev/null | head -1)
EF_CORE=$(find api/src -maxdepth 1 -type d -name "*EntityFrameworkCore" 2>/dev/null | head -1)
AUTH_SERVER=$(find api/src -maxdepth 1 -type d -name "*AuthServer" -o -name "*IdentityServer" 2>/dev/null | head -1)
API_HOST=$(find api/src -maxdepth 1 -type d -name "*HttpApi.Host" 2>/dev/null | head -1)

# Verify all projects exist
if [ -z "$DOMAIN" ] || [ -z "$EF_CORE" ] || [ -z "$AUTH_SERVER" ] || [ -z "$API_HOST" ]; then
  echo "❌ ERROR: Required projects not found"
  echo "Domain: $DOMAIN"
  echo "EF Core: $EF_CORE"
  echo "AuthServer: $AUTH_SERVER"
  echo "API Host: $API_HOST"
  exit 1
fi

echo "✓ Found all required projects"
```

### 2. Create Domain Constants and Extensions

#### 2.1 Create UserConsts.cs

**Path**: `{Domain}/Constants/UserConsts.cs`

Read project namespace from existing files, then create:

```csharp
namespace {YourProject};

public static class UserConsts
{
    public const string ConcurrentLoginToken = "ConcurrentLoginToken";
}
```

#### 2.2 Create IdentityUserExtensions.cs

**Path**: `{Domain}/Extensions/IdentityUserExtensions.cs`

```csharp
using Volo.Abp.Identity;

namespace {YourProject}.Extensions;

public static class IdentityUserExtensions
{
    private const string ConcurrentLoginTokenKey = "ConcurrentLoginToken";

    public static void SetConcurrentLoginToken(this IdentityUser user, string token)
    {
        user.SetProperty(ConcurrentLoginTokenKey, token);
    }

    public static string? GetConcurrentLoginToken(this IdentityUser user)
    {
        return user.GetProperty<string>(ConcurrentLoginTokenKey);
    }
}
```

**What this does:** Extension methods to store/retrieve the concurrent login token in user's extra properties.

### 3. Create OpenIddict Classes in EntityFrameworkCore

#### 3.1 Create ConcurrentLoginSignInManager.cs

**Path**: `{EntityFrameworkCore}/OpenIddict/ConcurrentLoginSignInManager.cs`

```csharp
using {YourProject}.Extensions;
using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Identity;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using System;
using System.Threading.Tasks;
using Volo.Abp.Identity;
using Volo.Abp.Identity.AspNetCore;
using Volo.Abp.Settings;
using IdentityUser = Volo.Abp.Identity.IdentityUser;

namespace {YourProject}.OpenIddict;

public class ConcurrentLoginSignInManager(
    IdentityUserManager userManager,
    IHttpContextAccessor contextAccessor,
    IUserClaimsPrincipalFactory<IdentityUser> claimsFactory,
    IOptions<IdentityOptions> optionsAccessor,
    ILogger<SignInManager<IdentityUser>> logger,
    IAuthenticationSchemeProvider schemes,
    IUserConfirmation<IdentityUser> confirmation,
    IOptions<AbpIdentityOptions> options,
    ISettingProvider settingProvider)
    : AbpSignInManager(userManager, contextAccessor, claimsFactory, optionsAccessor, logger, schemes, confirmation, options, settingProvider)
{
    public override async Task<SignInResult> PasswordSignInAsync(
        IdentityUser user,
        string password,
        bool isPersistent,
        bool lockoutOnFailure)
    {
        // Generate new unique token on login
        var newToken = Guid.NewGuid().ToString("N");
        user.SetConcurrentLoginToken(newToken);
        await userManager.UpdateAsync(user);

        return await base.PasswordSignInAsync(user, password, isPersistent, lockoutOnFailure);
    }
}
```

**What this does:** Overrides login to generate and store a new token each time.

#### 3.2 Create ConcurrentLoginClaimsPrincipalContributor.cs

**Path**: `{EntityFrameworkCore}/OpenIddict/ConcurrentLoginClaimsPrincipalContributor.cs`

```csharp
using {YourProject}.Constants;
using {YourProject}.Extensions;
using System.Linq;
using System.Security.Claims;
using System.Security.Principal;
using System.Threading.Tasks;
using Volo.Abp.DependencyInjection;
using Volo.Abp.Identity;
using Volo.Abp.Security.Claims;

namespace {YourProject}.OpenIddict;

public class ConcurrentLoginClaimsPrincipalContributor(IdentityUserManager userManager)
    : IAbpClaimsPrincipalContributor, ITransientDependency
{
    public async Task ContributeAsync(AbpClaimsPrincipalContributorContext context)
    {
        var identity = context.ClaimsPrincipal.Identities.FirstOrDefault();
        var userId = identity?.FindUserId();

        if (userId.HasValue)
        {
            var user = await userManager.FindByIdAsync(userId.ToString());
            var token = user?.GetConcurrentLoginToken();

            if (!string.IsNullOrWhiteSpace(token))
            {
                identity.AddClaim(new Claim(UserConsts.ConcurrentLoginToken, token));
            }
        }
    }
}
```

**What this does:** Adds the concurrent login token to user claims.

#### 3.3 Create ConcurrentLoginValidatorAuthMiddleware.cs

**Path**: `{EntityFrameworkCore}/OpenIddict/ConcurrentLoginValidatorAuthMiddleware.cs`

```csharp
using {YourProject}.Constants;
using {YourProject}.Extensions;
using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Identity;
using Microsoft.Extensions.DependencyInjection;
using System.Security.Principal;
using System.Threading.Tasks;
using Volo.Abp.Identity;
using Volo.Abp.Users;

namespace {YourProject}.OpenIddict;

public class ConcurrentLoginValidatorAuthMiddleware(
    RequestDelegate next,
    IdentityUserManager userManager,
    SignInManager<Volo.Abp.Identity.IdentityUser> signInManager)
{
    public async Task InvokeAsync(HttpContext context)
    {
        var currentUser = context.RequestServices.GetRequiredService<ICurrentUser>();

        if (currentUser.IsAuthenticated)
        {
            var userId = context.User?.FindUserId();

            if (userId.HasValue)
            {
                var user = await userManager.FindByIdAsync(userId.Value.ToString());
                var tokenClaim = context.User?.FindFirst(UserConsts.ConcurrentLoginToken)?.Value;

                if (!string.IsNullOrEmpty(tokenClaim))
                {
                    var validToken = user?.GetConcurrentLoginToken();

                    // Token mismatch = user logged in elsewhere
                    if (validToken != tokenClaim)
                    {
                        // Sign out the user
                        await signInManager.SignOutAsync();

                        var authenticationScheme = "Identity.Application";
                        context.Response.Cookies.Delete(authenticationScheme);
                        await context.SignOutAsync();

                        context.Response.StatusCode = StatusCodes.Status401Unauthorized;
                        await context.Response.WriteAsync("Session expired due to concurrent login. Please log in again.");
                        return;
                    }
                }
            }
        }

        await next(context);
    }
}
```

**What this does:** Simple 401 response when token mismatch detected.

#### 3.4 Create ConcurrentLoginValidatorMiddleware.cs

**Path**: `{EntityFrameworkCore}/OpenIddict/ConcurrentLoginValidatorMiddleware.cs`

```csharp
using {YourProject}.Constants;
using {YourProject}.Extensions;
using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using System.Security.Principal;
using System.Threading.Tasks;
using Volo.Abp.Identity;
using Volo.Abp.Users;

namespace {YourProject}.OpenIddict;

public class ConcurrentLoginValidatorMiddleware(
    RequestDelegate next,
    IdentityUserManager userManager,
    IConfiguration configuration)
{
    public async Task InvokeAsync(HttpContext context)
    {
        var currentUser = context.RequestServices.GetRequiredService<ICurrentUser>();

        if (currentUser.IsAuthenticated)
        {
            var userId = context.User?.FindUserId();

            if (userId.HasValue)
            {
                var user = await userManager.FindByIdAsync(userId.Value.ToString());
                var tokenClaim = context.User?.FindFirst(UserConsts.ConcurrentLoginToken)?.Value;

                if (!string.IsNullOrEmpty(tokenClaim))
                {
                    var validToken = user?.GetConcurrentLoginToken();

                    if (validToken != tokenClaim)
                    {
                        var authenticationScheme = "Identity.Application";
                        context.Response.Cookies.Delete(authenticationScheme);
                        await context.SignOutAsync();

                        context.Response.StatusCode = StatusCodes.Status401Unauthorized;
                        await context.Response.WriteAsync("Session expired due to concurrent login. Please log in again.");

                        var authServerUrl = configuration.GetValue<string>("AuthServer:Authority");

                        // Redirect to login page
                        if (!string.IsNullOrEmpty(authServerUrl))
                        {
                            context.Response.Redirect($"{authServerUrl}/Account/Login");
                        }
                        else
                        {
                            context.Response.Redirect("/Account/Login");
                        }

                        return;
                    }
                }
            }
        }

        await next(context);
    }
}
```

**What this does:** Redirects to login page on token mismatch.

### 4. Configure AuthServer Module

**File**: `{AuthServer}/*AuthServerModule.cs` or `*IdentityServerModule.cs`

#### 4.1 Add using statements at top:

```csharp
using {YourProject}.OpenIddict;
using {YourProject}.Constants;
using Microsoft.AspNetCore.Identity;
using System.Security.Claims;
using Volo.Abp.Security.Claims;
```

#### 4.2 Add to `ConfigureServices` method:

```csharp
// Configure Concurrent Login Feature
if (configuration.GetValue<bool>("Features:ConcurrentLogin", false))
{
    // Replace default SignInManager with custom one
    PreConfigure<IdentityBuilder>(builder =>
    {
        builder.AddSignInManager<ConcurrentLoginSignInManager>();
    });

    // Configure security stamp validation
    Configure<SecurityStampValidatorOptions>(options =>
    {
        options.ValidationInterval = TimeSpan.Zero; // Validate on every request
        options.OnRefreshingPrincipal = principalContext =>
        {
            // Preserve the concurrent login token when refreshing claims
            var oldToken = principalContext.CurrentPrincipal.Identities
                .FirstOrDefault()?.Claims
                .FirstOrDefault(c => c.Type == UserConsts.ConcurrentLoginToken);

            if (oldToken != null)
            {
                principalContext.NewPrincipal.Identities
                    .FirstOrDefault()?.AddOrReplace(
                        new Claim(UserConsts.ConcurrentLoginToken, oldToken.Value));
            }

            return Task.CompletedTask;
        };
    });

    // Register services
    context.Services.AddTransient<IAbpClaimsPrincipalContributor, ConcurrentLoginClaimsPrincipalContributor>();
    context.Services.AddTransient<ConcurrentLoginValidatorMiddleware>();
    context.Services.AddTransient<ConcurrentLoginValidatorAuthMiddleware>();
}
```

#### 4.3 Add to `OnApplicationInitialization` method (after UseAuthentication):

```csharp
app.UseAuthentication();
app.UseAbpClaimsMap();

// Add concurrent login middleware
if (configuration.GetValue<bool>("Features:ConcurrentLogin", false))
{
    var middlewareType = configuration.GetValue<string>("Features:ConcurrentLoginMiddleware", "redirect");

    if (middlewareType == "auth")
    {
        // Option 1: Simple 401 response
        app.UseMiddleware<ConcurrentLoginValidatorAuthMiddleware>();
    }
    else
    {
        // Option 2: Redirect to login (default)
        app.UseMiddleware<ConcurrentLoginValidatorMiddleware>();
    }
}

app.UseAuthorization();
```

#### 4.4 Update `appsettings.json`:

```json
{
  "Features": {
    "ConcurrentLogin": true,
    "ConcurrentLoginMiddleware": "redirect"
  },
  "AuthServer": {
    "Authority": "https://localhost:44300"
  }
}
```

### 5. Configure HttpApi.Host Module

**File**: `{HttpApi.Host}/*HttpApiHostModule.cs`

#### 5.1 Add using statements:

```csharp
using {YourProject}.OpenIddict;
using {YourProject}.Constants;
using Microsoft.AspNetCore.Identity;
using System.Security.Claims;
using Volo.Abp.Security.Claims;
```

#### 5.2 Add to `ConfigureServices` method:

```csharp
// Configure Concurrent Login Feature
if (configuration.GetValue<bool>("Features:ConcurrentLogin", false))
{
    Configure<SecurityStampValidatorOptions>(options =>
    {
        options.ValidationInterval = TimeSpan.Zero;
        options.OnRefreshingPrincipal = principalContext =>
        {
            var oldToken = principalContext.CurrentPrincipal.Identities
                .FirstOrDefault()?.Claims
                .FirstOrDefault(c => c.Type == UserConsts.ConcurrentLoginToken);

            if (oldToken != null)
            {
                principalContext.NewPrincipal.Identities
                    .FirstOrDefault()?.AddOrReplace(
                        new Claim(UserConsts.ConcurrentLoginToken, oldToken.Value));
            }

            return Task.CompletedTask;
        };
    });

    context.Services.AddTransient<IAbpClaimsPrincipalContributor, ConcurrentLoginClaimsPrincipalContributor>();
    context.Services.AddTransient<ConcurrentLoginValidatorAuthMiddleware>();
}
```

#### 5.3 Add to `OnApplicationInitialization` method (after UseAuthentication):

```csharp
app.UseAuthentication();
app.UseAbpClaimsMap();

// Add concurrent login middleware for API
if (configuration.GetValue<bool>("Features:ConcurrentLogin", false))
{
    app.UseMiddleware<ConcurrentLoginValidatorAuthMiddleware>();
}

app.UseAuthorization();
```

#### 5.4 Update `appsettings.json`:

```json
{
  "Features": {
    "ConcurrentLogin": true
  }
}
```

## Options

| Option | Effect |
|--------|--------|
| `--dry-run` | Show what would be changed without making changes |
| `--middleware auth` | Use simple 401 response (default) |
| `--middleware redirect` | Use redirect to login page |

## Testing

### Enable the Feature

Update both `appsettings.json` files (AuthServer and HttpApi.Host):

```json
{
  "Features": {
    "ConcurrentLogin": true
  }
}
```

### Test Scenario

1. **Open Browser A**
   - Navigate to login page
   - Login as `admin` / `password`
   - Note: Token `abc123` generated and stored

2. **Open Browser B** (private/incognito)
   - Navigate to login page
   - Login as same user: `admin` / `password`
   - Note: Token `xyz789` generated (overwrites `abc123`)

3. **Go back to Browser A**
   - Try to access any protected page/API
   - Expected: Session invalidated, redirected to login (or 401)
   - Reason: Token mismatch (`abc123` != `xyz789`)

### Manual Testing Commands

```bash
# Terminal 1: Login and get token
TOKEN1=$(curl -X POST https://localhost:44300/connect/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=password&username=admin&password=1q2w3E*&client_id=YourApp_App" \
  | jq -r '.access_token')

echo "Token 1: $TOKEN1"

# Terminal 2: Login again (same user) - invalidates Token 1
TOKEN2=$(curl -X POST https://localhost:44300/connect/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=password&username=admin&password=1q2w3E*&client_id=YourApp_App" \
  | jq -r '.access_token')

echo "Token 2: $TOKEN2"

# Try using Token 1 (should fail with 401)
curl -X GET https://localhost:44301/api/app/users \
  -H "Authorization: Bearer $TOKEN1" \
  -v

# Try using Token 2 (should work)
curl -X GET https://localhost:44301/api/app/users \
  -H "Authorization: Bearer $TOKEN2" \
  -v
```

## Build Verification

```bash
# Build all projects
dotnet build api/*.slnx

# Run AuthServer
dotnet run --project api/src/*AuthServer/

# Run API Host (in another terminal)
dotnet run --project api/src/*HttpApi.Host/

# Check logs for:
# "Concurrent login prevention enabled"
```

## Output Summary

```
## Concurrent Login Prevention Configured

### Files Created

**Domain Layer:**
- {Domain}/Constants/UserConsts.cs
- {Domain}/Extensions/IdentityUserExtensions.cs

**EntityFrameworkCore Layer:**
- {EntityFrameworkCore}/OpenIddict/ConcurrentLoginSignInManager.cs
- {EntityFrameworkCore}/OpenIddict/ConcurrentLoginClaimsPrincipalContributor.cs
- {EntityFrameworkCore}/OpenIddict/ConcurrentLoginValidatorAuthMiddleware.cs
- {EntityFrameworkCore}/OpenIddict/ConcurrentLoginValidatorMiddleware.cs

### Files Modified
- {AuthServer}/*AuthServerModule.cs
- {AuthServer}/appsettings.json
- {HttpApi.Host}/*HttpApiHostModule.cs
- {HttpApi.Host}/appsettings.json

### Configuration
- **Feature Enabled**: Yes (Features:ConcurrentLogin)
- **Middleware Type**: {auth|redirect}
- **Token Validation**: On every request
- **Session Behavior**: Single session per user

### How It Works
1. User logs in → New token generated
2. Token stored in database (user extra properties)
3. Token added to user claims
4. Every request validates token
5. Token mismatch → Session invalidated

### Next Steps
1. Restart AuthServer and API Host
2. Test with multiple browsers/devices
3. Verify old sessions are invalidated
4. Monitor user experience for session timeouts
5. Consider adding user notification of concurrent login
```

## Checkpoint

- [ ] Domain constants and extensions created
- [ ] OpenIddict classes created in EF Core
- [ ] AuthServer module configured
- [ ] HttpApi.Host module configured
- [ ] appsettings.json files updated
- [ ] Build succeeds without errors
- [ ] Can login successfully
- [ ] Second login invalidates first session
- [ ] Proper error message shown

## Troubleshooting

### Build errors about namespace

**Problem**: `The type or namespace name 'UserConsts' could not be found`

**Solution**:
```bash
# Ensure project references are correct
dotnet add api/src/*EntityFrameworkCore/ reference api/src/*Domain/
```

### Tokens not invalidating

**Checklist**:
- [ ] Feature flag enabled in both appsettings.json
- [ ] Middleware registered after UseAuthentication
- [ ] SecurityStampValidatorOptions.ValidationInterval = TimeSpan.Zero
- [ ] Claims contributor registered
- [ ] User extra properties updated in database

### Claims not containing token

**Problem**: Token not in claims

**Debug**:
```csharp
// Add logging in ConcurrentLoginClaimsPrincipalContributor
Logger.LogInformation("Token from DB: {Token}", token);
Logger.LogInformation("Claims: {Claims}", string.Join(", ", identity.Claims.Select(c => $"{c.Type}={c.Value}")));
```

### Sessions not expiring immediately

**Problem**: Old session still works for some time

**Cause**: Security stamp validation interval

**Solution**: Already set to `TimeSpan.Zero` in configuration

## Security Considerations

⚠️ **IMPORTANT**: This feature has security and UX implications.

### Pros
- ✅ Prevents session hijacking across devices
- ✅ Ensures only one active session per user
- ✅ Immediate invalidation on new login

### Cons
- ⚠️ Users may be logged out unexpectedly
- ⚠️ Shared accounts become problematic
- ⚠️ API calls on every request (check DB for token)

### Recommendations

1. **User Notification**: Notify users when their session is terminated
2. **Graceful UX**: Show clear message and easy re-login
3. **Exceptions**: Consider whitelisting certain user roles
4. **Monitoring**: Track concurrent login events
5. **Performance**: Cache tokens in Redis for high-traffic apps

### Performance Optimization

For high-traffic applications, consider caching tokens:

```csharp
// In ConcurrentLoginValidatorAuthMiddleware
// Use IDistributedCache to cache tokens
var cachedToken = await cache.GetStringAsync($"user:{userId}:token");
if (cachedToken == null)
{
    var user = await userManager.FindByIdAsync(userId.Value.ToString());
    cachedToken = user?.GetConcurrentLoginToken();
    await cache.SetStringAsync($"user:{userId}:token", cachedToken,
        new DistributedCacheEntryOptions { AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(5) });
}
```

## Advanced Configuration

### Allow Multiple Sessions for Admin Role

Add role check in middleware:

```csharp
public async Task InvokeAsync(HttpContext context)
{
    var currentUser = context.RequestServices.GetRequiredService<ICurrentUser>();

    if (currentUser.IsAuthenticated)
    {
        // Skip validation for admin role
        if (currentUser.IsInRole("admin"))
        {
            await next(context);
            return;
        }

        // Continue with token validation...
    }

    await next(context);
}
```

### Notify User of Concurrent Login

Emit event when token mismatch detected:

```csharp
// In middleware, before signing out
await eventBus.PublishAsync(new ConcurrentLoginDetectedEvent
{
    UserId = userId.Value,
    OldToken = tokenClaim,
    NewToken = validToken,
    IpAddress = context.Connection.RemoteIpAddress?.ToString()
});
```

### Store Device Information

Extend token storage to include device info:

```csharp
public static void SetConcurrentLoginToken(this IdentityUser user, string token, string deviceInfo)
{
    user.SetProperty("ConcurrentLoginToken", token);
    user.SetProperty("ConcurrentLoginDevice", deviceInfo);
    user.SetProperty("ConcurrentLoginTime", DateTime.UtcNow);
}
```

## References

- [ABP Identity Documentation](https://docs.abp.io/en/abp/latest/Modules/Identity)
- [ASP.NET Core Identity](https://learn.microsoft.com/en-us/aspnet/core/security/authentication/identity)
- [OpenIddict Documentation](https://documentation.openiddict.com/)
- [Claims-based Authorization](https://learn.microsoft.com/en-us/aspnet/core/security/authorization/claims)
