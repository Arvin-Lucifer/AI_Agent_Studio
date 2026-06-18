# L06 课后小测

## 简答题

1. LangChain 的五层架构分别是什么？
2. LCEL 中 `|` 的作用是什么？
3. `prompt | llm | StrOutputParser()` 的数据流是什么？
4. `RunnableParallel` 适合什么场景？
5. `RunnableBranch` 适合什么场景？
6. Pydantic Output Parser 相比 JSON Parser 有什么优势？
7. 自定义 Retriever 常见需求有哪些？
8. 为什么 `content[:100]` 不适合作为去重 key？
9. Callback 能监控哪些事件？
10. 生产级 Callback 还需要补哪些能力？

## 参考答案要点

1. 基础层、模型层、能力层、编排层、应用层。
2. 把 Runnable 组件按输入输出连接成链。
3. 输入 dict -> Prompt 生成 messages -> LLM 生成 AIMessage -> Parser 提取结果。
4. 多个独立子任务同时执行，例如中英文摘要、多个分析维度。
5. 根据输入条件选择不同链路，例如短问题直接答、长问题分步骤答。
6. 类型校验、字段说明、范围约束、下游可直接拿对象。
7. 混合检索、权限过滤、元数据过滤、多知识源、去重、rerank。
8. 前缀相同可能误删，前缀不同可能漏删，且没有归一化。
9. Chain、LLM、Tool、Retriever 的开始/结束/错误/耗时/token。
10. run_id 隔离、日志持久化、成本统计、告警、脱敏、可视化 trace。
