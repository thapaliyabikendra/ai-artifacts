using System.Threading.Tasks;
using Volo.Abp.DependencyInjection;

namespace ClinicManagementSystem.Data;

/* This is used if database provider does't define
 * IClinicManagementSystemDbSchemaMigrator implementation.
 */
public class NullClinicManagementSystemDbSchemaMigrator : IClinicManagementSystemDbSchemaMigrator, ITransientDependency
{
    public Task MigrateAsync()
    {
        return Task.CompletedTask;
    }
}
