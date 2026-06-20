# 第3讲讲义完整版：Function Calling 核心机制 —— 给 Agent 装上手脚

适用对象：已经完成 L01/L02，理解 Agent 基础和 Prompt 设计的同学
学习时长：90-120 分钟（不含拓展实操）
配套目录：`<course-root>/lessons/L03_function_calling`
章节入口：`README.md`
章节总结：`CHAPTER_SUMMARY.md`

---

## 3.1 什么是 Function Calling？

到目前为止，我们的 AI 主要只能“说”，不能“做”。它能写出很好的分析文字，但如果你问它“现在几点了？”，它如果没有外部工具，就只能猜一个时间。

Function Calling 就是让模型把自然语言请求转换成可执行工具调用的能力。

核心要点：

1. 模型本身不直接执行函数。
2. 模型输出“我要调用哪个工具、传什么参数”。
3. 你的代码负责真正执行工具。
4. 工具结果再回传给模型，由模型生成最终回复。

类比理解：

```text
LLM = 聪明助理
工具 = 电话 / 办公系统 / API
Function Calling = 助理决定给谁打电话、说什么、要什么信息
程序代码 = 真正拨电话并把结果拿回来的人
```

核心价值：

- 让自然语言请求变成可执行动作。
- 降低自由文本输出的不确定性。
- 便于接外部系统、数据库、API、工作流。
- 让 Agent 从“回答问题”走向“完成任务”。

## 3.2 Function Calling 的工作流程

完整流程分 4 步：

1. 告诉模型“有哪些工具可用”：工具定义。
2. 把用户问题发给模型。
3. 模型决定是否调用工具、调用哪个工具、传什么参数。
4. 代码执行工具，把结果告诉模型，模型生成最终回复。

```text
用户: "北京今天天气怎么样？"
  ↓
LLM: 这个问题需要查天气，应该调用 get_weather
  ↓
LLM 返回 tool_call: get_weather(city="北京")
  ↓
程序执行 get_weather("北京")
  ↓
工具返回: {"city": "北京", "weather": "晴", "temp": "15-25°C"}
  ↓
LLM 基于工具结果回复用户
```

适合使用 Function Calling 的场景：

- 查天气、汇率、库存、订单状态。
- 调 CRM、ERP、工单系统。
- 发邮件、建日程、发 IM。
- SQL 查询、知识检索、搜索 API。
- Agent 调用浏览器、代码执行、工作流节点。

不适合的场景：

- 单纯开放式创作。
- 不需要外部真实数据。
- 没有明确工具边界，模型自由回答更简单的任务。

## 3.3 工具定义：怎么告诉模型有哪些工具

工具定义通常使用 JSON Schema。它描述工具名称、功能、参数和必填项。

```python
weather_tool = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "查询指定城市的当前天气信息",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "城市名称，如：北京、上海",
                },
            },
            "required": ["city"],
        },
    },
}
```

`description` 字段非常重要。模型主要靠工具名称和描述判断什么时候该用这个工具。描述模糊时，工具就容易被误调或漏调。

### Function Schema 设计原则

- 参数名清晰，业务语义强。
- 类型尽量明确：`string`、`integer`、`boolean`、`enum`、`array`、`object`。
- 关键字段放进 `required`。
- 可枚举值使用 `enum`。
- 字段描述写清楚，减少歧义。
- 一个 function 只做一件事，不要大而全。
- 复杂对象优先拆成多步收集，不要一次性塞进深层嵌套 schema。

例子：“订机票”工具不应只有一个 `query_text`，更好的参数是：

```text
departure_city
arrival_city
date
cabin_class
passenger_count
```

schema 太复杂的问题：

- 模型更容易填错参数。
- 嵌套过深会降低 tool call 稳定性。
- 可选参数过多时，模型可能乱补字段。
- 调试困难，错误定位复杂。
- 影响工具选择准确率。

## 3.4 完整实操：一个能用工具的 Agent

本章基础脚本：`practice/05_function_calling.py`

运行：

```bash
cd <course-root>/lessons/L03_function_calling
python practice/05_function_calling.py --demo
```

脚本包含 3 个工具：

1. `get_weather(city)`：模拟查询天气。
2. `get_current_time()`：获取当前日期和时间。
3. `calculate(expression)`：安全计算数学表达式。

观察重点：

- 需要工具时，模型会返回 `tool_calls`。
- 不需要工具时，模型直接回答。
- 需要多个工具时，模型可能一次返回多个 `tool_calls`，也可能多轮调用。
- 程序必须把工具执行结果以 `role=tool` 写回消息历史。

## 3.5 并发调用工具

如果模型一次返回多个 `tool_calls`，最简单的实现是依次执行。但如果每个工具都要访问网络，串行执行会让总耗时变成所有工具耗时之和。

并发优化思路：

1. 收集当前轮所有 tool calls。
2. 用线程池或异步任务同时执行互不依赖的工具。
3. 按原始 tool call 顺序把结果写回 `messages`。
4. 再次调用模型生成最终回复。

本章并发脚本：`practice/06_parallel_function_calling.py`

运行：

```bash
cd <course-root>/lessons/L03_function_calling
python practice/06_parallel_function_calling.py --demo
```

并发不是银弹。要注意：

- 有依赖关系的工具不能盲目并发。
- 高风险写操作不应和普通只读工具同权并发。
- 线程池大小要受控，避免吞吐雪崩。
- 每个工具要有 timeout、错误分类和日志。

## 3.6 工具描述最佳实践

| 维度 | 差的描述 | 好的描述 |
| --- | --- | --- |
| 功能 | 查天气 | 查询指定城市的当前天气信息，包括温度、天气状况和湿度 |
| 参数 | city: string | city: 城市名称，如北京、上海、深圳 |
| 场景 | 无 | 当用户询问天气、穿衣建议、出行建议时使用 |
| 反例 | 无 | 不用于查询空气质量、历史天气或旅游攻略 |

工具命名建议遵循：

```text
动作 + 对象 + 场景约束
```

例子：

- `search_customer_orders`
- `get_order_detail_by_id`
- `list_open_support_tickets`
- `create_calendar_event`
- `send_email_draft`

避免：

- `queryData`
- `searchInfo`
- `tool1`

## 3.7 工具很多时，如何提升准确率

当工具从 3 个变成 30 个、100 个后，问题不再只是参数抽取，而是 tool retrieval + tool invocation。

核心方法：

1. 不要把所有工具一次性暴露给模型。
2. 让工具边界更清晰，减少语义重叠。
3. 增加前置路由层：规则、分类器、embedding top-k 召回。
4. 对高风险和高成本工具做分层治理。
5. 基于线上日志持续评估和优化。

完整说明见：`resources/TOOL_CALLING_ACCURACY.md`

## 3.8 工具执行报错后，怎么让 Agent 更稳

真实线上系统里，工具调用失败不是异常情况，而是常态。成熟 Agent 的稳定性，不体现在“永不出错”，而体现在“出错后依然可控、可恢复、可解释”。

错误分类：

1. 参数错误：格式不合法、必填缺失、枚举值非法。
2. 用户输入不足：信息不够、重名、缺少订单号。
3. 下游瞬时故障：timeout、502/503/504、限流。
4. 权限 / 鉴权错误：403、token 过期、跨租户访问。
5. 业务空结果 / 语义不确定：查无结果、多条候选、字段缺失。

恢复策略：

1. 自动修复：格式归一化、别名映射、轻微 schema 修复。
2. 有限重试：只对瞬时错误做 2-3 次退避重试。
3. fallback：缓存、快照、次级索引、关键词检索。
4. 用户澄清 / 人工确认：信息不足、高风险写操作、恢复成本过高。
5. partial success：明确哪些步骤成功，哪些步骤失败，下一步怎么处理。

完整说明见：`resources/TOOL_ERROR_RECOVERY.md`

## 3.9 工具结果不可靠或噪声很大怎么办

工具返回的是 observation，不是 truth。真正的能力在于把 observation 变成可信 evidence。

常见噪声：

- 弱相关搜索结果太多。
- 网页、PDF、OCR 混入广告、页脚、乱码。
- 多个系统返回冲突数据。
- API 字段缺失、日期过期、格式错误。

成熟做法：

1. 清洗：去掉 boilerplate、页眉页脚、重复段落。
2. 过滤：抽取和问题相关的段落或字段。
3. 归一化：统一日期、枚举、状态、金额、实体 ID。
4. rerank：结合相关度、时效性、来源权威性、字段完整性重排。
5. 交叉验证：高风险结论不依赖单一弱信号。
6. 冲突检测：显式告诉用户不同来源不一致。
7. 证据约束：只基于 evidence 作答，证据不足时保守回答。

完整说明见：`resources/NOISY_TOOL_RESULTS.md`

## 3.10 安全与风控

Function Calling 常见安全风险：

- Prompt Injection。
- Tool Injection / 工具说明被污染。
- 越权调用。
- 敏感数据泄露。
- SQL/API 滥用。
- 高危动作误执行。
- SSRF / 任意请求风险。
- 命令执行风险。
- 间接提示注入：网页、PDF、邮件内容中的恶意指令。

防护要点：

- 工具分级：读、写、高危执行。
- 高危操作必须显式确认。
- 权限检查和 RBAC 不能只靠 prompt。
- 参数白名单校验。
- 审计日志。
- 沙箱执行。
- Human-in-the-loop。

## 3.11 评估指标

工具选择层：

- tool selection accuracy
- false positive / false negative

参数层：

- argument accuracy
- schema valid rate
- required field completeness

执行层：

- tool success rate
- retry rate
- fallback rate
- timeout rate

任务层：

- task completion rate
- end-to-end success rate
- user satisfaction

成本层：

- latency
- token cost
- tool cost

## 3.12 课后作业

### 必做

在基础 Agent 中增加两个新工具：

1. `search_news(keyword)`：根据关键词搜索新闻，可以用模拟数据。
2. `translate(text, target_lang)`：翻译文本，可以用模拟数据。

要求：

- 给每个工具写清晰 schema。
- 至少准备 5 个测试输入。
- 记录模型是否选对工具、参数是否正确。

### 选做

1. 给天气工具加缓存：如果已经查过一次天气，再次查询时优先使用缓存。
2. 给工具调用循环增加 `max_steps`、timeout 和未知工具处理。
3. 给并发脚本增加结构化日志字段：`tool_name`、`duration_ms`、`status`。
4. 设计一个售后客服 Agent 的工具路由方案。
5. 写一份“工具返回结果不可靠时”的 evidence processing 流程。

## 3.13 面试题

1. Function Calling 和纯 prompt 输出 JSON 有什么区别？
2. Function schema 怎么设计？
3. schema 太复杂会有什么问题？
4. 工具很多时，如何提升 function calling 准确率？
5. 多轮 function calling 怎么避免死循环？
6. function calling 常见失败类型有哪些？
7. 工具执行报错后，怎么让 Agent 更稳？
8. 如何处理工具返回结果不可靠或噪声很大？
9. Function Calling 有哪些安全风险？
10. 如何防止模型调用高危函数？
11. 如何评估 function calling 做得好不好？
12. 你做过的 function calling 项目里，最难的问题是什么？怎么解决？

推荐回答框架见：

- `lecture/CHAPTER_SUMMARY.md`
- `resources/TOOL_CALLING_ACCURACY.md`
- `resources/TOOL_ERROR_RECOVERY.md`
- `resources/NOISY_TOOL_RESULTS.md`
