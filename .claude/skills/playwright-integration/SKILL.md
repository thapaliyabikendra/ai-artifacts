---
name: playwright-integration
description: Dynamic Playwright E2E testing assistant that adapts to any project type (React, Vue, Angular, Svelte, Next.js, Nuxt, or any web framework). Auto-detects build tools, routing, authentication, and provides tailored setup guidance. **CRITICAL: Never uses hardcoded credentials - always prompts user for valid URLs, environment, and real test credentials before generating login tests.** Use when: (1) setting up Playwright in a new project, (2) configuring Playwright for specific frameworks, (3) debugging framework-specific E2E testing issues, (4) optimizing selectors for React/Vue/Angular components, (5) handling authentication flows in tests (OIDC, JWT, sessions) with proper credential validation.
---

# Playwright Integration Skill

Dynamic, framework-agnostic Playwright assistant for any web project.

## Command

```
/playwright-integration
```

## What It Does

Auto-detects your web framework and provides tailored Playwright setup:

- **Framework Detection**: React, Vue, Angular, Svelte, Next.js, Nuxt, Solid, Qwik
- **Build Tool Detection**: Vite, Webpack, Rspack, Angular CLI, Next.js CLI, Nuxt CLI
- **Routing Detection**: React Router, Vue Router, Angular Router, file-based routing
- **Auth Pattern Detection**: OIDC, JWT, NextAuth, session-based, custom
- **UI Library Detection**: MUI, AntD, Tailwind, Bootstrap, Element Plus, etc.

## Pre-Generation Validation Phase (MANDATORY)

**Before generating ANY test code, you MUST gather:**

1. **Environment**: dev / staging / prod
2. **Base URL**: Full application URL (e.g., `http://localhost:4200`, `https://app-dev.example.com`)
3. **Credentials**: Valid username/password (or API keys) for authentication tests
   - ASK: "Please provide a valid username and password for the [ENVIRONMENT] environment"
   - NEVER use placeholder values like 'test@example.com' or 'password123'
4. **Auth bypass**: Does your backend provide test auth endpoints (e.g., `/api/auth/test-login`)?
5. **Test data**: Are seeded test users/data available?

**Validation Checklist** (complete before code generation):
- [ ] Base URL is reachable and correct for the target environment
- [ ] User-provided credentials work for manual login
- [ ] Authentication flow verified manually
- [ ] Test data/seeding strategy confirmed
- [ ] API bypass endpoints identified (if applicable)

## Usage

```bash
# Basic setup (auto-detects framework)
/playwright-integration setup

# Specific focus
/playwright-integration configure for React Next.js
/playwright-integration auth handling
/playwright-integration selectors
/playwright-integration debug flaky tests

# Override detection if needed
/playwright-integration --framework=react setup
```

## Example Responses

### React + Vite Project
```
📦 Detected: React 18 + TypeScript + Vite + MUI + React Router

Config recommendations:
- webServer.command: npm run dev (port 5173)
- Use RTL selectors: getByRole, getByTestId
- Add data-testid to MUI components
- Handle React StrictMode double renders
```

### Vue 3 + Nuxt
```
📦 Detected: Vue 3 + Nuxt 3 + Pinia + Vue Router

Config recommendations:
- webServer.command: nuxi dev
- Wait for Vue reactive updates
- Use Vue Test Utils patterns
- Handle file-based routes: pages/ → /
```

### Angular
```
📦 Detected: Angular 17 + Material + Router

Config recommendations:
- webServer.command: ng serve
- Prefer CSS selectors over RTL
- Handle change detection strategies
- Use Angular Material test IDs
```

## Parameters

- `action`: `setup`, `configure`, `auth`, `selectors`, `debug`, `optimize`
- `framework`: Override auto-detection (react, vue, angular, svelte, next, nuxt, other)
- `focus`: Area of focus (`auth`, `routing`, `selectors`, `state`, `performance`, `ci`)

## Benefits

✅ Works with ANY web framework
✅ Adapts to your existing setup
✅ Framework-specific best practices
✅ **Mandatory URL/credential validation**
✅ **Never uses hardcoded credentials**
✅ Practical, runnable examples

---

## Authentication Test Generation Rules

**HARD RULES (Non-negotiable):**

1. ❌ **NEVER** use hardcoded credentials like:
   - `'test@example.com'`
   - `'password123'`
   - `'admin' / 'admin123'`

2. ✅ **ALWAYS** ask user for:
   - Environment (dev/staging/prod)
   - Base URL (full application URL)
   - Valid credentials (username/password)
   - Auth bypass endpoint availability
   - Test user details

3. ✅ **Replace** all placeholders with `{{VARIABLE}}` markers:
   ```typescript
   const EMAIL = '{{USER_EMAIL}}'; // ASK USER
   const PASSWORD = '{{USER_PASSWORD}}'; // ASK USER
   ```

4. ✅ **Include** security warning: "Never commit real credentials"

5. ✅ **Suggest** environment variables or global setup for CI

**What to ask the user:**
```
To generate authentication tests, I need:
1. What environment? (dev/staging/prod)
2. Base URL? (e.g., http://localhost:4200)
3. Valid credentials? (email/username and password)
4. Test auth bypass endpoint? (y/n - if yes, provide path)
5. Seeded test users available? (y/n)
```

**If user cannot provide credentials:**
- Do NOT generate fake placeholder values
- Explain that tests will fail without valid credentials
- Offer to generate test structure without actual credential values
- Suggest implementing test auth bypass endpoint

---

For detailed documentation, see: `references/playwright-integration-detailed.md`
