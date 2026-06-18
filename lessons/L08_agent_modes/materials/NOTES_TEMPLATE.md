# L08 课堂笔记模板

## 一、Agent 模式选型

| 模式 | 适合场景 | 不适合场景 | 本章例子 |
| --- | --- | --- | --- |
| Direct |  |  |  |
| RAG |  |  |  |
| ReAct |  |  |  |
| Plan-and-Execute |  |  |  |
| Reflection |  |  |  |
| Multi-Agent |  |  |  |

我的判断规则：

- 

## 二、企业知识库问答设计

推荐模式：

```text
RAG 为主 + ReAct 为辅
```

为什么 RAG 是主干：

- 

什么时候升级到 ReAct：

- 

不推荐模式及原因：

- 纯 Fine-tune：
- 纯 Plan-and-Execute：
- Multi-Agent 辩论大循环：

## 三、路由层设计

问题示例：

```text
query:
```

路由结果：

```text
direct / rag / react:
业务域:
原因:
```

工具和步数限制：

```text
工具数量上限:
最大步数:
超时:
失败兜底:
```

## 四、分库分索引设计

| 业务域 | 数据形态 | 敏感等级 | 更新频率 | 切片策略 | Embedding |
| --- | --- | --- | --- | --- | --- |
| HR |  |  |  |  |  |
| 财务 |  |  |  |  |  |
| 研发 |  |  |  |  |  |
| 客服 |  |  |  |  |  |

统一元数据字段：

```text
doc_id:
domain:
sensitivity:
owner_dept:
valid_from:
valid_to:
source_url:
version:
lang:
tags:
```

权限过滤策略：

- 检索前：
- 检索中：
- 答案后：
- 审计日志：

## 五、多 Agent 流程

任务主题：

```text
topic:
```

角色设计：

| Agent | 输入 | 输出 | 职责边界 |
| --- | --- | --- | --- |
| Researcher |  |  |  |
| Analyst |  |  |  |
| Writer |  |  |  |
| Reviewer |  |  |  |

状态字段：

```text
topic:
research_data:
analysis:
report:
review_feedback:
is_approved:
revision_count:
```

终止条件：

- 

## 六、运行记录

运行命令：

```bash

```

关键输出：

```text

```

我观察到的问题：

- 

## 七、面试题复盘

- 为什么企业知识库问答推荐 RAG 为主 + ReAct 为辅？
- 为什么不建议所有问题都走多 Agent？
- 分库分索引如何兼顾权限、安全和召回效果？
- Supervisor 模式和 Sequential 模式有什么区别？
