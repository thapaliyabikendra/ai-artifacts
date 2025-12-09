using Volo.Abp.Modularity;

namespace ClinicManagementSystem;

[DependsOn(
    typeof(ClinicManagementSystemApplicationModule),
    typeof(ClinicManagementSystemDomainTestModule)
)]
public class ClinicManagementSystemApplicationTestModule : AbpModule
{

}
