# DbMigrator Docker Configuration Skill

## Overview

This skill generates production-ready Docker configurations for ABP Framework DbMigrator projects. It creates optimized `Dockerfile`, `docker-compose.yml`, and supporting configuration files for containerizing database migration tasks.

## Purpose

DbMigrator is a standalone .NET application that applies database migrations and seed data. Containerizing it provides:
- **Consistent** migration execution across environments
- **Isolated** database operations with proper dependency management
- **Scheduled** migrations via Kubernetes CronJobs or Docker schedules
- **Reproducible** database setup for new environments
- **CI/CD** integration for automated deployments

## When to Use

✅ Containerize a DbMigrator for:
- Kubernetes deployments (as CronJob or Job)
- Docker Compose development environments
- CI/CD pipelines (GitHub Actions, GitLab CI, Azure DevOps)
- Multi-environment deployments (Dev/Staging/Prod)
- Air-gapped or isolated network environments

❌ Skip containerization if:
- Running migrations manually from developer machine only
- Using alternative migration tools (Flyway, Liquibase, EF Core CLI)
- Database is read-only or cannot be modified

## What the Skill Generates

Depending on options, the skill creates:

### 1. Dockerfile
- Multi-stage build for minimal final image
- Non-root user for security
- Proper .NET runtime configuration
- Health check for container readiness
- Logging configuration (Serilog to stdout/stderr)
- Environment variable support

### 2. docker-compose.yml
- Service definition for DbMigrator
- Network configuration (bridge or host)
- Volume mounts for logs, configuration
- Environment variable injection
- Restart policy (none for one-off migrations)
- Dependency on database service

### 3. Kubernetes Manifests (optional)
- `Job` manifest for one-time migration
- `CronJob` manifest for scheduled migrations
- ConfigMap for appsettings
- Secret for connection strings
- ServiceAccount with proper RBAC

### 4. CI/CD Pipeline Templates
- GitHub Actions workflow
- Azure DevOps pipeline
- GitLab CI configuration

## Usage

```bash
/dbmigrator-docker-config [options]
```

### Options

**Output Formats:**
- `--dockerfile` - Generate Dockerfile only (default: true)
- `--compose` - Generate docker-compose.yml
- `--kubernetes` - Generate Kubernetes manifests (Job/CronJob)
- `--all` - Generate all formats (Dockerfile + compose + k8s)

**Configuration:**
- `--project <name>` - Project name (auto-detected from .csproj)
- `--tag <version>` - Docker image tag (default: latest)
- `--registry <url>` - Docker registry URL (for pushing)
- `--environment <env>` - Target environment (Development/Staging/Production)
- `--output <dir>` - Output directory (default: ./docker)

**Advanced:**
- `--include-secrets` - Include secret management examples
- `--health-check` - Add custom health check endpoint
- `--no-multi-stage` - Use single-stage build (simpler but larger)
- `--base-image <image>` - Base runtime image (default: mcr.microsoft.com/dotnet/aspnet:8.0)
- `--dry-run` - Preview without writing files

### Examples

```bash
# Generate all Docker configs for current project
/dbmigrator-docker-config --all

# Generate only Dockerfile and docker-compose for staging
/dbmigrator-docker-config --compose --environment Staging --output ./infra/docker

# Generate Kubernetes CronJob for production
/dbmigrator-docker-config --kubernetes --environment Production --tag v1.0.0

# Preview what would be generated
/dbmigrator-docker-config --all --dry-run
```

## Generated Files Structure

```
docker/
├── Dockerfile
├── docker-compose.yml
├── docker-compose.override.yml
├── .env.example
├── .dockerignore
├── manifests/
│   ├── job.yaml
│   ├── cronjob.yaml
│   ├── configmap.yaml
│   └── secret.yaml
└── ci/
    ├── github-actions.yml
    ├── gitlab-ci.yml
    └── azure-pipelines.yml
```

## Dockerfile Template

The skill generates a multi-stage Dockerfile based on your project:

```dockerfile
# Stage 1: Build
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# Copy solution and project files
COPY ["*.sln", "./"]
COPY ["src/MyProject.DbMigrator/MyProject.DbMigrator.csproj", "src/MyProject.DbMigrator/"]
COPY ["src/MyProject.EntityFrameworkCore/MyProject.EntityFrameworkCore.csproj", "src/MyProject.EntityFrameworkCore/"]
COPY ["src/MyProject.Domain/MyProject.Domain.csproj", "src/MyProject.Domain/"]
COPY ["src/MyProject.Domain.Shared/MyProject.Domain.Shared.csproj", "src/MyProject.Domain.Shared/"]
COPY ["src/MyProject.Application/ MyProject.Application.csproj", "src/MyProject.Application/"]
COPY ["src/MyProject.Application.Contracts/MyProject.Application.Contracts.csproj", "src/MyProject.Application.Contracts/"]
COPY ["src/MyProject.HttpApi/MyProject.HttpApi.csproj", "src/MyProject.HttpApi/"]

# Restore dependencies
RUN dotnet restore "./src/MyProject.DbMigrator/MyProject.DbMigrator.csproj"

# Copy everything else and build
COPY . .
WORKDIR "/src/src/MyProject.DbMigrator"
RUN dotnet build "MyProject.DbMigrator.csproj" -c Release -o /app/build

# Stage 2: Publish
FROM build AS publish
RUN dotnet publish "MyProject.DbMigrator.csproj" -c Release -o /app/publish

# Stage 3: Runtime
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS final
WORKDIR /app

# Create non-root user
RUN adduser --disabled-password --gecos "" --uid 1000 appuser && \
    chown -R appuser:appuser /app

# Copy published output
COPY --from=publish /app/publish .

# Switch to non-root user
USER appuser

# Entry point
ENTRYPOINT ["dotnet", "MyProject.DbMigrator.dll"]
```

### Customizations Applied

Based on your project analysis, the skill:

1. **Detects project structure:**
   - Parses `.csproj` to extract project name, target framework
   - Identifies all project references (recursive dependency tree)
   - Detects NuGet packages used (for base image selection)

2. **Adapts to environment:**
   - `--environment Development` → includes debug symbols, detailed logs
   - `--environment Production` → strips symbols, minimal logging
   - `--no-multi-stage` → single stage for simpler deployments

3. **Configures health checks:**
   - If migrations succeed → exit code 0
   - If migrations fail → exit code 1
   - Optional: `/health` endpoint if using web host (not for DbMigrator)

4. **Optimizes image size:**
   - Multi-stage build reduces final image to ~200MB (vs ~1GB SDK image)
   - `.dockerignore` excludes bin/, obj/, .git/, test files
   - Nerdctl/BuildKit cache optimization

## docker-compose.yml Template

```yaml
version: '3.8'

services:
  db-migrator:
    build:
      context: ..
      dockerfile: src/MyProject.DbMigrator/Dockerfile
    image: myproject/db-migrator:latest
    container_name: myproject-db-migrator
    restart: "no"  # One-off task, don't restart
    depends_on:
      - postgres
    environment:
      - ASPNETCORE_ENVIRONMENT=Production
      - ConnectionStrings__Default=Host=postgres;Port=5432;Database=myproject;User ID=postgres;Password=${DB_PASSWORD}
      - Redis__Configuration=redis:6379
      - CLIENT=MBL  # Optional: client-specific configuration
    volumes:
      - ./logs:/app/Logs
      - ../appsettings.json:/app/appsettings.json:ro
      - ../appsettings.Production.json:/app/appsettings.Production.json:ro
    networks:
      - backend
    # For one-off execution, use:
    # command: ["dotnet", "MyProject.DbMigrator.dll"]
    # Or with entrypoint already in Dockerfile, just:
    # (no command needed)

networks:
  backend:
    driver: bridge

volumes:
  postgres_data:
```

### Key Features

- **Depends on database**: Waits for PostgreSQL to be ready (use `healthcheck`)
- **Environment variables**: Secure injection of connection strings
- **Volume mounts**: Persistent logs, config overrides
- **Restart policy**: `"no"` for one-off tasks (use `on-failure` for retries)
- **Network isolation**: Dedicated backend network

## Kubernetes Manifests

### Job Manifest

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: myproject-db-migrator
  namespace: myproject
spec:
  backoffLimit: 3
  template:
    spec:
      restartPolicy: OnFailure
      containers:
      - name: db-migrator
        image: myproject/db-migrator:v1.0.0
        imagePullPolicy: IfNotPresent
        env:
        - name: ASPNETCORE_ENVIRONMENT
          value: Production
        - name: ConnectionStrings__Default
          valueFrom:
            secretKeyRef:
              name: myproject-secrets
              key: database-connection
        - name: Redis__Configuration
          value: "redis-master:6379"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

### CronJob Manifest

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: myproject-db-migrator
  namespace: myproject
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM
  jobTemplate:
    spec:
      backoffLimit: 3
      template:
        spec:
          restartPolicy: OnFailure
          containers:
          - name: db-migrator
            image: myproject/db-migrator:v1.0.0
            # ... same as Job above
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Database Migration

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  migrate:
    runs-on: ubuntu-latest
    environment: ${{ github.ref == 'refs/heads/main' && 'production' || 'staging' }}
    steps:
    - uses: actions/checkout@v3

    - name: Setup .NET
      uses: actions/setup-dotnet@v3
      with:
        dotnet-version: '8.0.x'

    - name: Build Docker image
      run: |
        docker build -t myproject/db-migrator:${{ github.sha }} \
          -f src/MyProject.DbMigrator/Dockerfile .

    - name: Run migration
      run: |
        docker run --rm \
          -e ConnectionStrings__Default="${{ secrets.DB_CONNECTION_STRING }}" \
          -e ASPNETCORE_ENVIRONMENT=${{ github.ref == 'refs/heads/main' && 'Production' || 'Staging' }} \
          myproject/db-migrator:${{ github.sha }}
```

## Configuration Detection

The skill automatically detects from your `.csproj`:

```xml
<!-- Detects: -->
<TargetFramework>net8.0</TargetFramework>
<!-- RUNTIME: aspnet:8.0 -->

<PackageReference Include="Volo.Abp.Autofac" Version="8.3.4" />
<!-- FRAMEWORK: ABP Framework -->

<ProjectReference Include="..\MyProject.EntityFrameworkCore\MyProject.EntityFrameworkCore.csproj" />
<!-- DEPENDENCY: EntityFrameworkCore module -->
```

### Project Reference Tree Analysis

The skill parses the dependency tree:

```
MyProject.DbMigrator.csproj
├─ MyProject.EntityFrameworkCore.csproj
│  ├─ MyProject.Domain.csproj
│  └─ MyProject.Domain.Shared.csproj
├─ MyProject.Application.Contracts.csproj
│  └─ MyProject.Application.csproj
└─ MyProject.HttpApi.csproj
```

All referenced projects are copied in Docker build context.

## Environment-Specific Configurations

### Development
- Use `docker-compose.override.yml` for hot reload
- Mount source code for debugging
- Detailed Serilog logging (Debug level)
- Expose logs to host

```yaml
# docker-compose.override.yml
version: '3.8'
services:
  db-migrator:
    volumes:
      - ./src:/src  # Mount source for debugging
    environment:
      - ASPNETCORE_ENVIRONMENT=Development
      - Logging__LogLevel__Default=Debug
```

### Production
- Minimal logging (Information level)
- No volume mounts (immutable)
- Resource limits enforced
- Readiness/liveness probes (if Job with sidecar)
- Security context (non-root, no capabilities)

### Staging
- Mirrors production but with verbose logging
- Alerting on migration failures
- Pre/post migration hooks

## Security Best Practices

### 1. Non-Root User
```dockerfile
RUN adduser --disabled-password --gecos "" --uid 1000 appuser
USER appuser
```

### 2. Secret Management
```bash
# Don't hardcode in Dockerfile or docker-compose.yml
# Use:
# - Docker secrets (Swarm)
# - Kubernetes secrets
# - Environment variables from CI/CD
# - HashiCorp Vault/Azure Key Vault integration
```

### 3. Image Scanning
```bash
# Scan for vulnerabilities
docker scan myproject/db-migrator:latest

# Use trusted base images only
FROM mcr.microsoft.com/dotnet/aspnet:8.0  # ✓ Official Microsoft
```

### 4. Resource Limits
```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

## Configuration File Handling

### Strategy: ConfigMap + Secrets (K8s)

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: db-migrator-config
data:
  appsettings.json: |
    {
      "App": { "SelfUrl": "https://localhost" },
      "ConnectionStrings": {
        "Default": "Host=postgres;Port=5432;Database=myproject;"
      }
    }

---
apiVersion: v1
kind: Secret
metadata:
  name: db-migrator-secrets
type: Opaque
stringData:
  ConnectionStrings__Default: "postgres://...password..."
```

Mount in Job:
```yaml
volumeMounts:
- name: config
  mountPath: /app/appsettings.json
  subPath: appsettings.json
```

### Strategy: Environment Variables (Docker Compose)

```bash
# .env file (DO NOT COMMIT)
DB_PASSWORD=super-secret-password
```

```yaml
environment:
  - ConnectionStrings__Default=Host=postgres;Port=5432;Database=myproject;User ID=postgres;Password=${DB_PASSWORD}
```

## Multi-Client Support

Your DbMigrator appears to support multiple clients (MBL, NCELL). The skill can generate:

### Client-Specific Docker Configs

```bash
/dbmigrator-docker-config --client MBL --tag v1.0.0-mbl
```

Generates:
- Image: `myproject/db-migrator:mbl-v1.0.0`
- Environment: `CLIENT=MBL`
- Config: mounts `appsettings.Staging.MBL.json`

### Multi-Client docker-compose.yml

```yaml
version: '3.8'

services:
  db-migrator-mbl:
    build:
      context: ..
      dockerfile: src/MyProject.DbMigrator/Dockerfile
    image: myproject/db-migrator:mbl-latest
    environment:
      - CLIENT=MBL
      - ASPNETCORE_ENVIRONMENT=Staging
    # ...

  db-migrator-ncell:
    build:
      context: ..
      dockerfile: src/MyProject.DbMigrator/Dockerfile
    image: myproject/db-migrator:ncell-latest
    environment:
      - CLIENT=NCELL
      - ASPNETCORE_ENVIRONMENT=Staging
    # ...
```

## Migration Execution Patterns

### Pattern 1: One-Off Manual Run
```bash
docker run --rm \
  -e ConnectionStrings__Default="${DB_CONNECTION}" \
  myproject/db-migrator:latest
```

### Pattern 2: Scheduled with Cron
```bash
# Using cron on host (not recommended for distributed systems)
docker run --rm myproject/db-migrator:latest && echo "Migration completed at $(date)" >> /var/log/db-migrate.log

# Better: Kubernetes CronJob
```

### Pattern 3: Pre-Deployment Hook
```yaml
# In your application's deployment pipeline:
- name: Run database migrations
  run: |
    docker run --rm \
      -e ConnectionStrings__Default="${{ secrets.DB_CONNECTION }}" \
      myproject/db-migrator:${{ github.sha }}
  env:
    DB_CONNECTION: ${{ secrets.DB_CONNECTION }}
```

### Pattern 4: Rolling Update Coordination
```yaml
# InitContainer in Kubernetes Deployment
initContainers:
- name: db-migrator
  image: myproject/db-migrator:v1.0.0
  command: ["dotnet", "MyProject.DbMigrator.dll"]
  env:
  - name: ConnectionStrings__Default
    valueFrom:
      secretKeyRef:
        name: db-secret
        key: connection-string
```

## Troubleshooting

### Issue: "Unable to connect to database"
**Check:**
1. Connection string format (use `Host:Port` not `Server:Port`)
2. Database server accessibility (network, firewall)
3. Credentials validity
4. Environment variable injection (use `docker exec <container> env`)

**Fix:**
```bash
# Test connection from inside container
docker run --rm \
  -e ConnectionStrings__Default="Host=host.docker.internal;Port=5432;..." \
  myproject/db-migrator:latest \
  dotnet MyProject.DbMigrator.dll --dry-run
```

### Issue: "Missing appsettings.json"
**Cause:** Config file not mounted or copied.
**Fix:**
```dockerfile
# Ensure COPY in Dockerfile includes all configs
COPY ["appsettings.json", "./"]
COPY ["appsettings.Production.json", "./"]
```

Or mount at runtime:
```bash
docker run -v $(pwd)/appsettings.json:/app/appsettings.json:ro ...
```

### Issue: "Permission denied on logs"
**Cause:** Container user can't write to mounted volume.
**Fix:**
```bash
# Ensure host directory is writable by container user (UID 1000)
sudo chown -R 1000:1000 ./logs

# Or don't mount logs (let container log to stdout)
docker run --rm -v /dev/null:/app/Logs ...
```

### Issue: "Migrations take too long, timeout"
**Fix:**
1. Increase timeout in connection string: `Timeout=300;`
2. Increase container resources (CPU/memory)
3. Run migrations during maintenance window
4. Split large migrations into smaller batches (if possible)

## Skill Output Format

```
Docker Configuration Generator for DbMigrator
Project: MyProject.DbMigrator
Framework: .NET 8.0
ABP: Yes

📋 Detected:
   • Target Framework: net8.0
   • Project References: 6 modules
   • Redis Support: Yes
   • Multi-Client: Yes (MBL, NCELL)

Generating: Dockerfile, docker-compose.yml, .env.example, .dockerignore

✓ Dockerfile created (multi-stage, 41 lines)
✓ docker-compose.yml created (with volumes, networks)
✓ .env.example created (template for secrets)
✓ .dockerignore created (optimizes build context)

⚠ Manual Steps Required:
   1. Review ConnectionStrings__Default in .env.example
   2. Set CLIENT environment variable if using multi-tenant
   3. Add to .gitignore: .env, logs/, docker/.env
   4. Build image: docker build -f src/MyProject.DbMigrator/Dockerfile .
   5. Test: docker compose up db-migrator

📁 Output Directory: ./docker
⏱ Estimated time: 5 minutes
```

## Advanced Options

### Custom Base Image
```bash
/dbmigrator-docker-config --base-image mcr.microsoft.com/dotnet/aspnet:8.0-alpine
```
Produces smaller Alpine-based image (~150MB vs 200MB), but ensure native dependencies compatible.

### Health Check
```bash
/dbmigrator-docker-config --health-check
```
Adds:
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD dotnet MyProject.DbMigrator.dll --health || exit 1
```

### Build Arguments
```bash
/dbmigrator-docker-config --build-arg "HTTP_PROXY=http://proxy:8080" --build-arg "HTTPS_PROXY=http://proxy:8080"
```
For builds behind corporate proxy.

## Comparison: Manual vs Skill

| Aspect | Manual Dockerization | Using This Skill |
|--------|---------------------|------------------|
| **Multi-stage setup** | Need to research best practices | Automatic, optimized |
| **Project references** | Easy to miss dependencies | All detected automatically |
| **Non-root user** | Often forgotten | Always included |
| **Health check** | Manual addition | Optional with `--health-check` |
| **Environment-specific** | Create multiple Dockerfiles | Single Dockerfile, compose overrides |
| **Security** | Might run as root | Non-root by default |
| **CI/CD integration** | Copy-paste from docs | Generated templates ready to use |
| **Time** | 30-60 minutes | 2 minutes |

## Project-Specific Adaptations

### If Your DbMigrator Has Additional Dependencies:

**Custom NuGet packages:**
```dockerfile
# Add before COPY . .
COPY ["lib/", "lib/"]  # For local package feeds
```

**External tools (psql, etc.):**
```dockerfile
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS final
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*
```

**Native libraries:**
```dockerfile
RUN apt-get update && apt-get install -y \
    libgdiplus \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/*
```

## Validation Checklist

After generating Docker configs:

- [ ] Dockerfile builds successfully: `docker build -t test .`
- [ ] Image size reasonable (< 500MB for final stage)
- [ ] Container runs without errors: `docker run --rm test`
- [ ] Migrations execute successfully (check DB)
- [ ] Logs output to stdout/stderr: `docker logs <container>`
- [ ] Environment variables work: override config with env
- [ ] Multi-stage build cache works (don't rebuild entire solution)
- [ ] Non-root user has necessary permissions
- [ ] Health check passes (if enabled)
- [ ] docker-compose up works (if generated)

## Best Practices

1. **Use specific tags** (not `latest`) for production:
   ```bash
   --tag v1.2.3 --tag stable --tag production
   ```

2. **Leverage build cache**:
   ```dockerfile
   # Copy csproj files first, restore, then copy rest
   # This caches restore layer unless dependencies change
   ```

3. **Scan for vulnerabilities**:
   ```bash
   docker scan myproject/db-migrator:latest
   ```

4. **Test migration rollback**:
   ```bash
   # Run migration, then test downgrade
   docker run --rm myproject/db-migrator:latest --dry-run
   ```

5. **Document required env vars**:
   ```markdown
   ## Environment Variables
   - `ConnectionStrings__Default` (required)
   - `ASPNETCORE_ENVIRONMENT` (default: Production)
   - `CLIENT` (optional, for multi-tenant)
   ```

## Further Reading

- [ABP Framework Docker Documentation](https://docs.abp.io/en/abp/latest/Docker-Containers)
- [Microsoft .NET Docker Guide](https://learn.microsoft.com/en-us/dotnet/core/docker/)
- [Kubernetes Jobs and CronJobs](https://kubernetes.io/docs/concepts/workloads/controllers/job/)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/security/)

## Examples in This Repository

The existing `src/Amnil.AccessControlManagementSystem.DbMigrator/Dockerfile` is a good starting point but can be enhanced with:

- [ ] Multi-stage build optimization (separate restore, build, publish)
- [ ] Non-root user configuration
- [ ] Health check instruction
- [ ] Build arguments for version tagging
- [ ] docker-compose.yml for local testing
- [ ] Kubernetes manifests for production

Run the skill to generate these enhancements!

---

**Skill Version:** 1.0.0
**Last Updated:** 2025-03-12
**Compatible With:** ABP Framework 8.0+, .NET 8.0+, PostgreSQL