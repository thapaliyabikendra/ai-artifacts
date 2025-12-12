# Async/Await Patterns

## Asynchronous Programming Guidelines

| Name | Description | Exceptions |
|------|-------------|------------|
| **Avoid async void** | Prefer `async Task` methods over `async void` | Event handlers only |
| **Async all the way** | Don't mix blocking and async code | Console main (C# <= 7.0) |
| **Configure context** | Use `ConfigureAwait(false)` when you can | Methods requiring context |

---

## The Async Way of Doing Things

| To Do This... | Instead of This... | Use This |
|---------------|-------------------|----------|
| Retrieve result of background task | `Task.Wait` or `Task.Result` | `await` |
| Wait for any task to complete | `Task.WaitAny` | `await Task.WhenAny` |
| Retrieve results of multiple tasks | `Task.WaitAll` | `await Task.WhenAll` |
| Wait a period of time | `Thread.Sleep` | `await Task.Delay` |

---

## Best Practices

### I/O Bound vs CPU Bound

```csharp
// ✅ Async/Await is BEST for I/O bound tasks
// - Network calls
// - Database queries
// - File operations
public async Task<Patient> GetPatientAsync(Guid id)
{
    return await _repository.GetAsync(id);
}

// ⚠️ For CPU-bound tasks, use Task.Run
// - Complex calculations
// - Image processing
// - Large data transformations
public async Task<ReportData> GenerateReportAsync()
{
    return await Task.Run(() => ComputeHeavyReport());
}
```

### Avoid These Anti-Patterns

```csharp
// ❌ Bad - Blocking on async (can deadlock!)
public Patient GetPatient(Guid id)
{
    return _repository.GetAsync(id).Result;  // BLOCKS!
}

// ❌ Bad - Async void (except event handlers)
public async void SavePatient(Patient patient)
{
    await _repository.InsertAsync(patient);  // Fire and forget - exceptions lost!
}

// ✅ Good
public async Task<Patient> GetPatientAsync(Guid id)
{
    return await _repository.GetAsync(id);
}

public async Task SavePatientAsync(Patient patient)
{
    await _repository.InsertAsync(patient);
}
```

---

## Solutions to Common Async Problems

| Problem | Solution |
|---------|----------|
| Create a task to execute code | `Task.Run` or `TaskFactory.StartNew` (NOT `Task` constructor) |
| Create task wrapper for operation/event | `TaskCompletionSource<T>` |
| Support cancellation | `CancellationTokenSource` and `CancellationToken` |
| Report progress | `IProgress<T>` and `Progress<T>` |
| Handle streams of data | TPL Dataflow or Reactive Extensions |
| Synchronize access to shared resource | `SemaphoreSlim` |
| Asynchronously initialize a resource | `AsyncLazy<T>` |

---

## Migration from Blocking to Async

| Old (Blocking) | New (Async) | Description |
|----------------|-------------|-------------|
| `task.Wait` | `await task` | Wait for task to complete |
| `task.Result` | `await task` | Get result of completed task |
| `Task.WaitAny` | `await Task.WhenAny` | Wait for any task |
| `Task.WaitAll` | `await Task.WhenAll` | Wait for all tasks |
| `Thread.Sleep` | `await Task.Delay` | Wait for period |
| `Task` constructor | `Task.Run` | Create code-based task |

---

## Parallel Execution Pattern

```csharp
// ❌ Bad - Sequential execution
var patient = await _patientRepository.GetAsync(patientId);
var doctor = await _doctorRepository.GetAsync(doctorId);
var appointments = await _appointmentRepository.GetListAsync();
// Total time = patient + doctor + appointments

// ✅ Good - Parallel execution
var patientTask = _patientRepository.GetAsync(patientId);
var doctorTask = _doctorRepository.GetAsync(doctorId);
var appointmentsTask = _appointmentRepository.GetListAsync();

await Task.WhenAll(patientTask, doctorTask, appointmentsTask);

var patient = await patientTask;
var doctor = await doctorTask;
var appointments = await appointmentsTask;
// Total time = max(patient, doctor, appointments)
```

---

## ConfigureAwait Usage

```csharp
// In library code (no UI context needed)
public async Task<string> GetDataAsync()
{
    var data = await _httpClient.GetStringAsync(url)
        .ConfigureAwait(false);  // Don't capture context
    return ProcessData(data);
}

// In UI code (need UI context)
public async Task UpdateUIAsync()
{
    var data = await GetDataAsync();  // Captures context
    lblStatus.Text = data;  // Must run on UI thread
}
```

---

## Cancellation Pattern

```csharp
public async Task<List<Patient>> GetPatientsAsync(
    CancellationToken cancellationToken = default)
{
    var patients = new List<Patient>();

    await foreach (var patient in _repository.GetAllAsync())
    {
        cancellationToken.ThrowIfCancellationRequested();
        patients.Add(patient);
    }

    return patients;
}

// Usage
var cts = new CancellationTokenSource(TimeSpan.FromSeconds(30));
try
{
    var patients = await GetPatientsAsync(cts.Token);
}
catch (OperationCanceledException)
{
    _logger.LogWarning("Operation was cancelled");
}
```
