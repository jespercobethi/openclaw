# Working Buffer (Danger Zone Log)

**Status:** STANDBY
**Started:** 2026-04-13
**Context Threshold:** 60%

---

## 使用说明

当 context 使用率超过 60% 时：
1. 将 Status 改为 ACTIVE
2. 清空旧日志，开始新鲜
3. 此后的每条消息都要记录在这里

## 格式

```markdown
## [timestamp] Human
[他们的消息]

## [timestamp] Agent (summary)
[1-2句话总结你的回复 + 关键细节]
```

---

## 日志

<!-- 在此开始记录 -->
