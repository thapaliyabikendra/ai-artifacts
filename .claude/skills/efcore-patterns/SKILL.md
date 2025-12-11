---
name: efcore-patterns
description: "Master Entity Framework Core patterns for ABP Framework including entity configuration, DbContext, migrations, relationships, and performance optimization. Use when: (1) configuring entities with Fluent API, (2) creating migrations, (3) designing relationships, (4) implementing repository patterns."
---

# EF Core Patterns

Entity Framework Core patterns for ABP Framework code-first development.

## When to Use

- Configuring entity mappings with Fluent API
- Creating and managing migrations
- Designing entity relationships (1:N, N:N)
- Implementing value objects and owned types
- Handling concurrency and optimistic locking
- Configuring inheritance hierarchies

## Entity Configuration

### ABP Base Classes

```csharp
// Full auditing with soft delete (most common)
public class Patient : FullAuditedAggregateRoot<Guid>
{
    public string FirstName { get; private set; }
    public string LastName { get; private set; }
    public string Email { get; private set; }
    public DateTime DateOfBirth { get; private set; }

    private Patient() { } // For EF Core

    public Patient(Guid id, string firstName, string lastName, string email)
        : base(id)
    {
        FirstName = Check.NotNullOrWhiteSpace(firstName, nameof(firstName), maxLength: 100);
        LastName = Check.NotNullOrWhiteSpace(lastName, nameof(lastName), maxLength: 100);
        Email = Check.NotNullOrWhiteSpace(email, nameof(email), maxLength: 255);
    }

    public void UpdateName(string firstName, string lastName)
    {
        FirstName = Check.NotNullOrWhiteSpace(firstName, nameof(firstName), maxLength: 100);
        LastName = Check.NotNullOrWhiteSpace(lastName, nameof(lastName), maxLength: 100);
    }
}

// Without soft delete
public class AuditLog : AuditedEntity<Guid>
{
    // CreationTime, CreatorId, LastModificationTime, LastModifierId
}

// Simple entity without auditing
public class Setting : Entity<Guid>
{
    // Just Id
}
```

### ABP Base Class Hierarchy

| Base Class | Fields Included |
|------------|-----------------|
| `Entity<TKey>` | Id |
| `AuditedEntity<TKey>` | + CreationTime, CreatorId, LastModificationTime, LastModifierId |
| `FullAuditedEntity<TKey>` | + IsDeleted, DeleterId, DeletionTime |
| `AggregateRoot<TKey>` | Entity + Domain Events + Concurrency Token |
| `AuditedAggregateRoot<TKey>` | AggregateRoot + Auditing |
| `FullAuditedAggregateRoot<TKey>` | AuditedAggregateRoot + Soft Delete |

### Fluent API Configuration

```csharp
public class PatientConfiguration : IEntityTypeConfiguration<Patient>
{
    public void Configure(EntityTypeBuilder<Patient> builder)
    {
        builder.ToTable("Patients");

        builder.HasKey(x => x.Id);

        builder.Property(x => x.FirstName)
            .IsRequired()
            .HasMaxLength(100);

        builder.Property(x => x.LastName)
            .IsRequired()
            .HasMaxLength(100);

        builder.Property(x => x.Email)
            .IsRequired()
            .HasMaxLength(255);

        builder.HasIndex(x => x.Email)
            .IsUnique();

        // ABP soft delete filter (automatic)
        builder.HasQueryFilter(x => !x.IsDeleted);
    }
}
```

### DbContext Configuration

```csharp
public class ClinicDbContext : AbpDbContext<ClinicDbContext>
{
    public DbSet<Patient> Patients { get; set; }
    public DbSet<Doctor> Doctors { get; set; }
    public DbSet<Appointment> Appointments { get; set; }

    public ClinicDbContext(DbContextOptions<ClinicDbContext> options)
        : base(options)
    {
    }

    protected override void OnModelCreating(ModelBuilder builder)
    {
        base.OnModelCreating(builder);

        // Apply all configurations from assembly
        builder.ApplyConfigurationsFromAssembly(typeof(ClinicDbContext).Assembly);

        // Or configure inline
        builder.Entity<Patient>(b =>
        {
            b.ToTable("Patients");
            b.HasIndex(x => x.Email).IsUnique();
        });
    }
}
```

## Relationships

### One-to-Many (1:N)

```csharp
// Parent entity
public class Doctor : FullAuditedAggregateRoot<Guid>
{
    public string FullName { get; private set; }
    public ICollection<Appointment> Appointments { get; private set; } = new List<Appointment>();
}

// Child entity
public class Appointment : FullAuditedEntity<Guid>
{
    public Guid DoctorId { get; private set; }
    public Doctor Doctor { get; private set; }
    public DateTime AppointmentDate { get; private set; }
}

// Configuration
builder.Entity<Appointment>(b =>
{
    b.HasOne(x => x.Doctor)
        .WithMany(x => x.Appointments)
        .HasForeignKey(x => x.DoctorId)
        .OnDelete(DeleteBehavior.Restrict); // Prevent cascade delete
});
```

### Many-to-Many (N:N)

```csharp
// With explicit join entity (recommended for ABP)
public class DoctorSpecialization : Entity
{
    public Guid DoctorId { get; set; }
    public Doctor Doctor { get; set; }
    public Guid SpecializationId { get; set; }
    public Specialization Specialization { get; set; }

    public override object[] GetKeys() => new object[] { DoctorId, SpecializationId };
}

// Configuration
builder.Entity<DoctorSpecialization>(b =>
{
    b.ToTable("DoctorSpecializations");
    b.HasKey(x => new { x.DoctorId, x.SpecializationId });

    b.HasOne(x => x.Doctor)
        .WithMany(x => x.Specializations)
        .HasForeignKey(x => x.DoctorId);

    b.HasOne(x => x.Specialization)
        .WithMany(x => x.Doctors)
        .HasForeignKey(x => x.SpecializationId);
});
```

### One-to-One (1:1)

```csharp
public class Patient : FullAuditedAggregateRoot<Guid>
{
    public PatientProfile Profile { get; private set; }
}

public class PatientProfile : Entity<Guid>
{
    public Guid PatientId { get; set; }
    public Patient Patient { get; set; }
    public string EmergencyContact { get; set; }
}

// Configuration
builder.Entity<PatientProfile>(b =>
{
    b.HasOne(x => x.Patient)
        .WithOne(x => x.Profile)
        .HasForeignKey<PatientProfile>(x => x.PatientId);
});
```

## Value Objects & Owned Types

```csharp
// Value object
public class Address
{
    public string Street { get; private set; }
    public string City { get; private set; }
    public string PostalCode { get; private set; }

    private Address() { }

    public Address(string street, string city, string postalCode)
    {
        Street = street;
        City = city;
        PostalCode = postalCode;
    }
}

// Entity using value object
public class Patient : FullAuditedAggregateRoot<Guid>
{
    public Address Address { get; private set; }
}

// Configuration as owned type
builder.Entity<Patient>(b =>
{
    b.OwnsOne(x => x.Address, address =>
    {
        address.Property(a => a.Street).HasMaxLength(200);
        address.Property(a => a.City).HasMaxLength(100);
        address.Property(a => a.PostalCode).HasMaxLength(20);
    });
});
```

## Enums

```csharp
// Enum in Domain.Shared
public enum AppointmentStatus
{
    Scheduled = 0,
    Confirmed = 1,
    InProgress = 2,
    Completed = 3,
    Cancelled = 4,
    NoShow = 5
}

// Entity using enum
public class Appointment : FullAuditedEntity<Guid>
{
    public AppointmentStatus Status { get; private set; }
}

// Configuration (stored as int by default)
builder.Entity<Appointment>(b =>
{
    b.Property(x => x.Status)
        .HasConversion<int>(); // Explicit, but default behavior

    // Or store as string
    b.Property(x => x.Status)
        .HasConversion<string>()
        .HasMaxLength(20);
});
```

## Migrations

### Creating Migrations

```bash
# Navigate to EntityFrameworkCore project
cd api/src/ClinicManagementSystem.EntityFrameworkCore

# Add migration
dotnet ef migrations add AddPatientEntity \
    --startup-project ../ClinicManagementSystem.DbMigrator

# Apply migration
dotnet ef database update \
    --startup-project ../ClinicManagementSystem.DbMigrator

# Or use DbMigrator project
cd api/src/ClinicManagementSystem.DbMigrator
dotnet run
```

### Migration Best Practices

```csharp
// Good: Split large migrations
// Migration 1: Add new tables
public partial class AddPatientEntity : Migration
{
    protected override void Up(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.CreateTable(
            name: "Patients",
            columns: table => new
            {
                Id = table.Column<Guid>(nullable: false),
                FirstName = table.Column<string>(maxLength: 100, nullable: false),
                // ... other columns
            },
            constraints: table =>
            {
                table.PrimaryKey("PK_Patients", x => x.Id);
            });

        migrationBuilder.CreateIndex(
            name: "IX_Patients_Email",
            table: "Patients",
            column: "Email",
            unique: true);
    }
}

// Migration 2: Add data (separate migration)
public partial class SeedInitialPatients : Migration
{
    protected override void Up(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.InsertData(
            table: "Patients",
            columns: new[] { "Id", "FirstName", "LastName", "Email" },
            values: new object[] { Guid.NewGuid(), "John", "Doe", "john@example.com" });
    }
}
```

## Concurrency Handling

```csharp
// ABP provides automatic concurrency token via AggregateRoot
public class Patient : FullAuditedAggregateRoot<Guid>
{
    // ConcurrencyStamp is inherited from AggregateRoot
}

// In AppService - ABP handles optimistic concurrency automatically
public async Task UpdateAsync(Guid id, UpdatePatientDto input)
{
    var patient = await _patientRepository.GetAsync(id);

    // ABP checks ConcurrencyStamp automatically
    patient.UpdateName(input.FirstName, input.LastName);

    await _patientRepository.UpdateAsync(patient);
}

// Handle concurrency exception
try
{
    await _patientRepository.UpdateAsync(patient);
}
catch (AbpDbConcurrencyException)
{
    throw new UserFriendlyException("Record was modified by another user. Please refresh and try again.");
}
```

## Global Query Filters

```csharp
// ABP automatically applies these filters:
// - ISoftDelete: WHERE IsDeleted = false
// - IMultiTenant: WHERE TenantId = @currentTenantId

// Disable soft delete filter temporarily
using (_dataFilter.Disable<ISoftDelete>())
{
    var allPatients = await _patientRepository.GetListAsync();
    // Includes soft-deleted patients
}

// Disable multi-tenant filter
using (_dataFilter.Disable<IMultiTenant>())
{
    var allTenantPatients = await _patientRepository.GetListAsync();
}
```

## Performance Patterns

### Batch Operations (EF Core 7+)

```csharp
// Batch update without loading entities
await _context.Patients
    .Where(p => p.Status == PatientStatus.Inactive)
    .Where(p => p.LastVisitDate < DateTime.UtcNow.AddYears(-2))
    .ExecuteUpdateAsync(setters => setters
        .SetProperty(p => p.IsArchived, true));

// Batch delete without loading entities
await _context.AuditLogs
    .Where(l => l.CreationTime < DateTime.UtcNow.AddMonths(-6))
    .ExecuteDeleteAsync();
```

### Split Queries

```csharp
// Avoid Cartesian explosion with multiple collections
var doctors = await _context.Doctors
    .Include(d => d.Appointments)
    .Include(d => d.Specializations)
    .AsSplitQuery() // Executes separate queries for each Include
    .ToListAsync();
```

### Compiled Queries

```csharp
// Define compiled query (for hot paths)
private static readonly Func<ClinicDbContext, Guid, Task<Patient?>> GetPatientById =
    EF.CompileAsyncQuery((ClinicDbContext context, Guid id) =>
        context.Patients.FirstOrDefault(p => p.Id == id));

// Use compiled query
public async Task<Patient?> GetAsync(Guid id)
{
    return await GetPatientById(_context, id);
}
```

## Index Configuration

```csharp
builder.Entity<Patient>(b =>
{
    // Simple index
    b.HasIndex(x => x.Email).IsUnique();

    // Composite index
    b.HasIndex(x => new { x.LastName, x.FirstName });

    // Filtered index (partial)
    b.HasIndex(x => x.Email)
        .HasFilter("\"IsDeleted\" = false");

    // Include columns for covering index
    b.HasIndex(x => x.Email)
        .IncludeProperties(x => new { x.FirstName, x.LastName });
});
```

## PostgreSQL-Specific Patterns

### PostgreSQL Data Types

```csharp
// Entity with PostgreSQL-specific types
public class AuditRecord : Entity<Guid>
{
    public string[] Tags { get; set; }           // PostgreSQL array
    public Dictionary<string, object> Metadata { get; set; }  // jsonb
    public NpgsqlRange<DateTime> ValidRange { get; set; }     // daterange
}

// Configuration
builder.Entity<AuditRecord>(b =>
{
    // Array column
    b.Property(x => x.Tags)
        .HasColumnType("text[]");

    // JSONB column (most common for flexible data)
    b.Property(x => x.Metadata)
        .HasColumnType("jsonb");

    // Date range
    b.Property(x => x.ValidRange)
        .HasColumnType("daterange");
});
```

### PostgreSQL UUID Primary Key

```csharp
// PostgreSQL generates UUID (no need for client-side generation)
builder.Entity<Patient>(b =>
{
    b.Property(x => x.Id)
        .HasDefaultValueSql("gen_random_uuid()");
});
```

### Full-Text Search with tsvector

```csharp
// Entity with search vector
public class Patient : FullAuditedAggregateRoot<Guid>
{
    public string FirstName { get; private set; }
    public string LastName { get; private set; }
    public NpgsqlTsVector SearchVector { get; private set; }
}

// Configuration
builder.Entity<Patient>(b =>
{
    // Generated column for full-text search
    b.Property(x => x.SearchVector)
        .HasColumnType("tsvector")
        .HasComputedColumnSql(
            "to_tsvector('english', coalesce(\"FirstName\", '') || ' ' || coalesce(\"LastName\", ''))",
            stored: true);

    // GIN index for fast text search
    b.HasIndex(x => x.SearchVector)
        .HasMethod("GIN");
});

// Usage in repository
public async Task<List<Patient>> SearchAsync(string searchTerm)
{
    var dbSet = await GetDbSetAsync();
    return await dbSet
        .Where(p => p.SearchVector.Matches(EF.Functions.ToTsQuery("english", searchTerm)))
        .ToListAsync();
}
```

### PostgreSQL Index Types

```csharp
builder.Entity<Patient>(b =>
{
    // B-tree (default) - equality and range queries
    b.HasIndex(x => x.Email).IsUnique();

    // GIN - arrays, jsonb, full-text search
    b.HasIndex(x => x.Tags).HasMethod("GIN");

    // GiST - geometric data, ranges, full-text
    b.HasIndex(x => x.ValidRange).HasMethod("GIST");

    // BRIN - large tables with natural ordering
    b.HasIndex(x => x.CreationTime).HasMethod("BRIN");

    // Partial index (filtered)
    b.HasIndex(x => x.Email)
        .HasFilter("\"IsDeleted\" = false")
        .IsUnique();

    // Covering index (include columns)
    b.HasIndex(x => x.Email)
        .IncludeProperties(x => new { x.FirstName, x.LastName });
});
```

### JSONB Queries

```csharp
// Query JSONB data
public async Task<List<AuditRecord>> GetByMetadataAsync(string key, string value)
{
    var dbSet = await GetDbSetAsync();

    // Using raw SQL for complex JSONB queries
    return await dbSet
        .FromSqlRaw(
            "SELECT * FROM \"AuditRecords\" WHERE \"Metadata\" @> @p0::jsonb",
            $"{{\"{key}\": \"{value}\"}}")
        .ToListAsync();

    // Or using EF.Functions (limited support)
    return await dbSet
        .Where(x => EF.Functions.JsonContains(x.Metadata, new { key = value }))
        .ToListAsync();
}
```

### PostgreSQL Connection String

```json
{
  "ConnectionStrings": {
    "Default": "Host=localhost;Port=5432;Database=ClinicManagementSystem;Username=postgres;Password=secret;Include Error Detail=true;Pooling=true;Minimum Pool Size=5;Maximum Pool Size=100"
  }
}
```

**Key parameters:**
- `Include Error Detail=true` - Detailed errors in dev
- `Pooling=true` - Enable connection pooling
- `Minimum Pool Size` / `Maximum Pool Size` - Pool limits
- `Command Timeout` - Query timeout in seconds
- `SSL Mode=Require` - For production

### PostgreSQL-Specific Migrations

```csharp
protected override void Up(MigrationBuilder migrationBuilder)
{
    // Create extension (for UUID, full-text, etc.)
    migrationBuilder.Sql("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";");
    migrationBuilder.Sql("CREATE EXTENSION IF NOT EXISTS \"pg_trgm\";"); // Trigram for LIKE optimization

    // Create enum type
    migrationBuilder.Sql(@"
        DO $$ BEGIN
            CREATE TYPE appointment_status AS ENUM ('Scheduled', 'Confirmed', 'Completed', 'Cancelled');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    ");

    // Create table with PostgreSQL features
    migrationBuilder.CreateTable(
        name: "Patients",
        columns: table => new
        {
            Id = table.Column<Guid>(nullable: false, defaultValueSql: "gen_random_uuid()"),
            Tags = table.Column<string[]>(type: "text[]", nullable: true),
            Metadata = table.Column<string>(type: "jsonb", nullable: true),
            SearchVector = table.Column<NpgsqlTsVector>(type: "tsvector", nullable: true)
        });

    // Create GIN index
    migrationBuilder.Sql(@"
        CREATE INDEX ""IX_Patients_SearchVector"" ON ""Patients"" USING GIN (""SearchVector"");
    ");
}
```

### ABP with PostgreSQL Configuration

```csharp
// EntityFrameworkCoreModule configuration
public override void ConfigureServices(ServiceConfigurationContext context)
{
    context.Services.AddAbpDbContext<ClinicDbContext>(options =>
    {
        options.AddDefaultRepositories(includeAllEntities: true);
    });

    Configure<AbpDbContextOptions>(options =>
    {
        options.UseNpgsql(npgsqlOptions =>
        {
            // Enable retry on transient errors
            npgsqlOptions.EnableRetryOnFailure(
                maxRetryCount: 3,
                maxRetryDelay: TimeSpan.FromSeconds(30),
                errorCodesToAdd: null);

            // Command timeout
            npgsqlOptions.CommandTimeout(60);
        });
    });
}
```

## Quality Checklist

- [ ] Entities inherit appropriate ABP base class
- [ ] Private setters with public methods for encapsulation
- [ ] Private parameterless constructor for EF Core
- [ ] Fluent API configuration in separate class
- [ ] Indexes defined for query patterns
- [ ] Relationships have explicit delete behavior
- [ ] Value objects configured as owned types
- [ ] Enums have explicit conversion
- [ ] Concurrency handled via AggregateRoot
- [ ] PostgreSQL-specific types used where appropriate (jsonb, arrays)
- [ ] GIN/GiST indexes for jsonb and full-text columns

## Integration Points

This skill is used by:
- **abp-developer**: Entity and DbContext implementation
- **backend-architect**: Data layer design decisions
- **code-reviewer**: EF Core pattern validation
- **database-migrator**: Migration generation and review
