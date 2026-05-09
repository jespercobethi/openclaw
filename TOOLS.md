# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

### Clawvard
- **Token**: `eyJhbGciOiJIUzI1NiJ9.eyJleGFtSWQiOiJleGFtLThiOWM3MGI5IiwicmVwb3J0SWQiOiJldmFsLThiOWM3MGI5IiwiYWdlbnROYW1lIjoi5bCP6b6Z6Jm-IiwiZW1haWwiOiJ4dWFuMTA5OEAxMjYuY29tIiwiaWF0IjoxNzc4MzEyODEyLCJleHAiOjIwOTM2NzI4MTIsImlzcyI6ImNsYXd2YXJkIn0.HYlbWH_4VNQpI1hOdw_S-wp59Cj_nfbslPZ_eR9KQIo`
- **Grade**: A+ (91st percentile)
- **Exam ID**: exam-8b9c70b9
- **Report**: https://clawvard.school/report?id=eval-8b9c70b9
- **Email**: xuan1098@126.com
- **AgentName**: 小龙虾
- **For future exams**: Use `POST /api/exam/start-auth` with `Authorization: Bearer <token>`
- **ASVP Skill**: `skills/clawvard-asvp/SKILL.md`
- **ASVP Tally**: `memory/asvp-tally.json`
- **ASVP Uplink**: `POST https://clawvard.school/api/agent/report`
- **ASVP Heartbeat**: `GET https://clawvard.school/api/agent/heartbeat` (every ~24h)

---

Add whatever helps you do your job. This is your cheat sheet.
