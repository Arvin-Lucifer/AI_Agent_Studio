# AI Native 的工作方式

这份教辅资料总结一线 AI-native 团队的组织实践。它关注的不是“员工会不会用 AI 工具”，而是组织是否围绕 **agent、context、loop** 重新设计工作方式。

一句话：

> AI-native 不是把 AI 加进旧流程，而是围绕 agent、context 和 loop 重构组织执行系统。

## 一、结论先看

1. Agent 已从“个人助手”演化为“组织执行单元”。很多团队不再是员工各自用 AI，而是由公司统一建设、维护和治理核心 agent。
2. Human in the loop 正在被压缩为 Human at the beginning and the end。人负责设定方向、验收结果，执行中的拆解、研究、实现、联动逐步交给 AI 闭环完成。
3. Context 管理正在替代传统知识管理。文档、聊天、会议记录、代码库、ticket、历史决策被视为同一个上下文系统。
4. 组织形态开始从“按职能分工”转向“按 loop 分工”。每个人和每个 agent 尽量完成更完整的闭环，减少跨人协调成本。
5. AI-native 组织的管理重点，从“给工具”变成“做系统”：统一 skill、统一工作流、统一任务入口、统一上下文和统一验收机制。

## 二、八个重要观察

### 1. Coding Agent 正在成为基础设施

硅谷 AI-native 团队中，Claude Code 等 coding agent 几乎成为基础设施。

趋势不只是“人使用 coding agent”，而是：

```text
人表达意图
  -> 总控 agent 整理任务
  -> worker agent 调用 coding agent
  -> 自动实现、测试、提交 PR
```

这意味着 AI 工具竞争点正在从“单次对话体验”，转向“能否嵌入组织流程”。

### 2. 真正的放大器不是更多 agent，而是让 AI 管 AI

Clockless AI 的实践很有代表性：创始人不再自己管理多个 agent，而是把“管理 agent 的工作”交给总控 agent。

典型流程：

```text
人用语音表达意图
  -> 总控 agent 提取目标、约束、验收标准和背景
  -> 分发给 worker agent
  -> worker agent 通过文件系统传递 intent 和 task
  -> 人通过 dashboard 观察进展
```

关键判断：

> 只要人还在执行 loop 里，AI 越强，人越累。

原因是 token 吞吐远超人脑处理能力，人很难稳定跟踪多个 agent 的上下文、状态和任务依赖。

### 3. 公司级 agent 正在替代“每人一个 agent”

一些团队不再让每个员工各自训练一套 agent，而是全公司共用一个核心 agent，由 CTO 或核心技术负责人集中运营。

背后的思路：

```text
与其让所有员工学习 prompt、skill 和 agent 使用技巧，
不如直接把高质量能力封装好，喂到每个人手边。
```

典型案例：公司级 coding agent 从 Linear 拉任务，自动研究问题、产出技术方案、实现代码、生成 PR，再让工程师 review。

流程变化：

```text
Before:
Leader -> Engineer -> Claude Code -> Engineer 验收

After:
CEO/Leader -> 公司级 Agent -> PR -> Engineer Review
```

本质变化：

> Agent 不再只是工程师的工具，而是公司自己在迭代的内部产品。

### 4. PRD 没死，但规格说明正在向任务系统集中

AI-native 团队仍然需要 PRD 和 specs，只是它们不一定放在 Notion，而是进入 Linear、Issue、Ticket 等任务系统。

原因：

- 文档不只是给人看，也要给 agent 执行。
- 任务系统逐渐变成规格说明、执行入口、协作界面的统一载体。
- 一个结构化 ticket 可以直接触发 agent 执行、测试和提交 PR。

好的 ticket 需要包含：

- 目标。
- 背景。
- 约束。
- 验收标准。
- 相关上下文。
- 不做什么。

### 5. 知识管理正在升级成 Context 管理

传统知识管理强调“把知识存起来”。AI-native 的 context 管理强调“让 agent 能调用、推理、执行”。

Context 包括：

- 聊天记录。
- 文档。
- 会议逐字稿。
- 代码库。
- Ticket。
- 历史决策。
- 口头讨论。

典型方法：

1. 人先给出知识库结构。
2. Agent 去爬 Notion、Slack、Linear、GitHub 等系统。
3. Agent 反问“还缺什么？”。
4. Agent 为相关人员生成 question list。
5. 相关人员和 Agent 开会，补充缺失信息。

这不是传统人工整理知识库，而是让 agent 主动发现上下文缺口并发起补全流程。

### 6. 上下文不是越多越好，隔离同样重要

高水平 AI-native 团队不只做 context 汇总，也做 context boundary design。

需要回答：

- 哪些信息应该共享？
- 哪些信息应该延迟暴露？
- 哪些角色只看问题，不看答案？
- 哪些 agent 不能访问敏感上下文？

例子：

Research Agent 不一定应该过早看到 PM 已经写好的 solution。否则它可能被既有答案污染，失去独立发现能力。

这和课程里的权限过滤、RAG Prompt Injection 防御、Memory 隔离和 Skill 授权边界是同一个工程问题。

### 7. 极致 Context 捕获：持续记录组织记忆

有些团队走向另一端：尽量捕获所有上下文，例如办公室持续录音、会议自动总结、讨论自动转任务。

价值：

- 临时想法不会丢失。
- 高优需求能进入任务系统。
- 零散讨论能转化为可检索组织记忆。
- Agent 可以基于更完整的历史上下文行动。

风险：

- 隐私和合规。
- 上下文噪声。
- 权限边界。
- 过度记录造成心理压力。

所以“极致捕获”必须配合权限、脱敏、保留周期和访问审计。

### 8. 人与人的协作价值正在变化

AI 降低了执行成本，但组织摩擦不会自动消失。

如果只是给每个人配 AI，让每个人成为“超级个体”，组织流程却不变，整体效率未必提升。

人的协作价值会更多转向：

- 建立信任。
- 激发创意。
- 做价值判断。
- 提供情绪支持。
- 解决模糊冲突。
- 定义方向和验收标准。

一句话：

> 协作不等于协调。AI-native 组织要减少低价值协调，把人的沟通还给信任、创意和判断。

## 三、组织设计启发

### 1. 从按职能分工到按 loop 分工

传统组织按职能拆分：

```text
PM -> Design -> Engineering -> QA -> Ops
```

AI-native 组织更强调按 loop 组织：

```text
目标 -> 上下文 -> 执行 -> 验收 -> 反馈 -> 迭代
```

含义：

- 不是让每个职能只完成一小段。
- 而是尽量围绕一个完整问题闭环组织人和 agent。
- 每个角色或 agent 完成更完整的输入、执行、反馈链路。

直接收益是减少协同成本。

### 2. 每个人都要像做产品一样迭代自己的工作方式

AI-native 团队会把工作方式本身当作可设计对象。

例如 marketing manager 可以把营销工作拆成：

- 选题 research skill。
- 用户访谈 summary skill。
- 竞品分析 skill。
- 投放复盘 skill。
- 内容改写 skill。

然后像迭代产品一样持续优化这些 skills。

这意味着：

- 个人 workflow 需要产品化。
- 组织要沉淀可复用 skills。
- 好的工作方法不只靠口口相传，而要系统化下发。

### 3. 管理者更像系统设计者

未来优秀管理者的关键能力，可能不再是频繁分派任务和做过程追踪，而是：

- 设计任务结构。
- 设计验收标准。
- 设计 context 边界。
- 设计人机分工。
- 设计组织里的闭环。
- 设计 agent 与人的协作协议。

管理者不只是“盯执行”，而是“设计系统让执行发生”。

## 四、具体做法清单

### Agent 架构与任务执行

- 建立总控 agent，负责理解意图、拆解目标、调度 worker agent。
- worker agent 之间尽量通过结构化文件或状态传递，不靠散乱聊天。
- 人只在开始定义目标，在结束验收结果。
- 公司级 coding agent 从 Linear/Jira/GitHub Issue 拉任务，自动产出 PR。
- 每个 ticket 独立容器运行，支持高并发和休眠唤醒。

### Context 管理

- 人先设计知识结构，再让 agent 去多源系统补上下文。
- 让 agent 主动发现上下文缺口，并生成访谈问题。
- 对关键会议、讨论和决策做自动摘要和可检索沉淀。
- 对不同 agent 设置 context 边界，避免污染和越权。
- 为组织记忆设置权限、保留周期、审计和删除机制。

### 管理与组织演化

- 统一下发公共 skill，而不是指望员工各自摸索。
- 鼓励一线团队围绕 pain point 快速造小工具。
- 把重复性工作封装成 skills。
- 用 dashboard 观察 agent 执行状态，而不是人工实时盯每一步。
- 把人的沟通更多用于信任、创意、冲突解决和方向判断。

## 五、案例速览

| 案例 | 核心做法 | 代表意义 |
| --- | --- | --- |
| Clockless AI | 总控 agent 管理 worker agent，人退出执行回路 | AI 管 AI，而不是人盯 AI |
| BeSimple | 全公司共用 coding agent，ticket 直达 PR | 公司级 agent 产品化 |
| Mission AI | 管理层统一准备公共 skill | 降低组织 adoption 成本 |
| Ditto | Claude 主动补齐知识库缺口 | Context 自增长 |
| Perfectly | 办公室持续录音，沉淀组织记忆 | 极致 context 捕获 |
| Intuit | 为不同 agent 做 context 隔离 | 避免上下文污染 |
| Meta | 鼓励小团队自行造工具 | Bottom-up 创新更快 |
| Flyhomes | 把 marketing 工作做成 skills | 非技术岗位 workflow 产品化 |

## 六、对国内团队的参考价值

### 1. 不要只采购工具，要建设组织级使用方式

单独给员工配 AI，常常只能提升个体效率。真正的组织增益来自：

- 是否有统一 agent。
- 是否有统一任务入口。
- 是否有统一上下文系统。
- 是否有统一 skill。
- 是否有统一验收方式。

### 2. 先改最短路径，不要一开始就做大一统平台

很多优秀实践不是中央规划出来的，而是从一线痛点出发：

```text
先做一个能闭环的小系统
  -> 跑通一个团队
  -> 抽象成公共 skill
  -> 扩展到更多场景
```

### 3. 先做闭环，再做平台

不要一开始就建设“AI 中台”。更实际的路径是：

1. 找一个高频痛点。
2. 定义输入和验收标准。
3. 接入必要上下文。
4. 让 agent 完成执行闭环。
5. 把成功经验沉淀为 skill 或 workflow。

## 七、和本课程的关系

这份资料可以帮助学生理解为什么课程不是孤立讲 Prompt、RAG、Memory、MCP、Skill、Eval、Deploy，而是在拼一个组织级 AI-native 工作系统。

对应关系：

| AI-native 概念 | 课程章节 |
| --- | --- |
| Agent 作为组织执行单元 | L01、L08、L10 |
| Context 管理 | L05 RAG、L07 Memory |
| 统一 Skill | L10 Skill |
| 统一任务入口和执行闭环 | L08 Agent 模式、L11 部署 |
| 验收标准和回归评测 | L11 评测 |
| 毕业项目端到端闭环 | L12 |

## 八、课堂讨论问题

1. 如果公司只给每个人配一个 AI 工具，但流程不变，会发生什么？
2. 哪些工作适合做成公司级 agent，而不是个人 prompt？
3. Context 越多越好吗？什么时候应该隔离上下文？
4. Human in the loop 和 Human at the beginning and the end 的差别是什么？
5. 你的团队里哪个最短 loop 最适合先做 AI-native 改造？

## 九、总结

AI-native 的核心不是“用 AI 提效”，而是组织执行系统的重构：

```text
Agent -> 执行单元
Context -> 组织记忆和行动依据
Loop -> 工作闭环和验收机制
Skill -> 可复用能力
Dashboard -> 人类观察和治理入口
```

如果沿用旧组织形态，只让个体变强，最后可能得到的是“很多超级个体 + 依旧低效的组织”。

真正的机会，是让组织本身也变成 AI-native。
