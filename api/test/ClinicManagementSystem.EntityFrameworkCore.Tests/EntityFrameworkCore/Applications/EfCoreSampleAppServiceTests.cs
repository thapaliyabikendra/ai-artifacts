using ClinicManagementSystem.Samples;
using Xunit;

namespace ClinicManagementSystem.EntityFrameworkCore.Applications;

[Collection(ClinicManagementSystemTestConsts.CollectionDefinitionName)]
public class EfCoreSampleAppServiceTests : SampleAppServiceTests<ClinicManagementSystemEntityFrameworkCoreTestModule>
{

}
