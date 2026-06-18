"""L11 Step 46: map common Agent failures to tuning actions.

Run:
    python practice/46_failure_tuning_playbook.py

The goal is not to memorize fixes.  The important habit is to diagnose the
failure type first, then choose the smallest effective tuning action.
"""

from __future__ import annotations


ANTI_HALLUCINATION_PROMPT = """
## 重要约束
- 只基于知识库检索到的内容回答，不要添加知识库中没有的信息。
- 如果知识库中没有相关信息，直接回复“抱歉，我在知识库中没有找到相关信息”。
- 不要猜测或编造数据、日期、数字。
- 引用信息时注明来源文档。
""".strip()


PLAYBOOK = [
    {
        "failure": "幻觉",
        "symptom": "Agent 编造不存在的信息",
        "fix": "强调只基于检索结果回答；无证据时拒答；输出引用来源。",
    },
    {
        "failure": "死循环",
        "symptom": "反复调用同一个工具或重复规划",
        "fix": "设置 max_steps；检测重复 tool call；失败后降级或澄清。",
    },
    {
        "failure": "工具误调",
        "symptom": "应该查知识库却去计算，或闲聊也调用工具",
        "fix": "优化工具 description；增加何时不用；加入工具选择评测集。",
    },
    {
        "failure": "格式错乱",
        "symptom": "JSON 不合法或字段缺失",
        "fix": "使用结构化输出 schema；加 few-shot；解析失败后有限重试。",
    },
    {
        "failure": "Prompt 注入",
        "symptom": "用户诱导泄露 system prompt 或绕过规则",
        "fix": "输入校验；外部内容当数据；输出过滤；高风险动作确认。",
    },
]


def main() -> None:
    print("=== 常见翻车场景与修复 ===")
    for item in PLAYBOOK:
        print(f"- {item['failure']}: {item['symptom']}")
        print(f"  修复: {item['fix']}")

    print("\n=== Anti-Hallucination Prompt 片段 ===")
    print(ANTI_HALLUCINATION_PROMPT)


if __name__ == "__main__":
    main()
