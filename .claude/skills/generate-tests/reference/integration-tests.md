# HTTP API Integration Tests

## Template

```csharp
using System.Net;
using System.Net.Http.Json;
using Shouldly;
using Xunit;

namespace [Namespace].HttpApi.Tests;

public class [Entity]ControllerTests : [Module]HttpApiTestBase
{
    private const string BaseUrl = "/api/app/[entities]";

    [Fact]
    public async Task GetList_ReturnsOk()
    {
        var response = await Client.GetAsync(BaseUrl);
        response.StatusCode.ShouldBe(HttpStatusCode.OK);
    }

    [Fact]
    public async Task Get_ExistingId_ReturnsOk()
    {
        var response = await Client.GetAsync($"{BaseUrl}/{TestData.[Entity]Id}");
        response.StatusCode.ShouldBe(HttpStatusCode.OK);
    }

    [Fact]
    public async Task Get_NonExistingId_ReturnsNotFound()
    {
        var response = await Client.GetAsync($"{BaseUrl}/{Guid.NewGuid()}");
        response.StatusCode.ShouldBe(HttpStatusCode.NotFound);
    }

    [Fact]
    public async Task Create_ValidInput_ReturnsCreated()
    {
        var input = new Create[Entity]Dto { Name = "Test" };
        var response = await Client.PostAsJsonAsync(BaseUrl, input);
        response.StatusCode.ShouldBe(HttpStatusCode.Created);
    }

    [Fact]
    public async Task Create_InvalidInput_ReturnsBadRequest()
    {
        var response = await Client.PostAsJsonAsync(BaseUrl, new Create[Entity]Dto());
        response.StatusCode.ShouldBe(HttpStatusCode.BadRequest);
    }

    [Fact]
    public async Task Delete_Unauthorized_ReturnsForbidden()
    {
        await AuthenticateAsAsync("readonly-user");
        var response = await Client.DeleteAsync($"{BaseUrl}/{TestData.[Entity]Id}");
        response.StatusCode.ShouldBe(HttpStatusCode.Forbidden);
    }
}
```

## HTTP Status Codes

| Scenario | Status |
|----------|--------|
| GET/PUT success | 200 OK |
| POST created | 201 Created |
| DELETE success | 204 NoContent |
| Validation error | 400 BadRequest |
| Not authenticated | 401 Unauthorized |
| No permission | 403 Forbidden |
| Not found | 404 NotFound |
| Conflict | 409 Conflict |

## Authentication

```csharp
// Login as test user
await AuthenticateAsAsync("admin");
await AuthenticateAsAsync("readonly-user");

// Login with specific permission
await AuthenticateWithPermissionAsync("MyModule.Entity.Delete");

// Test anonymous access
Client.DefaultRequestHeaders.Authorization = null;
```

## Error Response

```csharp
var error = await response.Content.ReadFromJsonAsync<RemoteServiceErrorResponse>();
error.Error.Code.ShouldBe("MyModule:EntityInUse");
error.Error.Message.ShouldContain("cannot be deleted");
```
