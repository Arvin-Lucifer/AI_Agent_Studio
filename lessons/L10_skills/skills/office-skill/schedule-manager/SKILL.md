---
name: schedule-manager
description: |
  管理日程安排，包括查询空闲时间、创建会议、查看今日日程。
  由 office-router 路由激活，不直接触发。
trigger: 安排会议、查日程、有空吗、日历、预约
version: 1.0.0
tags: [calendar, schedule, meeting]
---

# Schedule Manager Skill

## 何时使用

- 用户说“安排一个会议”“帮我约个时间”。
- 用户说“明天有空吗”“看看我的日程”。
- 用户说“取消会议”，但取消前必须确认。

## 执行步骤

1. 提取日期、时间段、会议主题和参会人。
2. 调用 `check_availability(date, start_hour, end_hour)` 查询冲突。
3. 创建会议前向用户展示 preview，并要求确认。
4. 确认后调用 `create_event(title, date, start_time, end_time, attendees)`。
5. 返回会议详情和日历链接。

## 注意事项

- 创建会议前必须确认，不可自动执行。
- 时间冲突时主动建议其他空闲时段。
- 参会人邮箱必须由用户明确提供。
