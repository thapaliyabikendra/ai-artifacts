# React Code Review Examples

Code examples demonstrating patterns to look for during React/TypeScript reviews.

## Component Patterns

### Props and Typing

```tsx
// ❌ Bad - any type, no explicit props interface
const PatientCard = (props: any) => {
  const [data, setData] = useState();
  useEffect(() => {
    fetch('/api/patient').then(r => r.json()).then(setData);
  }, []);
  return <div onClick={props.onClick}>{data?.name}</div>;
};

// ✅ Good - typed props, React Query, semantic HTML
interface PatientCardProps {
  patientId: string;
  onClick: (id: string) => void;
}

const PatientCard: React.FC<PatientCardProps> = ({ patientId, onClick }) => {
  const { data, isLoading, error } = useQuery({
    queryKey: ['patient', patientId],
    queryFn: () => patientApi.get(patientId),
  });

  const handleClick = useCallback(() => {
    onClick(patientId);
  }, [patientId, onClick]);

  if (isLoading) return <Skeleton />;
  if (error) return <ErrorMessage error={error} />;

  return (
    <button
      onClick={handleClick}
      aria-label={`View patient ${data.name}`}
    >
      {data.name}
    </button>
  );
};
```

## Hooks Patterns

### Conditional Logic

```tsx
// ❌ Bad - hook in conditional
useEffect(() => {
  if (condition) {
    // Using hook conditionally
  }
}, []);

// ✅ Good - conditional inside hook or useMemo
const result = useMemo(() => {
  return condition ? computeValue() : defaultValue;
}, [condition]);
```

### Missing Cleanup

```tsx
// ❌ Bad - no cleanup for subscription
useEffect(() => {
  const subscription = eventEmitter.subscribe(handler);
}, []);

// ✅ Good - cleanup function returned
useEffect(() => {
  const subscription = eventEmitter.subscribe(handler);
  return () => subscription.unsubscribe();
}, []);
```

### Missing Dependencies

```tsx
// ❌ Bad - missing dependency
useEffect(() => {
  fetchData(userId);
}, []); // userId missing

// ✅ Good - complete dependencies
useEffect(() => {
  fetchData(userId);
}, [userId]);
```

## Type Patterns

### API Types

```tsx
// ❌ Bad - any and type casting
const handleSubmit = (data: any) => {
  api.post(data as PatientDto);
};

// ✅ Good - explicit types throughout
const handleSubmit = (data: CreatePatientDto): Promise<PatientDto> => {
  return api.post<PatientDto>('/patients', data);
};
```

### Null Handling

```tsx
// ❌ Bad - non-null assertion
const name = user!.name;

// ✅ Good - proper null check
const name = user?.name ?? 'Unknown';
```

## State Management Patterns

### Server State

```tsx
// ❌ Bad - useEffect for data fetching
const [patients, setPatients] = useState([]);
const [loading, setLoading] = useState(true);

useEffect(() => {
  setLoading(true);
  fetch('/api/patients')
    .then(r => r.json())
    .then(setPatients)
    .finally(() => setLoading(false));
}, []);

// ✅ Good - React Query
const { data: patients, isLoading } = useQuery({
  queryKey: ['patients'],
  queryFn: patientApi.getList,
});
```

### Derived State

```tsx
// ❌ Bad - useEffect for derived state
const [filteredItems, setFilteredItems] = useState([]);
useEffect(() => {
  setFilteredItems(items.filter(i => i.active));
}, [items]);

// ✅ Good - compute in render
const filteredItems = useMemo(
  () => items.filter(i => i.active),
  [items]
);
```

## Accessibility Patterns

### Semantic HTML

```tsx
// ❌ Bad - div with click handler
<div onClick={handleClick} className="btn">
  Save
</div>

// ✅ Good - semantic button
<button onClick={handleClick} type="button">
  Save
</button>
```

### ARIA Labels

```tsx
// ❌ Bad - icon-only button without label
<button onClick={onClose}>
  <XIcon />
</button>

// ✅ Good - accessible label
<button onClick={onClose} aria-label="Close dialog">
  <XIcon aria-hidden="true" />
</button>
```

### Form Labels

```tsx
// ❌ Bad - placeholder only
<input placeholder="Email" value={email} onChange={...} />

// ✅ Good - associated label
<label htmlFor="email">Email</label>
<input id="email" value={email} onChange={...} />
```

## Performance Patterns

### Callback Memoization

```tsx
// ❌ Bad - inline function recreated on each render
<ChildComponent onClick={() => handleClick(id)} />

// ✅ Good - memoized callback
const handleClickMemoized = useCallback(
  () => handleClick(id),
  [id]
);
<ChildComponent onClick={handleClickMemoized} />
```

### List Keys

```tsx
// ❌ Bad - index as key
{items.map((item, index) => (
  <Item key={index} data={item} />
))}

// ✅ Good - stable unique key
{items.map(item => (
  <Item key={item.id} data={item} />
))}
```

## Security Patterns

### XSS Prevention

```tsx
// ❌ Bad - dangerouslySetInnerHTML without sanitization
<div dangerouslySetInnerHTML={{ __html: userContent }} />

// ✅ Good - sanitized or avoided
import DOMPurify from 'dompurify';
<div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(userContent) }} />

// Or better - use text content when possible
<div>{userContent}</div>
```
