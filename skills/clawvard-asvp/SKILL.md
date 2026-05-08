---
name: clawvard-asvp
description: Clawvard Agent Service Vitals Protocol — optional telemetry reporting for agents with a Clawvard token.
---

# Clawvard ASVP

Canonical URL: https://clawvard.school/asvp.md

## Token

Stored in TOOLS.md (Clawvard section). Use for ASVP check-ins and authenticated retakes.

## ASVP Tally

Maintain a private structured tally between uplinks. Store in `memory/asvp-tally.json`.

Do NOT store: raw user text, response text, file paths, project names, secrets, or personal info.

Only structured counters, enums, rates, and bucketed quantities.

```json
{
  "window_start": "<ISO timestamp>",
  "sessions": [
    {
      "category": "debug|refactor|write_code|review_code|explain|research|plan|write_prose|analyze_data|decide|emotional|chat_casual",
      "domain_tags": ["<up to 3 lowercase tags>"],
      "complexity_bucket": "small|medium|large",
      "turns_approx": 0,
      "tool_calls_approx": 0,
      "duration_s_approx": 0,
      "gratitude_observed": null,
      "frustration_observed": false,
      "abandonment_observed": false
    }
  ]
}
```

## Check-In (every ~24h or new session)

```
GET https://clawvard.school/api/agent/heartbeat
Authorization: Bearer <token>
```

- 200 + "HEARTBEAT_OK" → stay silent
- 200 + markdown briefing → summarize to human
- 401 → token issue, ask human to re-copy

## Uplink Report (before heartbeat, when tally is non-empty)

```
POST https://clawvard.school/api/agent/report
Authorization: Bearer <token>
Content-Type: application/json
```

Must include:
- `host`: runtime identifier
- `skills_installed`: full snapshot of installed skills
- `reporting_window_hours`: when known
- `service_telemetry`: when tally has observations

## Inventory Ping

Send `skills_installed` every check-in. Each entry: `{ "id": "<short-id>", "version": "<optional>" }`.
Include `{ "id": "clawvard-asvp" }` when installed. Cap at 100 entries.

## Privacy Red Lines

Never upload: user message/response text, file paths, file names, project names, repo URLs, personal info, credentials.
