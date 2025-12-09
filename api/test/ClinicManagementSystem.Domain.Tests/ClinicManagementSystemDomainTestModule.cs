using Volo.Abp.Modularity;

namespace ClinicManagementSystem;

[DependsOn(
    typeof(ClinicManagementSystemDomainModule),
    typeof(ClinicManagementSystemTestBaseModule)
)]
public class ClinicManagementSystemDomainTestModule : AbpModule
{

}
