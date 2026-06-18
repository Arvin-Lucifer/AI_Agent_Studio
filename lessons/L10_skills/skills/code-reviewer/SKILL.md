---
name: code-reviewer
description: |
  审查代码变更，检测 Bug、安全漏洞、性能问题和风格问题。
  触发条件：用户提供代码片段、PR 链接，或要求审查代码。
  不触发：纯闲聊、非代码相关请求、没有具体代码的概念问答。
trigger: 用户提供代码片段、PR 链接，或要求 review、审查、检查代码
version: 1.0.0
tags: [code-quality, security, review]
---

# Code Reviewer Skill

## 何时使用

- 用户提交代码片段并请求审查。
- 用户分享 GitHub PR 链接。
- 用户提到 review、审查、检查代码、Code Review。

## 何时不使用

- 用户只是问编程概念。
- 用户没有提供具体代码。
- 用户只要求解释某个 API，而不是审查实现。

## 执行步骤

### Step 1: 代码分类

判断代码语言、代码类型和可能影响范围。

### Step 2: 多维度检查

| 维度 | 严重级别 | 检查内容 |
| --- | --- | --- |
| 安全 | critical | SQL 注入、XSS、硬编码密钥、路径遍历 |
| 正确性 | critical/high | 逻辑错误、空指针、类型错误 |
| 性能 | warning | N+1 查询、内存泄漏、不必要循环 |
| 风格 | suggestion | 命名、注释、重复代码 |

### Step 3: 输出格式

按 `severity/category/location/description/fix/confidence` 结构化输出。

## 注意事项

- 安全问题一律标记为 critical。
- 不确定的问题标注置信度。
- 必须给出可操作的修复建议。
