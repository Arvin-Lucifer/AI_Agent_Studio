#!/usr/bin/env python3
"""L10 Step 34: discover SKILL.md files and show progressive metadata.

这个脚本对应讲义 3.1：SKILL.md 是 Skill 的声明式入口。
它只做发现和解析，不执行任何业务动作，目的是让学生先看清：

- Skill 的元信息层：name / description / trigger / tags。
- Skill 的指令层：Markdown 里的使用说明和执行步骤。
- 为什么启动时只加载元信息，触发后才加载完整 instructions。

Usage:
    python practice/34_skill_loader.py
"""

from __future__ import annotations

from skill_common import SkillLoader


def main() -> None:
    loader = SkillLoader()
    skills = loader.discover_skills()

    print("=== DISCOVERED SKILLS ===")
    for skill in skills:
        print(f"- {skill.name} v{skill.version}")
        print(f"  tags: {', '.join(skill.tags) if skill.tags else '无'}")
        print(f"  trigger: {skill.trigger or '未声明'}")
        print(f"  description: {skill.description.splitlines()[0] if skill.description else ''}")
        print(f"  instructions_chars: {len(skill.instructions)}")

    print("\n=== PROGRESSIVE DISCLOSURE DEMO ===")
    weather = loader.load_skill("weather-query")
    print("启动时预加载：")
    print(f"- name: {weather.name}")
    print(f"- description: {weather.description.splitlines()[0]}")
    print("触发后再加载：")
    print(weather.instructions.splitlines()[0])


if __name__ == "__main__":
    main()
