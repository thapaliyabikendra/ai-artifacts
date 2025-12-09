using ClinicManagementSystem.Localization;
using Volo.Abp.Authorization.Permissions;
using Volo.Abp.Localization;

namespace ClinicManagementSystem.Permissions;

public class ClinicManagementSystemPermissionDefinitionProvider : PermissionDefinitionProvider
{
    public override void Define(IPermissionDefinitionContext context)
    {
        var myGroup = context.AddGroup(ClinicManagementSystemPermissions.GroupName);
        //Define your own permissions here. Example:
        //myGroup.AddPermission(ClinicManagementSystemPermissions.MyPermission1, L("Permission:MyPermission1"));
    }

    private static LocalizableString L(string name)
    {
        return LocalizableString.Create<ClinicManagementSystemResource>(name);
    }
}
