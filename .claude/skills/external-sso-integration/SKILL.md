# External SSO Login Integration Skill

## Overview

This skill generates **production-ready C# code** to add OpenID Connect external SSO login to your ABP Framework AuthServer module. It follows ABP best practices and is reusable across any ABP project.

**What this skill does:**
- ✅ Generates `ConfigureExternalAuthentication()` method code
- ✅ Adds method call to `ConfigureServices()`
- ✅ Handles SSL bypass for dev/staging
- ✅ Supports custom scopes
- ✅ Includes proper logout handling
- ✅ Feature flag controlled

**What this skill does NOT do:**
- ❌ Modify appsettings.json (you'll add your own configuration keys)
- ❌ Assume any specific provider (Google, Microsoft, etc.)
- ❌ Add UI components (your existing login page will automatically show external login button if configured)

## Usage

```bash
/external-sso-login-integration [options]
```

### Options

**Configuration Keys (customize these to match your appsettings structure):**
- `--config-section <name>` - Configuration section name (default: `ExternalSsoLogin`)
- `--authority-key <key>` - Config key for authority URL (default: `Authority`)
- `--client-id-key <key>` - Config key for client ID (default: `ClientId`)
- `--client-secret-key <key>` - Config key for client secret (default: `ClientSecret`)
- `--bypass-ssl-key <key>` - Config key for SSL bypass flag (default: `ByPassSSL`)
- `--redirect-uri-key <key>` - Config key for redirect URI (default: `RedirectUri`)

**Feature Flag:**
- `--feature-flag <name>` - Feature flag identifier (default: `Authentication.OpenIDConnect`)
- `--auto-enable` - Add code to auto-enable feature flag (for testing)

**Scopes:**
- `--scopes <list>` - Comma-separated list of OIDC scopes (default: `openid,profile,email,role`)
- `--custom-scopes <list>` - Additional custom scopes (e.g., `ncell_scheduler_stg`)

**Code Generation:**
- `--method-name <name>` - Name of the configuration method (default: `ConfigureExternalAuthentication`)
- `--insert-location <line>` - Insert method call at specific line number (default: find best location)
- `--dry-run` - Preview code without modifying files
- `--backup` - Create backup before modifications

### Examples

```bash
# Standard OIDC integration (generic)
/external-sso-login-integration \
  --config-section ExternalSsoLogin \
  --feature-flag Authentication.OpenIDConnect

# Custom configuration keys
/external-sso-login-integration \
  --config-section OpenIdConnect \
  --authority-key OidcAuthority \
  --client-id-key ClientIdentifier \
  --scopes "openid,profile,email,roles"

# With custom scopes (like NCell)
/external-sso-login-integration \
  --custom-scopes "ncell_scheduler_stg,permissions" \
  --auto-enable

# Preview only
/external-sso-login-integration --dry-run
```

## Generated Code

The skill generates two code additions to your `AuthServerModule.cs`:

### 1. New Method: `ConfigureExternalAuthentication()`

```csharp
private void ConfigureExternalAuthentication(ServiceConfigurationContext context, IConfiguration configuration)
{
    var hostingEnvironment = context.Services.GetHostingEnvironment();
    var enableOpenIdConnect = IsFeatureEnabled(configuration, "Authentication.OpenIDConnect");

    if (!enableOpenIdConnect)
    {
        Console.WriteLine("[SSO] OpenID Connect is disabled");
        return;
    }

    Console.WriteLine("[SSO] Configuring OpenID Connect authentication");

    // Read configuration (customize these keys to match your appsettings.json)
    var authority = configuration["ExternalSsoLogin:Authority"]?.TrimEnd('/');
    var clientId = configuration["ExternalSsoLogin:ClientId"];
    var clientSecret = configuration["ExternalSsoLogin:ClientSecret"];
    var bypassSSL = configuration.GetValue<bool>("ExternalSsoLogin:ByPassSSL", false);
    var redirectUri = configuration["ExternalSsoLogin:RedirectUri"] ?? "/Account/Login";

    if (string.IsNullOrWhiteSpace(authority))
        throw new InvalidOperationException("ExternalSsoLogin:Authority is missing");

    if (string.IsNullOrWhiteSpace(clientId))
        throw new InvalidOperationException("ExternalSsoLogin:ClientId is missing");

    var isDevOrBypass = hostingEnvironment.IsDevelopment() || bypassSSL;

    Console.WriteLine($"[SSO] Authority: {authority}");

    context.Services.AddAuthentication()
        .AddOpenIdConnect(OpenIdConnectDefaults.AuthenticationScheme, options =>
        {
            options.Authority = authority;
            options.ClientId = clientId;
            options.ClientSecret = clientSecret;

            options.ResponseType = OpenIdConnectResponseType.CodeIdToken;
            options.UsePkce = true;
            options.SaveTokens = true;
            options.GetClaimsFromUserInfoEndpoint = true;
            options.SignedOutRedirectUri = redirectUri;

            options.Scope.Clear();
            options.Scope.Add("openid");
            options.Scope.Add("profile");
            options.Scope.Add("email");
            options.Scope.Add("role");
            // Add custom scopes here if needed
            // options.Scope.Add("your_custom_scope");

            // SSL bypass for dev/staging environments (DANGEROUS in production!)
            if (isDevOrBypass)
            {
                var handler = new HttpClientHandler
                {
                    ServerCertificateCustomValidationCallback = HttpClientHandler.DangerousAcceptAnyServerCertificateValidator
                };
                options.Backchannel = new HttpClient(handler);
            }

            options.RequireHttpsMetadata = !isDevOrBypass;

            // Validate issuer matches authority
            options.TokenValidationParameters = new TokenValidationParameters
            {
                NameClaimType = "name",
                RoleClaimType = "role",
                ValidIssuer = options.Authority,
            };

            // Proper logout handling
            options.Events = new OpenIdConnectEvents
            {
                OnRedirectToIdentityProviderForSignOut = async context =>
                {
                    var result = await context.HttpContext.AuthenticateAsync(OpenIdConnectDefaults.AuthenticationScheme);
                    var idToken = result.Properties?.GetTokenValue(OpenIdConnectParameterNames.IdToken);
                    if (!string.IsNullOrEmpty(idToken))
                    {
                        context.ProtocolMessage.IdTokenHint = idToken;
                    }
                }
            };
        });

    if (hostingEnvironment.IsDevelopment())
    {
        Microsoft.IdentityModel.Logging.IdentityModelEventSource.ShowPII = true;
    }

    Console.WriteLine("[SSO] OpenID Connect configured successfully");
}
```

**Key features:**
- Feature flag controlled (disable/enable without recompiling)
- SSL validation bypass for development (`ByPassSSL` flag)
- PKCE enabled for security
- Token issuer validation
- Proper logout with id_token_hint
- Development PII logging for debugging

---

### 2. Update `ConfigureServices()` to Call New Method

```csharp
public override void ConfigureServices(ServiceConfigurationContext context)
{
    var configuration = context.Services.GetConfiguration();

    // ... existing configuration code ...

    ConfigureHealthChecks(context, configuration);
    ConfigureRateLimiting(context, configuration);
    ConfigureCookies(context, configuration);
    ConfigureExternalAuthentication(context, configuration); // ← ADD THIS LINE

    context.Services.AddTransient<ITokenManagementAppService, TokenManagementAppService>();
}
```

---

## Customization Guide

### Step 1: Update Configuration Keys

The generated code uses these config keys (customize with `--config-section` and related options):

```csharp
var authority = configuration["ExternalSsoLogin:Authority"];
var clientId = configuration["ExternalSsoLogin:ClientId"];
var clientSecret = configuration["ExternalSsoLogin:ClientSecret"];
var bypassSSL = configuration.GetValue<bool>("ExternalSsoLogin:ByPassSSL", false);
var redirectUri = configuration["ExternalSsoLogin:RedirectUri"] ?? "/Account/Login";
```

**To use custom keys**, run the skill with options:
```bash
/external-sso-login-integration \
  --config-section OpenIdConnect \
  --authority-key OidcAuthority \
  --client-id-key ClientId \
  --client-secret-key ClientSecret \
  --bypass-ssl-key AllowInvalidCertificates \
  --redirect-uri-key PostLogoutRedirectUri
```

Would generate:
```csharp
var authority = configuration["OpenIdConnect:OidcAuthority"];
var clientId = configuration["OpenIdConnect:ClientId"];
var clientSecret = configuration["OpenIdConnect:ClientSecret"];
var bypassSSL = configuration.GetValue<bool>("OpenIdConnect:AllowInvalidCertificates", false);
var redirectUri = configuration["OpenIdConnect:PostLogoutRedirectUri"] ?? "/Account/Login";
```

### Step 2: Add Custom Scopes

Default scopes: `openid,profile,email,role`

To add custom scopes (like `ncell_scheduler_stg`):

**Option A:** Use `--custom-scopes` flag:
```bash
/external-sso-login-integration --custom-scopes "ncell_scheduler_stg,permissions"
```

Generates:
```csharp
options.Scope.Add("ncell_scheduler_stg");
options.Scope.Add("permissions");
```

**Option B:** Manually edit after generation:
```csharp
options.Scope.Add("ncell_scheduler_stg");  // ← Add your custom scope here
```

### Step 3: Add Your appsettings.json Configuration

**This is your responsibility.** Add a section to your `appsettings.json` (or environment-specific config) with your OIDC provider details:

```json
{
  "ExternalSsoLogin": {
    "Authority": "https://login.your-company.com/oauth2/default",
    "ClientId": "your-client-id",
    "ClientSecret": "your-client-secret",
    "ByPassSSL": false,
    "RedirectUri": "/Account/Login"
  },
  "FeatureManagement": {
    "FeatureFlags": [
      {
        "id": "Authentication.OpenIDConnect",
        "enabled": false
      }
    ]
  }
}
```

**For production:**
- Use environment variables: `ExternalSsoLogin__ClientSecret=actual-secret`
- Use user secrets for development: `dotnet user-secrets set "ExternalSsoLogin:ClientSecret" "secret"`
- Use Azure Key Vault / HashiCorp Vault for production secrets

### Step 4: Enable Feature Flag

Set `"Authentication.OpenIDConnect"` to `true` in your feature flags (appsettings.features.json or FeatureManagement table).

---

## Implementation Details

### Modified Files

The skill modifies **only one file**: `{ProjectName}.AuthServer/{ProjectName}AuthServerModule.cs`

**If the file doesn't exist** (your AuthServer has a different name), use `--module` flag:
```bash
/external-sso-login-integration --module src/MyApp/Auth/MyAuthModule.cs
```

### Insertion Logic

The skill:
1. Finds the `ConfigureServices` method
2. Inserts call to `ConfigureExternalAuthentication()` at the end of existing configuration calls (before `AddTransient<ITokenManagementAppService>` or similar)
3. Adds the new method after `ConfigureRateLimiting()` or at end of class (respecting existing method order)
4. Preserves existing code formatting and style

### Dependencies

The generated code requires these namespaces (already present in typical AuthServer modules):

```csharp
using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Authentication.OpenIdConnect;
using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.Configuration;
using Microsoft.IdentityModel.Protocols.OpenIdConnect;
using Microsoft.IdentityModel.Tokens;
using Microsoft.IdentityModel.Logging;  // Optional (dev only)
```

If missing, the skill will add them at the top of the file.

---

## Reusability Across Projects

### Project A: Simple OIDC

```bash
# Generate code with default settings
/external-sso-login-integration --dry-run
# Review, then apply
/external-sso-login-integration --backup
```

Add to appsettings.json manually:
```json
{
  "ExternalSsoLogin": {
    "Authority": "https://login.company-a.com/oauth2/default",
    "ClientId": "company-a-client",
    "ClientSecret": "..."
  }
}
```

### Project B: Different Config Keys

```bash
/external-sso-login-integration \
  --config-section OpenIdConnect \
  --authority-key IssuerUrl \
  --client-id-key OidcClientId \
  --client-secret-key OidcClientSecret \
  --scopes "openid,profile,email" \
  --backup
```

Add custom config:
```json
{
  "OpenIdConnect": {
    "IssuerUrl": "https://auth.company-b.com/oauth",
    "OidcClientId": "client-id",
    "OidcClientSecret": "secret",
    "AllowInvalidSsl": true
  }
}
```

---

## Code-Only Philosophy

This skill **only generates C# code**. Why?

1. **You control your configuration** - Different projects have different config structures (some use `ExternalAuth:Google`, others use `SSO:Settings`, etc.)
2. **Security** - You manage secrets (client secrets should never be in generated code samples)
3. **Flexibility** - Use environment variables, Azure Key Vault, user secrets - your choice
4. **No assumptions** - Your project might already have an `ExternalAuth` section with different keys
5. **Cleaner git diffs** - Code changes tracked separately from config changes

---

## What You Need to Do After Running the Skill

1. **Review generated code** (in `AuthServerModule.cs`)
2. **Add your configuration** to `appsettings.json`:
   - Choose your config section name
   - Add `Authority`, `ClientId`, `ClientSecret`, `ByPassSSL`, `RedirectUri` keys
3. **Enable feature flag** `Authentication.OpenIDConnect`
4. **Test the flow**:
   - Run AuthServer
   - Go to `/Account/Login`
   - You should see external login button
   - Click → redirect to IdP → back to app
5. **Configure your IdP** with correct redirect URI: `https://yourapp.com/signin-oidc`

---

## Configuration Flexibility

The generated code uses `configuration["ExternalSsoLogin:Authority"]` by default. But you can customize:

**Example 1: Nested config**
```json
{
  "Authentication": {
    "External": {
      "ProviderUrl": "...",
      "AppClientId": "..."
    }
  }
}
```
Use flags:
```bash
/external-sso-login-integration \
  --config-section "Authentication:External" \
  --authority-key ProviderUrl \
  --client-id-key AppClientId
```

**Example 2: Environment variables only**
```bash
export OIDC_AUTHORITY=https://login.company.com
export OIDC_CLIENT_ID=abc123
export OIDC_CLIENT_SECRET=secret
```
Code generated with:
```bash
/external-sso-login-integration \
  --config-section "" \
  --authority-key OIDC_AUTHORITY \
  --client-id-key OIDC_CLIENT_ID \
  --client-secret-key OIDC_CLIENT_SECRET
```
(NOTE: empty config section reads from root)

---

## Troubleshooting

### "Method already exists"
**Cause:** `ConfigureExternalAuthentication()` already defined in module.
**Fix:** Use `--method-name` to use different name, or manually merge code.

### "Unable to find insertion point in ConfigureServices()"
**Cause:** Module structure different from expected pattern.
**Fix:** Use `--insert-location` with line number, or manually add method call.

### "External login button not showing"
**Cause:** ABP UI needs external auth schemes registered before `AddIdentity()`.
**Fix:** Ensure `AddAuthentication().AddOpenIdConnect()` is in `ConfigureServices()` **before** `AddIdentity()` (typical ABP pattern).

### "No authentication handler for scheme 'OpenIdConnect'"
**Cause:** `AddOpenIdConnect()` not called (feature flag might be off).
**Fix:** Check logs for `[SSO] OpenID Connect isdisabled`. Enable feature flag.

---

## Code Review Checklist

After running the skill, verify:

- [ ] `ConfigureExternalAuthentication()` method added
- [ ] Method signature matches: `private void ConfigureExternalAuthentication(ServiceConfigurationContext context, IConfiguration configuration)`
- [ ] Method called from `ConfigureServices()` with `configuration` parameter
- [ ] `IsFeatureEnabled(configuration, "Authentication.OpenIDConnect")` check present
- [ ] SSL bypass logic based on `ByPassSSL` config + `IsDevelopment()`
- [ ] Token validation sets `ValidIssuer = options.Authority`
- [ ] Logout event handler present (adds `IdTokenHint`)
- [ ] `options.UsePkce = true` (security)
- [ ] `options.GetClaimsFromUserInfoEndpoint = true` (get full claims)
- [ ] Scopes include at least `openid,profile,email`
- [ ] Development logging: `Microsoft.IdentityModel.Logging.IdentityModelEventSource.ShowPII = true`

---

## Sample Output (Dry-Run)

```
🎯 External SSO Integration - Code Generation

📋 Configuration to add manually to appsettings.json:
   {
     "ExternalSsoLogin": {
       "Authority": "https://your-idp.example.com/oauth2/default",
       "ClientId": "your-client-id",
       "ClientSecret": "your-client-secret",
       "ByPassSSL": false,
       "RedirectUri": "/Account/Login"
     }
   }

🔧 Code modifications:

1. File: src/MyProject.AuthServer/MyProjectAuthServerModule.cs

   ADD METHOD (after ConfigureRateLimiting or at end of class):

   private void ConfigureExternalAuthentication(ServiceConfigurationContext context, IConfiguration configuration)
   {
       var hostingEnvironment = context.Services.GetHostingEnvironment();
       var enableOpenIdConnect = IsFeatureEnabled(configuration, "Authentication.OpenIDConnect");

       if (!enableOpenIdConnect)
       {
           Console.WriteLine("[SSO] OpenID Connect is disabled");
           return;
       }

       Console.WriteLine("[SSO] Configuring OpenID Connect authentication");

       var authority = configuration["ExternalSsoLogin:Authority"]?.TrimEnd('/');
       var clientId = configuration["ExternalSsoLogin:ClientId"];
       var clientSecret = configuration["ExternalSsoLogin:ClientSecret"];
       var bypassSSL = configuration.GetValue<bool>("ExternalSsoLogin:ByPassSSL", false);
       var redirectUri = configuration["ExternalSsoLogin:RedirectUri"] ?? "/Account/Login";

       if (string.IsNullOrWhiteSpace(authority))
           throw new InvalidOperationException("ExternalSsoLogin:Authority is missing");
       if (string.IsNullOrWhiteSpace(clientId))
           throw new InvalidOperationException("ExternalSsoLogin:ClientId is missing");

       var isDevOrBypass = hostingEnvironment.IsDevelopment() || bypassSSL;
       Console.WriteLine($"[SSO] Authority: {authority}");

       context.Services.AddAuthentication()
           .AddOpenIdConnect(OpenIdConnectDefaults.AuthenticationScheme, options =>
           {
               options.Authority = authority;
               options.ClientId = clientId;
               options.ClientSecret = clientSecret;
               options.ResponseType = OpenIdConnectResponseType.CodeIdToken;
               options.UsePkce = true;
               options.SaveTokens = true;
               options.GetClaimsFromUserInfoEndpoint = true;
               options.SignedOutRedirectUri = redirectUri;

               options.Scope.Clear();
               options.Scope.Add("openid");
               options.Scope.Add("profile");
               options.Scope.Add("email");
               options.Scope.Add("role");

               if (isDevOrBypass)
               {
                   var handler = new HttpClientHandler
                   {
                       ServerCertificateCustomValidationCallback = HttpClientHandler.DangerousAcceptAnyServerCertificateValidator
                   };
                   options.Backchannel = new HttpClient(handler);
               }

               options.RequireHttpsMetadata = !isDevOrBypass;

               options.TokenValidationParameters = new TokenValidationParameters
               {
                   NameClaimType = "name",
                   RoleClaimType = "role",
                   ValidIssuer = options.Authority,
               };

               options.Events = new OpenIdConnectEvents
               {
                   OnRedirectToIdentityProviderForSignOut = async context =>
                   {
                       var result = await context.HttpContext.AuthenticateAsync(OpenIdConnectDefaults.AuthenticationScheme);
                       var idToken = result.Properties?.GetTokenValue(OpenIdConnectParameterNames.IdToken);
                       if (!string.IsNullOrEmpty(idToken))
                       {
                           context.ProtocolMessage.IdTokenHint = idToken;
                       }
                   }
               };
           });

       if (hostingEnvironment.IsDevelopment())
       {
           Microsoft.IdentityModel.Logging.IdentityModelEventSource.ShowPII = true;
       }

       Console.WriteLine("[SSO] OpenID Connect configured successfully");
   }

   ADD METHOD CALL in ConfigureServices():

   Find line containing: "ConfigureCookies(context, configuration);"
   Add immediately after:
   ConfigureExternalAuthentication(context, configuration);

2. Feature flag to enable (in appsettings.features.json or database):
   {
     "FeatureManagement": {
       "FeatureFlags": [
         { "id": "Authentication.OpenIDConnect", "enabled": true }
       ]
     }
   }

⏱ Code generation: <1 second
💾 Backup: Not created (use --backup flag next time)
```

---

## Complete Workflow Example

```bash
# 1. Generate code (dry-run to preview)
/external-sso-login-integration --dry-run

# 2. Apply with backup
/external-sso-login-integration --backup

# 3. Manually edit appsettings.json (or appsettings.Production.json):
#    Add ExternalSsoLogin section with your IdP credentials

# 4. Enable feature flag:
#    In appsettings.features.json add: "Authentication.OpenIDConnect": true
#    OR in database: INSERT INTO AbpSettings WHERE Name = 'FeatureManagement:FeatureFlags'

# 5. Build and run
dotnet build src/MyProject.AuthServer/
dotnet run --project src/MyProject.AuthServer/

# 6. Check logs for: [SSO] OpenID Connect configured successfully

# 7. Test: Navigate to https://localhost:44333/Account/Login
#    Should redirect to your IdP when clicking external login button
```

---

## Limitations

- **Single provider only** - This pattern supports one OIDC provider per deployment. For multiple providers, you'd need to extend the code.
- **No UI generation** - Assumes you have ABP Account module with external login UI
- **Assumes AuthServer module** - If your project doesn't have separate AuthServer, adapt for HttpApi.Host
- **ASP.NET Core Identity required** - Uses `IdentityConstants.ExternalScheme`

---

## Adapting to Different Module Names

If your AuthServer module has a different name or structure:

```bash
# Specify module file explicitly
/external-sso-login-integration --module src/MyApp/Auth/MyCustomAuthModule.cs
```

The skill will analyze the file and insert code appropriately.

---

## Security Best Practices

1. **Never commit client secrets** - Use environment variables or secret managers
2. **Enable HTTPS** - Set `ByPassSSL=false` in production
3. **Validate issuer** - `ValidIssuer = Authority` prevents token substitution attacks
4. **Use PKCE** - Already enabled (`UsePkce=true`) - don't disable
5. **Request minimal scopes** - Only request `openid,profile,email` plus necessary custom scopes
6. **Enable feature flag** - Keep SSO disabled until ready to test
7. **Monitor logs** - Watch for `[SSO]` messages and errors

---

**Skill Version:** 2.0.0 (Code-Only, Reusable)
**Last Updated:** 2025-03-12
**Compatible With:** ABP Framework 8.0+, .NET 8.0+
**Pattern Source:** Adapted from ACMS `AccessControlManagementSystemAuthServerModule`
**Reusability:** ✅ Works with any ABP project (customize configuration keys via flags)