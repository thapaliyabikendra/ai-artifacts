# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Clinic Management System** - a layered monolith application built on **ABP Framework** using Domain Driven Design (DDD). The system manages patients, appointments, and doctor schedules for a local clinic.

**Tech Stack**: .NET 10, ABP Framework 10.0.1, Entity Framework Core, PostgreSQL, Redis, OpenIddict (OAuth 2.0)

## Repository Structure

```
ai-artifacts/
├── api/                    # .NET Backend (ABP Framework)
│   ├── src/               # Source projects
│   └── test/              # Test projects
├── ui/                    # Frontend (Angular - not yet implemented)
├── docs/                  # Business requirements documentation
└── .claude/skills/        # Claude Code skills for this project
```

## Build Commands

All commands should be run from `api/` directory:

```bash
# Build solution
dotnet build ClinicManagementSystem.slnx

# Run API host
dotnet run --project src/ClinicManagementSystem.HttpApi.Host

# Run AuthServer
dotnet run --project src/ClinicManagementSystem.AuthServer

# Run database migrations
dotnet run --project src/ClinicManagementSystem.DbMigrator

# Run all tests
dotnet test

# Run specific test project
dotnet test test/ClinicManagementSystem.Application.Tests
```

## ABP Framework Architecture

### Layer Dependencies (bottom to top)
```
Domain.Shared → Domain → EntityFrameworkCore
                ↓
Application.Contracts → Application → HttpApi → HttpApi.Host
                                  ↓
                           HttpApi.Client
```

### Project Responsibilities

| Layer | Purpose |
|-------|---------|
| `Domain.Shared` | Enums, constants, localization resources shared across all layers |
| `Domain` | Entities, aggregate roots, domain services, repository interfaces |
| `Application.Contracts` | DTOs, application service interfaces |
| `Application` | Application services implementing business logic |
| `HttpApi` | API controllers, REST endpoints |
| `HttpApi.Host` | API startup, configuration, dependency injection |
| `EntityFrameworkCore` | EF Core DbContext, repository implementations, migrations |
| `AuthServer` | OAuth 2.0 authentication server (OpenIddict) |
| `DbMigrator` | Database migration console app |

### Key ABP Patterns

- **AppServices**: Inherit from `ApplicationService` or implement `IApplicationService`
- **DTOs**: Use `CreateUpdateDtoBase`, `EntityDto<TKey>` patterns
- **Validation**: FluentValidation with ABP integration
- **AutoMapper**: Configure in `*ApplicationAutoMapperProfile.cs`
- **Permissions**: Define in `*Permissions.cs`, grant in module configuration

## Domain Entities

- **Patient**: FirstName, LastName, Email, Phone, DateOfBirth
- **Doctor**: FullName, Specialization, Email, Phone
- **Appointment**: PatientId, DoctorId, AppointmentDate, Description, Status
- **DoctorSchedule**: DoctorId, DayOfWeek, StartTime, EndTime

Roles: Admin (full control), Doctor (view own appointments/patients), Receptionist (create patients, schedule appointments)

## Available Skills

The `.claude/skills/` directory contains specialized skills:

- **crud-service**: Generate ABP CRUD services with DTOs, validators, and AppServices
- **docker-dotnet-containerize**: Create optimized Dockerfiles for .NET projects
- **distributed-event-bus**: Implement RabbitMQ event handlers following ABP patterns
- **skill-creator**: Guide for creating new Claude skills

## Prerequisites

- .NET 10.0+ SDK
- Node v20.11+ (for AuthServer client libraries)
- Redis (for distributed caching)
- PostgreSQL

Before first run:
1. Run `abp install-libs` in AuthServer directory for client libraries
2. Run DbMigrator to create database and seed initial data
