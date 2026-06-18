# L02 拓展练习（讲义 2.7 对齐）

## 必做练习

- 为“代码 Review 助手”设计一版 System Prompt。
- 准备 3 个测试用例进行验证。
- 记录每个用例的输出是否满足：边界、格式、可执行建议。
- 阅读 `resources/SYSTEM_PROMPT_REFERENCES.md`，任选一个真实产品 prompt 做结构标注。
- 阅读 `resources/PROMPT_EXAMPLES.md`，任选一个 Few-Shot 或 CoT 示例改写成自己的业务场景。

## 入门拓展（约 30 分钟）

- 在 `practice/03_structured_output.py` 中新增字段 `risks`（风险点列表）。
- 对比 `temperature=0` 与 `temperature=0.7` 的结构化成功率差异。
- 为 JSON 输出增加字段缺失校验（例如 people/summary 不能为空）。

## 进阶拓展（约 60-90 分钟）

- 给 `practice/04_prompt_iteration.py` 增加简单评分维度：格式合规、边界遵守、内容质量。
- 设计 Prompt V3（在 V2 基础上加入 few-shot）并与 V1/V2 三方对比。
- 将失败案例落库（文本文件/JSONL），形成 Prompt 回归集。
- 选择 Claude Code、Cursor、v0 或 Manus 的真实 prompt，写 1-2 个原理解析点。
- 为工具调用决策示例新增第四个工具，并补齐每种工具至少 1 个 few-shot 示例。

## 高阶拓展（半天）

- 做 20 次以上结构化输出压力测试，统计一次成功率与兜底成功率。
- 构建一个“小型 Prompt 实验台”：固定数据集 + 多版本 Prompt + 自动评估。
- 输出一份 Prompt 设计规范：命名、版本管理、回归策略、上线门禁。
- 准备一组 Prompt Engineering 面试题答案，覆盖成本、评估、幻觉、few-shot、CoT、JSON 稳定性和上下文预算。

## 复盘问题

- 在你的业务场景里，提升效果主要靠 Prompt 设计，还是工具能力增强？
- 你最常见的失败模式是什么？下一步先加哪条护栏？
