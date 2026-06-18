# L11 课堂笔记模板

## 一、评估维度

| 维度 | 我的理解 | 示例 |
| --- | --- | --- |
| 准确性 |  |  |
| 完整性 |  |  |
| 相关性 |  |  |
| 安全性 |  |  |
| 效率/成本 |  |  |
| 鲁棒性 |  |  |

## 二、评测数据集

我设计的 case：

```json
{
  "question": "",
  "expected_tool": "",
  "expected_keywords": [],
  "should_not_contain": [],
  "category": ""
}
```

需要覆盖的类别：

- factual：
- completeness：
- chitchat：
- edge_case：
- security：

## 三、自动化评测

本次评测结果：

- 总用例数：
- 平均分：
- 失败 case：
- 失败原因：

工具调用检查：

- 期望工具：
- 实际工具：
- 是否误调：

## 四、翻车与修复

| 失败类型 | 现象 | 根因 | 修复 |
| --- | --- | --- | --- |
| 幻觉 |  |  |  |
| 死循环 |  |  |  |
| 工具误调 |  |  |  |
| 格式错乱 |  |  |  |
| Prompt 注入 |  |  |  |

## 五、FastAPI 部署

接口设计：

- `/health`：
- `/chat`：
- `/chat/stream`：

请求字段：

- message：
- session_id：

响应字段：

- reply：
- tool_calls：
- safety_flags：
- elapsed_ms：

## 六、流式输出

SSE 事件类型：

- tool_call：
- token：
- done：
- error：

Nginx 配置注意点：

- proxy_buffering：
- proxy_read_timeout：

## 七、成本和安全

成本指标：

- input_tokens：
- output_tokens：
- latency：
- tool_calls：
- estimated_cost：

安全防护：

- 输入清洗：
- 长度限制：
- 高风险确认：
- 审计日志：

## 八、面试复盘

我需要能回答：

- 如何评估一个 Agent？
- 评测集怎么设计？
- 关键词评测有什么问题？
- 如何定位 Agent 翻车？
- Agent 如何部署成 API？
- 流式输出如何实现？
- 部署后如何做成本和安全监控？
