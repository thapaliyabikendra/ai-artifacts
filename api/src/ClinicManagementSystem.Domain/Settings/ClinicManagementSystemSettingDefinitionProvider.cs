using Volo.Abp.Settings;

namespace ClinicManagementSystem.Settings;

public class ClinicManagementSystemSettingDefinitionProvider : SettingDefinitionProvider
{
    public override void Define(ISettingDefinitionContext context)
    {
        //Define your own settings here. Example:
        //context.Add(new SettingDefinition(ClinicManagementSystemSettings.MySetting1));
    }
}
