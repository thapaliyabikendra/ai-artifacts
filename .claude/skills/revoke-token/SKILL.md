# Revoke Token Skill

## Description
This skill revokes a user's authentication tokens when their status is changed to false (inactive) by an administrator. It ensures that when an admin deactivates a user account, any existing tokens are immediately invalidated to prevent continued access.

## Implementation Details

### Parameters
- `user_id` (string, required): The ID of the user whose tokens should be revoked
- `reason` (string, required): The reason for revocation (typically "status changed to false")

### Steps
1. Validate the user exists in the IdentityUser store
2. Verify the user's IsActive status is false
3. Use OpenIddict's token revocation service to invalidate all tokens for the user
4. Log the revocation event with administrator context for audit purposes
5. Return success confirmation

### Related Files
- `src/Amnil.VideoKyc.Application/Appservices/CustomAppServices/CustomUserAppService.cs` - User management service
- `src/Amnil.VideoKyc.Domain/OpenIddict/OpenIddictDataSeedContributor.cs` - OpenIddict configuration
- `src/Amnil.VideoKyc.AuthServer/VideoKycSignInManager.cs` - Custom sign-in manager

### Usage
This skill would typically be invoked when:
- An administrator updates a user's status to inactive via the user management interface
- A user account is disabled through administrative actions
- Security policies require immediate token revocation upon status change

## Notes
- This skill assumes OpenIddict is being used for token management (as evidenced by the OpenIddictDataSeedContributor.cs file)
- Integration with the existing user update flow in CustomUserAppService.UpdateAsync method would be required
- Proper error handling and logging should be implemented for production use