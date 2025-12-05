# Distributed Event Bus Skill

You are an expert in the Drop WMS Inbound Service distributed event bus architecture. This skill helps developers work with the ABP Framework distributed event bus powered by RabbitMQ.

## Architecture Overview

The system uses:
- **Framework**: ABP Framework's Distributed Event Bus (Volo.Abp.EventBus.Distributed)
- **Message Broker**: RabbitMQ
- **Database**: PostgreSQL with Inbox/Outbox pattern for guaranteed delivery
- **Pattern**: Outbox/Inbox pattern ensures reliable event processing
- **Multi-Tenancy**: Events are processed with tenant filtering disabled

## Key File Locations

- **Configuration**: `src/Drop.WMS.InboundService.HttpApi.Host/InboundServiceHttpApiHostModule.cs`
- **DbContext**: `src/Drop.WMS.InboundService.EntityFrameworkCore/EntityFrameworkCore/InboundServiceDbContext.cs`
- **Event Handlers**: `src/Drop.WMS.InboundService.Application/EventHandlers/`
- **AppServices**: `src/Drop.WMS.InboundService.Application/AppServices/EventHandles/`
- **Contracts**: `src/Drop.WMS.InboundService.Application.Contracts/Interfaces/`
- **AutoMapper**: `src/Drop.WMS.InboundService.Application/InboundServiceApplicationAutoMapperProfile.cs`

## Existing Event Types

### Warehouse Events
- `WarehouseTenantCompletedEto`
- `WarehouseUpdatedEto`

### User Events
- `UserAddedEto`
- `UserUpdatedEto`
- `UserDeletedEto`

### Location Events
- `LocationAddedEto`
- `LocationUpdatedEto`
- `LocationDeletedEto`

### Tag Events
- `TagStatusUpdatedEto`

### License Plate Events
- `LicensePlateAllocatedEto`
- `LicensePlateShippedOutEto`
- `LicensePlateUnAllocateEto`

## Standard Implementation Pattern

When creating a new event handler, follow this pattern:

### 1. Create Interface in Application.Contracts

Location: `src/Drop.WMS.InboundService.Application.Contracts/Interfaces/{Entity}/I{Entity}EventHandlerAppService.cs`

```csharp
using Drop.WMS.Shared.Hosting.Etos.{Entity};
using System.Threading.Tasks;

namespace Drop.WMS.InboundService.Interfaces.{Entity}
{
    public interface I{Entity}EventHandlerAppService
    {
        Task<bool> {Operation}Async({Entity}Eto eto);
    }
}
```

### 2. Create Event Handler

Location: `src/Drop.WMS.InboundService.Application/EventHandlers/{Entity}/{Entity}EventHandlerAppService.cs`

```csharp
using Drop.WMS.InboundService.Dependencies;
using Drop.WMS.InboundService.Interfaces.{Entity};
using Drop.WMS.Shared.Hosting.Etos.{Entity};
using System;
using System.Threading.Tasks;
using Volo.Abp.DependencyInjection;
using Volo.Abp.EventBus.Distributed;
using Volo.Abp;

namespace Drop.WMS.InboundService.EventHandlers.{Entity}
{
    public class {Entity}EventHandlerAppService : IDistributedEventHandler<{Entity}Eto>, ITransientDependency
    {
        private readonly CommonDependencies<{Entity}EventHandlerAppService> _commonDependencies;
        private readonly I{Entity}EventHandlerAppService _appService;

        public {Entity}EventHandlerAppService(
            CommonDependencies<{Entity}EventHandlerAppService> commonDependencies,
            I{Entity}EventHandlerAppService appService)
        {
            _commonDependencies = commonDependencies;
            _appService = appService;
        }

        public async Task HandleEventAsync({Entity}Eto eto)
        {
            try
            {
                _commonDependencies._logger.LogInformation($"::{Entity} Event Started::");
                await _appService.{Operation}Async(eto);
                _commonDependencies._logger.LogInformation($"::{Entity} Event Ended::");
            }
            catch (Exception ex)
            {
                _commonDependencies._logger.LogError($"::{Entity} Event Exception:: - {ex.Message}");
                throw new UserFriendlyException(ex.Message);
            }
        }
    }
}
```

### 3. Create AppService Implementation

Location: `src/Drop.WMS.InboundService.Application/AppServices/EventHandles/{Entity}/{Entity}EventHandlerAppService.cs`

```csharp
using Drop.WMS.InboundService.Dependencies;
using Drop.WMS.InboundService.Interfaces.{Entity};
using Drop.WMS.InboundService.Entities.{Entity};
using Drop.WMS.Shared.Hosting.Etos.{Entity};
using System;
using System.Linq;
using System.Threading.Tasks;
using Volo.Abp;
using Volo.Abp.Data;
using Volo.Abp.Domain.Repositories;
using Volo.Abp.MultiTenancy;

namespace Drop.WMS.InboundService.AppServices.EventHandles.{Entity}
{
    public class {Entity}EventHandlerAppService : InboundServiceAppService, I{Entity}EventHandlerAppService
    {
        private readonly IRepository<{Entity}, Guid> _repository;
        private readonly CommonDependencies<{Entity}EventHandlerAppService> _commonDependencies;

        public {Entity}EventHandlerAppService(
            IRepository<{Entity}, Guid> repository,
            CommonDependencies<{Entity}EventHandlerAppService> commonDependencies)
        {
            _repository = repository;
            _commonDependencies = commonDependencies;
        }

        public async Task<bool> {Operation}Async({Entity}Eto eto)
        {
            using (_commonDependencies._dataFilter.Disable<IMultiTenant>())
            {
                try
                {
                    _commonDependencies._logger.LogInformation($"::{Entity} {Operation} Started::");

                    // Check for existing entity (for updates/duplicates)
                    var existing = await _repository.FirstOrDefaultAsync(x => x.{UniqueField} == eto.{UniqueField});

                    if (existing != null)
                    {
                        // Update scenario
                        ObjectMapper.Map(eto, existing);
                        await _repository.UpdateAsync(existing);
                    }
                    else
                    {
                        // Create scenario
                        var entity = ObjectMapper.Map<{Entity}Eto, {Entity}>(eto);
                        await _repository.InsertAsync(entity);
                    }

                    _commonDependencies._logger.LogInformation($"::{Entity} {Operation} Completed::");
                    return true;
                }
                catch (Exception ex)
                {
                    _commonDependencies._logger.LogError($"::{Entity} {Operation} Exception:: - {ex.Message}");
                    throw new UserFriendlyException(ex.Message);
                }
            }
        }
    }
}
```

### 4. Add AutoMapper Configuration

Location: `src/Drop.WMS.InboundService.Application/InboundServiceApplicationAutoMapperProfile.cs`

Add mapping in the constructor:

```csharp
CreateMap<{Entity}Eto, {Entity}>()
    .ForMember(dest => dest.Id, opt => opt.Ignore());
```

## Key Patterns to Follow

1. **Dependency Injection**: Use `CommonDependencies<T>` for logger, data filter, and event bus
2. **Multi-Tenancy**: Always use `using (_commonDependencies._dataFilter.Disable<IMultiTenant>())` when processing cross-tenant events
3. **Error Handling**: Catch exceptions and throw `UserFriendlyException` for user-friendly messages
4. **Logging**: Log at start, end, and exception points with consistent format
5. **Idempotency**: Check for duplicates before creating new entities
6. **Transient Lifetime**: Implement `ITransientDependency` for event handlers
7. **Async Operations**: All methods must be async
8. **Object Mapping**: Use AutoMapper to map ETOs to domain entities

## Configuration

RabbitMQ configuration in `appsettings.json`:

```json
{
  "RabbitMQ": {
    "Connections": {
      "Default": {
        "HostName": "localhost",
        "UserName": "root",
        "Password": "root"
      }
    },
    "EventBus": {
      "ClientName": "DropWMS_InboundService",
      "ExchangeName": "DropWMS"
    }
  },
  "DistributedEventBusOptions": {
    "Enable": false,
    "PollingInterval": 0.5
  }
}
```

## Publishing Events

To publish an event from this service:

```csharp
await _distributedEventBus.PublishAsync(new {Entity}Eto
{
    // Set properties
});
```

The event will be:
1. Stored in the `OutgoingEventRecord` table (Outbox)
2. Published to RabbitMQ by the background worker
3. Consumed by other services listening to the exchange

## Troubleshooting

### Events Not Being Received
1. Check RabbitMQ connection settings in `appsettings.json`
2. Verify `DistributedEventBusOptions.Enable` is set correctly
3. Check RabbitMQ management console for message flow
4. Verify handler implements `IDistributedEventHandler<TEto>`
5. Check `IncomingEventRecord` table for inbox records

### Events Not Being Sent
1. Check `OutgoingEventRecord` table for pending events
2. Verify polling interval in `DistributedEventBusOptions`
3. Check background worker is running
4. Verify RabbitMQ connection and exchange exist

### Duplicate Event Processing
1. Check idempotency logic in handler
2. Verify unique identifier checks before insert
3. Check `IncomingEventRecord` for duplicate event IDs

## Database Tables

- **OutgoingEventRecord**: Stores events to be published (Outbox pattern)
- **IncomingEventRecord**: Stores received events (Inbox pattern)

These ensure reliable event delivery even if RabbitMQ is temporarily unavailable.

## Common Tasks

When asked to:

1. **Create a new event handler**: Follow the 4-step pattern above
2. **Debug event flow**: Check Outbox/Inbox tables and RabbitMQ console
3. **Add event logging**: Use `_commonDependencies._logger` with consistent format
4. **Handle event updates**: Check for existing entity by unique field, then update or insert
5. **Test event handling**: Publish test event and verify handler execution and database changes

## Dependencies

ETOs come from the shared package: `Drop.WMS.Shared.Hosting.Etos.*`

Ensure the ETO is defined in the shared package and referenced in this project before creating handlers.
