---
name: doc-generator
description: |
  生成办公文档，包括会议纪要模板、周报、项目总结等。
  由 office-router 路由激活，不直接触发。
trigger: 生成文档、会议纪要、写周报、创建模板
version: 1.0.0
tags: [document, writing, template]
---

# Doc Generator Skill

## 何时使用

- 用户说“帮我写会议纪要”。
- 用户说“生成一个周报模板”。
- 用户说“创建项目总结文档”。

## 执行步骤

1. 识别文档类型：会议纪要、周报、项目总结或其它。
2. 从对话上下文中提取会议主题、参会人、讨论内容等信息。
3. 生成结构化文档内容。
4. 调用 `create_doc(title, content, folder_id)`。
5. 返回文档标题和访问链接。

## 注意事项

- 文档内容需结构化，使用标题和列表。
- 上下文不足时主动追问。
- 默认保存到用户文档根目录。
