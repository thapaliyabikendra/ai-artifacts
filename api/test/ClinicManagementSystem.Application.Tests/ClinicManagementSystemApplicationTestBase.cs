using Volo.Abp.Modularity;

namespace ClinicManagementSystem;

public abstract class ClinicManagementSystemApplicationTestBase<TStartupModule> : ClinicManagementSystemTestBase<TStartupModule>
    where TStartupModule : IAbpModule
{

}
