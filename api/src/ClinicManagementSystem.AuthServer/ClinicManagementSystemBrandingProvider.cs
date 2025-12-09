using Microsoft.Extensions.Localization;
using ClinicManagementSystem.Localization;
using Volo.Abp.Ui.Branding;
using Volo.Abp.DependencyInjection;

namespace ClinicManagementSystem;

[Dependency(ReplaceServices = true)]
public class ClinicManagementSystemBrandingProvider : DefaultBrandingProvider
{
    private IStringLocalizer<ClinicManagementSystemResource> _localizer;

    public ClinicManagementSystemBrandingProvider(IStringLocalizer<ClinicManagementSystemResource> localizer)
    {
        _localizer = localizer;
    }

    public override string AppName => _localizer["AppName"];
}
