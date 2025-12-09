using System.Threading.Tasks;

namespace ClinicManagementSystem.Data;

public interface IClinicManagementSystemDbSchemaMigrator
{
    Task MigrateAsync();
}
