using ClinicManagementSystem.Localization;
using Volo.Abp.AspNetCore.Mvc;

namespace ClinicManagementSystem.Controllers;

/* Inherit your controllers from this class.
 */
public abstract class ClinicManagementSystemController : AbpControllerBase
{
    protected ClinicManagementSystemController()
    {
        LocalizationResource = typeof(ClinicManagementSystemResource);
    }
}
