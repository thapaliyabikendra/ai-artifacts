# Revoke Token Implementation Guide

This guide explains how to implement the token revocation functionality when a user's status changes to false.

## Integration Points

The token revocation should be integrated into the `CustomUserAppService.UpdateAsync` method, specifically after checking if the user's status is being set to false.

## Implementation Steps

### 1. Add Required Dependencies
Add these using statements to CustomUserAppService.cs:
```csharp
using Volo.Abp.OpenIddict;
using Volo.Abp.OpenIddict.AuthorizationServer;
using Volo.Abp.OpenIddict.Applications;
```

### 2. Inject Required Services
Add to constructor:
```csharp
private readonly IOpenIddictApplicationManager _applicationManager;
private readonly IOpenIddictAuthorizationManager _authorizationManager;
private readonly IOpenIddictScopeManager _scopeManager;
```

Update constructor parameters:
```csharp
public CustomUserAppService(
    // ... existing parameters
    IOpenIddictApplicationManager applicationManager,
    IOpenIddictAuthorizationManager authorizationManager,
    IOpenIddictScopeManager scopeManager
    // ... rest of parameters
)
{
    // ... existing assignments
    _applicationManager = applicationManager;
    _authorizationManager = authorizationManager;
    _scopeManager = scopeManager;
}
```

### 3. Add Token Revocation Method
Add this method to CustomUserAppService.cs:
```csharp
private async Task RevokeUserTokensAsync(Guid userId, string reason)
{
    try
    {
        // Find all applications/tokens for the user
        var applications = await _applicationManager.GetListAsync(
            filter: t => t.Properties.ContainsKey("sub") &&
                       t.Properties["sub"] == userId.ToString()
        );

        foreach (var application in applications)
        {
            // Revoke tokens for this application
            await _applicationManager.RevokeTokenByClientIdAsync(
                application.ClientId,
                reason: reason
            );
        }

        _logger.LogInformation(
            "Tokens revoked for user {UserId}. Reason: {Reason}",
            userId,
            reason
        );
    }
    catch (Exception ex)
    {
        _logger.LogError(ex,
            "Error revoking tokens for user {UserId}: {Message}",
            userId,
            ex.Message
        );
        // Don't throw - we don't want to fail the user update if token revocation fails
    }
}
```

### 4. Integrate into UpdateAsync Method
In the UpdateAsync method, after line 294 where `userExtension.IsActive = input.IsActive;` is set, add:
```csharp
// If user is being deactivated, revoke their tokens
if (!input.IsActive && userExtension.IsActive)
{
    await RevokeUserTokensAsync(user.Id, "User status changed to inactive by admin");
}
```

### 5. Alternative Approach Using Hangfire
For asynchronous processing, you could also queue this as a background job:
```csharp
// If user is being deactivated, queue token revocation
if (!input.IsActive && userExtension.IsActive)
{
    BackgroundJob.Enqueue<CustomUserAppService>(
        service => service.RevokeUserTokensAsync(user.Id, "User status changed to inactive by admin")
    );
}
```

## Testing Considerations

1. Test with active user -> inactive transition (should revoke tokens)
2. Test with inactive user -> active transition (should NOT revoke tokens)
3. Test with no status change (should NOT revoke tokens)
4. Test error handling when token revocation fails
5. Verify audit logs are created appropriately

## Security Notes

- Ensure only administrators can trigger this functionality
- The reason parameter should be validated/sanitized
- Consider implementing rate limiting to prevent abuse
- Log both successful and failed revocation attempts for security monitoring