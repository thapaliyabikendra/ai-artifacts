using System;
using System.Collections.Generic;
using System.Text;
using ClinicManagementSystem.Localization;
using Volo.Abp.Application.Services;

namespace ClinicManagementSystem;

/* Inherit your application services from this class.
 */
public abstract class ClinicManagementSystemAppService : ApplicationService
{
    protected ClinicManagementSystemAppService()
    {
        LocalizationResource = typeof(ClinicManagementSystemResource);
    }
}
