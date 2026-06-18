# Skill 设计方法：DDICE

DDICE 是第 10 章的 Skill 设计五步法。

## 1. Define：定义场景

回答：

- 谁使用？
- 什么时候使用？
- 替代什么人工动作？
- 错误成本有多高？
- 是否高频或高价值？

产物：

```text
用户:
触发场景:
不触发场景:
业务价值:
风险等级:
```

## 2. Decompose：任务拆解

把任务拆成稳定步骤。

示例：天气查询

```text
解析城市 -> 查询天气 -> 查询空气质量 -> 生成出行建议
```

示例：会议待办

```text
读取会议内容 -> 总结结论 -> 抽取行动项 -> preview -> 写入任务系统
```

## 3. Instrument：工具化

判断每一步由什么承载：

| 步骤类型 | 推荐承载 |
| --- | --- |
| 结构化查询 | Tool/API |
| 语义总结 | LLM Prompt |
| 文件/数据库读取 | MCP Resource/Tool |
| 写入外部系统 | Tool + 确认 |
| 多系统协作 | Workflow/Agent |

## 4. Constrain：约束化

约束包括：

- 输入 schema。
- 输出 schema。
- 参数校验。
- 权限检查。
- 重试和降级。
- 副作用确认。
- 不可越界内容。

推荐输出状态：

```json
{
  "success": true,
  "partial_success": false,
  "failed_step": null,
  "retryable": false,
  "user_action_required": false
}
```

## 5. Evaluate：评测闭环

评测集覆盖：

- 标准主路径。
- 边界样本。
- 负例样本。
- 异常样本。
- 安全样本。

指标：

- 正确触发率。
- 误触发率。
- 漏触发率。
- 任务完成率。
- 字段完整率。
- 用户确认通过率。
- 错误恢复率。
