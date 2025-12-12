# API Mock Templates Reference

Templates for mock server implementation using MSW (Mock Service Worker) for Node.js/React.

## MSW Setup

### Installation

```bash
npm install msw --save-dev
```

### Mock Server Handler (Node.js)

```typescript
// mocks/handlers.ts
import { http, HttpResponse, delay } from 'msw';

// Define API mocks
export const handlers = [
    // GET list with pagination
    http.get('/api/patients', async ({ request }) => {
        const url = new URL(request.url);
        const page = parseInt(url.searchParams.get('page') || '1');
        const pageSize = parseInt(url.searchParams.get('pageSize') || '20');

        await delay(100); // Simulate network latency

        return HttpResponse.json({
            items: generatePatients(pageSize, page),
            totalCount: 150,
            pageNumber: page,
            pageSize: pageSize,
        });
    }),

    // GET single resource
    http.get('/api/patients/:id', async ({ params }) => {
        const { id } = params;

        if (id === 'not-found') {
            return HttpResponse.json(
                { error: { code: 'NOT_FOUND', message: 'Patient not found' } },
                { status: 404 }
            );
        }

        return HttpResponse.json({
            id,
            name: 'John Doe',
            email: 'john@example.com',
            status: 'Active',
        });
    }),

    // POST create resource
    http.post('/api/patients', async ({ request }) => {
        const body = await request.json();

        // Simulate validation error
        if (!body.email) {
            return HttpResponse.json(
                { error: { code: 'VALIDATION_ERROR', details: [{ field: 'email', message: 'Email is required' }] } },
                { status: 422 }
            );
        }

        return HttpResponse.json(
            { id: crypto.randomUUID(), ...body },
            { status: 201 }
        );
    }),

    // PUT update resource
    http.put('/api/patients/:id', async ({ params, request }) => {
        const { id } = params;
        const body = await request.json();

        return HttpResponse.json({ id, ...body });
    }),

    // DELETE resource
    http.delete('/api/patients/:id', async ({ params }) => {
        return new HttpResponse(null, { status: 204 });
    }),
];
```

### Server Setup (Node.js/Integration Tests)

```typescript
// mocks/server.ts
import { setupServer } from 'msw/node';
import { handlers } from './handlers';

export const server = setupServer(...handlers);

// Jest/Vitest setup
// setupTests.ts
import { server } from './mocks/server';

beforeAll(() => server.listen({ onUnhandledRequest: 'warn' }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

### Browser Setup (React Development)

```typescript
// mocks/browser.ts
import { setupWorker } from 'msw/browser';
import { handlers } from './handlers';

export const worker = setupWorker(...handlers);

// Start in development
// main.tsx
async function enableMocking() {
    if (process.env.NODE_ENV !== 'development') return;

    const { worker } = await import('./mocks/browser');
    return worker.start({ onUnhandledRequest: 'bypass' });
}

enableMocking().then(() => {
    // Render app
});
```

---

## Test Data Generation

```typescript
// mocks/generators.ts
import { faker } from '@faker-js/faker';

interface Patient {
    id: string;
    name: string;
    email: string;
    dateOfBirth: string;
    status: 'Active' | 'Inactive';
}

export function generatePatient(overrides?: Partial<Patient>): Patient {
    return {
        id: faker.string.uuid(),
        name: faker.person.fullName(),
        email: faker.internet.email(),
        dateOfBirth: faker.date.birthdate({ min: 18, max: 80, mode: 'age' }).toISOString(),
        status: faker.helpers.arrayElement(['Active', 'Inactive']),
        ...overrides,
    };
}

export function generatePatients(count: number, page: number = 1): Patient[] {
    // Consistent data using seeded random
    faker.seed(page * 1000);
    return Array.from({ length: count }, () => generatePatient());
}

// Scenario-specific generators
export const testScenarios = {
    emptyList: () => [],
    singleItem: () => [generatePatient()],
    largeList: () => generatePatients(100, 1),
    withInactive: () => [
        ...generatePatients(5, 1),
        generatePatient({ status: 'Inactive' }),
    ],
};
```

---

## Scenario-Based Mocking

```typescript
// mocks/scenarios.ts
import { http, HttpResponse, delay } from 'msw';

export const errorScenarios = {
    // Server error
    serverError: http.get('/api/*', () => {
        return HttpResponse.json(
            { error: { code: 'INTERNAL_ERROR', message: 'Internal Server Error' } },
            { status: 500 }
        );
    }),

    // Network timeout
    timeout: http.get('/api/*', async () => {
        await delay('infinite');
    }),

    // Rate limiting
    rateLimited: http.get('/api/*', () => {
        return HttpResponse.json(
            { error: { code: 'RATE_LIMITED', message: 'Too many requests' } },
            { status: 429, headers: { 'Retry-After': '60' } }
        );
    }),

    // Unauthorized
    unauthorized: http.get('/api/*', () => {
        return HttpResponse.json(
            { error: { code: 'UNAUTHORIZED', message: 'Token expired' } },
            { status: 401 }
        );
    }),
};

export const performanceScenarios = {
    // Slow response
    slowResponse: http.get('/api/*', async (resolver) => {
        await delay(3000);
        return resolver; // Continue with normal handler
    }),

    // Degraded performance (intermittent slowness)
    degraded: http.get('/api/*', async (resolver) => {
        const delayMs = Math.random() > 0.7 ? 2000 : 100;
        await delay(delayMs);
        return resolver;
    }),
};
```

### Using Scenarios in Tests

```typescript
// __tests__/patients.test.tsx
import { server } from '../mocks/server';
import { errorScenarios } from '../mocks/scenarios';
import { render, screen, waitFor } from '@testing-library/react';
import { PatientList } from '../components/PatientList';

describe('PatientList', () => {
    it('displays patients on successful load', async () => {
        render(<PatientList />);

        await waitFor(() => {
            expect(screen.getByText('John Doe')).toBeInTheDocument();
        });
    });

    it('shows error message on server failure', async () => {
        server.use(errorScenarios.serverError);

        render(<PatientList />);

        await waitFor(() => {
            expect(screen.getByText(/failed to load/i)).toBeInTheDocument();
        });
    });

    it('shows loading state on slow network', async () => {
        server.use(errorScenarios.timeout);

        render(<PatientList />);

        expect(screen.getByRole('progressbar')).toBeInTheDocument();
    });
});
```

---

## Third-Party API Mocking

For mocking external services (payment gateways, email providers, etc.):

```typescript
// mocks/external-services.ts
import { http, HttpResponse } from 'msw';

export const stripeHandlers = [
    http.post('https://api.stripe.com/v1/payment_intents', async ({ request }) => {
        return HttpResponse.json({
            id: 'pi_mock_123',
            status: 'requires_payment_method',
            client_secret: 'pi_mock_123_secret_456',
            amount: 1000,
            currency: 'usd',
        });
    }),

    http.post('https://api.stripe.com/v1/payment_intents/:id/confirm', () => {
        return HttpResponse.json({
            id: 'pi_mock_123',
            status: 'succeeded',
        });
    }),
];

export const sendgridHandlers = [
    http.post('https://api.sendgrid.com/v3/mail/send', () => {
        return new HttpResponse(null, { status: 202 });
    }),
];

// Combine with app handlers
// mocks/handlers.ts
import { stripeHandlers, sendgridHandlers } from './external-services';

export const handlers = [
    ...appHandlers,
    ...stripeHandlers,
    ...sendgridHandlers,
];
```

---

## Response Sequencing

For testing retry logic and state transitions:

```typescript
// mocks/sequences.ts
import { http, HttpResponse } from 'msw';

// Fail twice, then succeed
let attemptCount = 0;

export const retrySequence = http.post('/api/orders', () => {
    attemptCount++;

    if (attemptCount <= 2) {
        return HttpResponse.json(
            { error: { code: 'TRANSIENT_ERROR' } },
            { status: 503 }
        );
    }

    attemptCount = 0; // Reset for next test
    return HttpResponse.json({ id: 'order-123', status: 'created' }, { status: 201 });
});

// Pagination sequence
export function createPaginatedHandler<T>(
    path: string,
    allItems: T[],
    pageSize: number = 20
) {
    return http.get(path, ({ request }) => {
        const url = new URL(request.url);
        const page = parseInt(url.searchParams.get('page') || '1');

        const start = (page - 1) * pageSize;
        const items = allItems.slice(start, start + pageSize);

        return HttpResponse.json({
            items,
            totalCount: allItems.length,
            pageNumber: page,
            pageSize,
            hasMore: start + pageSize < allItems.length,
        });
    });
}
```

---

## Docker Deployment for CI

```yaml
# docker-compose.test.yml
version: '3.8'
services:
  test-runner:
    build:
      context: .
      dockerfile: Dockerfile.test
    environment:
      - NODE_ENV=test
      - API_BASE_URL=http://localhost:3000
    command: npm run test:e2e
```

---

## Best Practices

1. **Keep handlers realistic** - Match actual API contracts
2. **Use faker for data** - Consistent, realistic test data
3. **Reset between tests** - Use `server.resetHandlers()` in afterEach
4. **Scenario isolation** - Each test should set up its own mocks
5. **Type safety** - Share types between handlers and app code
6. **Documentation** - Comment non-obvious mock behaviors

## Integration with Playwright

```typescript
// playwright/global-setup.ts
import { setupServer } from 'msw/node';
import { handlers } from '../mocks/handlers';

const server = setupServer(...handlers);

export default async function globalSetup() {
    server.listen();
}

export default async function globalTeardown() {
    server.close();
}
```
