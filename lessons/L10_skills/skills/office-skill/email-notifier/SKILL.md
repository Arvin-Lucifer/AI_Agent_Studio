---
name: email-notifier
description: |
  发送邮件通知，支持发送会议邀请、日程提醒等邮件。
  由 office-router 路由激活，不直接触发。
trigger: 发邮件、通知、发送提醒、邮件告知
version: 1.0.0
tags: [email, notification, communication]
---

# Email Notifier Skill

## 何时使用

- 用户说“发邮件通知某人”。
- 用户说“提醒一下参会人”。
- 安排完会议后，需要发送邀请邮件。

## 执行步骤

1. 提取收件人邮箱。
2. 根据上下文生成邮件主题和正文。
3. 展示邮件 preview，请用户确认。
4. 确认后调用 `send_email(to, subject, body)`。
5. 返回发送状态。

## 注意事项

- 发送前必须预览确认。
- 邮件内容需专业正式。
- 当前版本不支持附件。
