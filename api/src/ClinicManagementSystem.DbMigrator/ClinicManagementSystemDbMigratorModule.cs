using ClinicManagementSystem.EntityFrameworkCore;
using Volo.Abp.Autofac;
using Volo.Abp.Caching;
using Volo.Abp.Caching.StackExchangeRedis;
using Volo.Abp.Modularity;

namespace ClinicManagementSystem.DbMigrator;

[DependsOn(
    typeof(AbpAutofacModule),
    typeof(AbpCachingStackExchangeRedisModule),
    typeof(ClinicManagementSystemEntityFrameworkCoreModule),
    typeof(ClinicManagementSystemApplicationContractsModule)
    )]
public class ClinicManagementSystemDbMigratorModule : AbpModule
{
    public override void ConfigureServices(ServiceConfigurationContext context)
    {
        Configure<AbpDistributedCacheOptions>(options => { options.KeyPrefix = "ClinicManagementSystem:"; });
    }
}
