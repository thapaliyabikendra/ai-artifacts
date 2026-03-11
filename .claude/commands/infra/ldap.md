---
name: abp-ldap-login-integration
description: Implement or refine LDAP login integration for ABP projects using a custom authentication branch that preserves the ABP default login pipeline and keeps LDAP login separate from LDAP sync or provisioning. Use when Codex needs to add, debug, review, or modify LDAP-backed login behavior in an ABP solution without switching to the ABP Pro LDAP module.
---

# ABP LDAP Login Integration

Implement LDAP login integration in an ABP solution by extending the existing authentication flow instead of replacing it.

**User request**: $ARGUMENTS

## Pre-flight

- Read `CLAUDE.md` if it exists for repository conventions.
- Detect the solution layout before changing code.
- Locate the authentication entrypoint, identity verification path, and any existing LDAP abstractions.

Typical search targets:

```bash
rg -n "LoginModel|SignInManager|PasswordSignInAsync|CheckPasswordAsync|IdentityUserManager" src test
rg -n "LDAP|Ldap|IsInternalUser|DistinguishedName|DN" src test
rg --files -g "*AuthServer*.cs" -g "*HttpApi.Host*.cs" -g "*.Domain*.csproj" -g "*EntityFrameworkCore*.csproj"
```

## Objective

Preserve the ABP default login pipeline while inserting a custom LDAP authentication branch for external users only.

Target behavior:

1. Respect `LDAP:Enable`.
2. Keep internal users on local password validation.
3. Authenticate external users against LDAP.
4. Require stored LDAP identity data such as `DN` for LDAP-authenticated users.
5. Keep LDAP login separate from LDAP sync, user import, role mapping, and provisioning unless explicitly requested.

## Architecture Rules

- Do not replace the login UI, login endpoint, or ABP page model unless the repository already does that.
- Prefer extending the identity verification layer instead of rewriting the top-level login flow.
- Keep ABP lockout, audit, security stamp, external login, and password sign-in behavior intact.
- Do not introduce new feature flags unless the repository already uses them for auth customization.
- Do not silently create or sync users from LDAP unless the user explicitly requests provisioning.
- Detect actual implementation points from the repository; do not assume fixed namespaces or paths.

## Workflow

### 1. Verify Project Structure

Identify the relevant projects and files:

- `*.AuthServer` or `*.IdentityServer`
- `*.HttpApi.Host` if login or claims flow is split
- `*.Domain` for user properties and constants
- `*.EntityFrameworkCore` or equivalent integration layer for DI wiring

If the solution structure differs from standard ABP tiered layout, follow the repository's auth path instead of forcing the standard one.

### 2. Trace the Authentication Flow

Find the effective runtime path for username/password login:

1. Login endpoint or page model
2. `SignInManager` call site
3. `IdentityUserManager` password verification path
4. Any existing custom auth manager, LDAP service, or user property helpers

Document where each step happens before editing code.

### 3. Identify the LDAP Branch Point

Prefer a customization point that keeps the existing sign-in flow unchanged for callers.

Good options:

- Custom `IdentityUserManager`
- Existing auth manager abstraction already used by the solution
- A narrowly scoped override used by login only

Avoid:

- Replacing the entire login controller or Razor page just to add LDAP
- Duplicating ABP sign-in logic in a new top-level login handler

### 4. Implement the Authentication Decision

Use this decision tree:

```text
if LDAP:Enable is false:
    use base/local password verification
else if user is internal:
    use base/local password verification
else:
    require DN
    authenticate against LDAP
```

Implementation requirements:

- Determine internal vs external users from the repository's actual model, typically `IsInternalUser`.
- Read the LDAP identity field from the existing model, typically `DN`.
- Fail clearly when an external user is marked for LDAP login but has no DN.
- Route local-password users through the original ABP/base verification method.
- Route LDAP users through a dedicated LDAP manager or service abstraction.
- Preserve repository-specific error handling and localization patterns.

### 5. Wire Services and Configuration

Confirm or add only the minimum required configuration keys:

- `LDAP:Enable`
- `LDAP:Host`
- `LDAP:Port`
- `LDAP:BindDn` or bind username
- `LDAP:BindPassword`
- `LDAP:SearchBase`
- `LDAP:SearchFilter`
- `LDAP:UseSsl` or `LDAP:UseTls`

If the repository already uses different key names, keep the existing naming convention instead of normalizing it.

Confirm DI wiring for:

- Custom `IdentityUserManager` override, if used
- LDAP manager/service abstraction
- Any option classes or configuration binding already used by the repo

### 6. Verify End-to-End Behavior

Run the narrowest relevant verification available:

- Build the affected solution or projects
- Run auth-related tests if present
- Add or update tests when the repository already has coverage in this area

Manual verification should cover:

1. Internal user login still works with local password.
2. External LDAP user login succeeds with valid LDAP credentials.
3. External LDAP user login fails with invalid LDAP credentials.
4. External LDAP user without `DN` fails with a clear, non-silent error path.
5. Disabling `LDAP:Enable` restores local-password behavior.

## Implementation Guidance

### Preferred Pattern

Use a custom authentication branch inside the existing identity verification flow. Keep the ABP login pipeline intact and let callers continue using the same sign-in method they already call.

### Data Expectations

Common repository fields:

- `IsInternalUser`
- `DN`

If the repository uses different names, map to those fields instead of introducing duplicates.

### Fallback Policy

Use local password verification when:

- LDAP is disabled
- The user is classified as internal
- The repository explicitly allows fallback and the user is not intended for LDAP

Do not add fallback from LDAP failure to local-password success for external users unless the repository already does this or the user explicitly requests it.

### Error Handling

Keep behavior aligned with existing auth semantics:

- Return the same style of auth failure used by the repository
- Avoid leaking LDAP infrastructure details to end users
- Log enough detail for operators to diagnose bind/search failures

## Output Contract

When reporting completion, include:

- `Summary`: one-line outcome
- `Detected Authentication Flow`: login entrypoint and verification path
- `Files Modified`: exact changed files
- `LDAP Login Logic`: final decision branch and fallback policy
- `Configuration Keys`: required, existing, added, and missing keys
- `Verification`: commands run, tests run, and manual checks covered
- `Risks or Follow-ups`: only if something remains incomplete or repository constraints limited the implementation

## Checkpoint

- [ ] Authentication entrypoint identified
- [ ] Identity verification branch identified
- [ ] LDAP integration point identified
- [ ] Internal vs external user rule confirmed
- [ ] `DN` handling confirmed
- [ ] LDAP configuration keys validated
- [ ] Code changes implemented without replacing the ABP login pipeline
- [ ] Build or relevant tests executed when available
- [ ] Manual verification steps documented

## Troubleshooting

### LDAP branch never executes

Check:

- `LDAP:Enable` binding
- The actual service registered in DI
- Whether the overridden manager is the one the login flow really resolves

### Internal users start failing login

Check:

- The internal/external classification logic
- Whether local-password users still call the base verification path

### External users always fail

Check:

- `DN` presence and correctness
- LDAP bind credentials and search base
- TLS/SSL settings
- Whether the LDAP manager expects username vs DN during bind

### Login flow changed too much

If the implementation requires rewriting controller or page-model logic, step back and move the customization lower into the identity verification layer unless the repository already uses a custom top-level auth flow.
