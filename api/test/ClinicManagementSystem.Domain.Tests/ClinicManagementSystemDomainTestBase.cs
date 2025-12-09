using Volo.Abp.Modularity;

namespace ClinicManagementSystem;

/* Inherit from this class for your domain layer tests. */
public abstract class ClinicManagementSystemDomainTestBase<TStartupModule> : ClinicManagementSystemTestBase<TStartupModule>
    where TStartupModule : IAbpModule
{

}
