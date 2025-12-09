using System;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using ClinicManagementSystem.Data;
using Volo.Abp.DependencyInjection;

namespace ClinicManagementSystem.EntityFrameworkCore;

public class EntityFrameworkCoreClinicManagementSystemDbSchemaMigrator
    : IClinicManagementSystemDbSchemaMigrator, ITransientDependency
{
    private readonly IServiceProvider _serviceProvider;

    public EntityFrameworkCoreClinicManagementSystemDbSchemaMigrator(
        IServiceProvider serviceProvider)
    {
        _serviceProvider = serviceProvider;
    }

    public async Task MigrateAsync()
    {
        /* We intentionally resolve the ClinicManagementSystemDbContext
         * from IServiceProvider (instead of directly injecting it)
         * to properly get the connection string of the current tenant in the
         * current scope.
         */

        await _serviceProvider
            .GetRequiredService<ClinicManagementSystemDbContext>()
            .Database
            .MigrateAsync();
    }
}
