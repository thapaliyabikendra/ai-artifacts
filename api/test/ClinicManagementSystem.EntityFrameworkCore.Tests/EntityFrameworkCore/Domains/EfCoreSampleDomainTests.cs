using ClinicManagementSystem.Samples;
using Xunit;

namespace ClinicManagementSystem.EntityFrameworkCore.Domains;

[Collection(ClinicManagementSystemTestConsts.CollectionDefinitionName)]
public class EfCoreSampleDomainTests : SampleDomainTests<ClinicManagementSystemEntityFrameworkCoreTestModule>
{

}
