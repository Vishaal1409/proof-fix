# API Contract (Backend <-> Frontend)

Base URL (local): `http://localhost:8000`

Streaming choice: **Server-Sent Events (SSE)**. It is one-way (server to browser), simpler than WebSocket, and enough for a live timeline. The browser uses `EventSource`.

## Endpoints

### `GET /health`
Returns `{"status": "ok"}`.

### `POST /runs`
Starts a new agent run.

Request:
```json
{
  "issue_text": "calculate_average crashes when the list is empty",
  "repo_url": "https://github.com/user/repo",
  "language": "python",
  "max_attempts": 3
}
```
Response (`201`):
```json
{
  "run_id": "run_8f3a2c",
  "status": "queued"
}
```

### `GET /runs/{run_id}`
Returns the current state and, when finished, the result.

Response:
```json
{
  "run_id": "run_8f3a2c",
  "status": "running",
  "current_step": "verify",
  "attempt": 2,
  "max_attempts": 3,
  "created_at": "2026-10-07T10:15:00Z",
  "result": null
}
```

When `status` is `completed` or `failed`, `result` is filled:
```json
{
  "fixed": true,
  "attempts_used": 2,
  "repro_test": "def test_empty_list(): ...",
  "patch_diff": "--- a/stats.py\n+++ b/stats.py\n...",
  "test_results": {
    "repro_before_fix": { "passed": false, "summary": "1 failed" },
    "repro_after_fix":  { "passed": true,  "summary": "1 passed" },
    "full_suite_after_fix": { "passed": true, "summary": "12 passed" }
  },
  "review": { "verdict": "approve", "notes": "Handles empty input, no side effects found." },
  "explanation": "The function divided by len(items) without checking for an empty list...",
  "pr_url": null
}
```

`status` values: `queued`, `running`, `completed`, `failed`.

### `GET /runs/{run_id}/events` (SSE)
Streams step events as they happen. Each message is one JSON event (format below). The stream closes after the final event.

Frontend example:
```js
const es = new EventSource(`${API}/runs/${runId}/events`);
es.onmessage = (e) => {
  const event = JSON.parse(e.data);
  // update the timeline with event
};
es.onerror = () => es.close();
```

## Event format

```json
{
  "run_id": "run_8f3a2c",
  "seq": 7,
  "step": "verify",
  "status": "failed",
  "attempt": 1,
  "message": "Full test suite: 2 tests failed",
  "data": {},
  "timestamp": "2026-10-07T10:16:42Z"
}
```

| Field | Meaning |
|---|---|
| `run_id` | Which run this event belongs to |
| `seq` | Increasing number, so the UI can order events and ignore duplicates |
| `step` | `understand`, `reproduce`, `fix`, `verify`, `retry`, `review`, `deliver` |
| `status` | `pending`, `running`, `done`, `failed` |
| `attempt` | Which attempt (1, 2, 3...). Steps before the first fix use 0 or 1 |
| `message` | Short human-readable text shown in the timeline |
| `data` | Optional extras: `diff`, `test_output`, `files`, `model`. Can be `{}` |
| `timestamp` | UTC ISO-8601 time |

### Example event sequence (one retry)

```
understand  running   "Reading repository"
understand  done      "Likely cause: stats.py, calculate_average"
reproduce   running   "Writing reproduction test"
reproduce   done      "Test fails as expected"
fix         running   "Generating patch (attempt 1)"
fix         done      "Patch applied"
verify      running   "Running tests"
verify      failed    "2 existing tests broke"
retry       running   "Analyzing failure, new approach"
fix         running   "Generating patch (attempt 2)"
fix         done      "Patch applied"
verify      done      "All tests pass"
review      done      "Verdict: approve"
deliver     done      "Result ready"
```

The UI maps each event to the timeline: show the latest status per `step`, and show the `message` and attempt number. Failed attempts stay visible. They are part of the story in the demo.

## Error responses

```json
{ "error": "run_not_found", "message": "No run with that id" }
```

| Code | When |
|---|---|
| 400 | Missing or invalid input |
| 404 | Unknown `run_id` |
| 500 | Unexpected server error |

## Notes for each teammate

- **Arun (frontend):** build against this contract using mock events first, then switch to the real endpoint.
- **Shruthika (sandbox):** your function returns the structure in `architecture.md` section 5. The backend turns its output into events and `test_results`.
- **Vishaal (backend):** every step transition emits one event. Keep `message` short.

If anything here needs to change, update this file and tell the group.
