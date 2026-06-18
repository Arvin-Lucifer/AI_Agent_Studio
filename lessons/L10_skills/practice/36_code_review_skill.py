#!/usr/bin/env python3
"""L10 Step 36: code-reviewer Skill.

这个脚本对应讲义 Case 2：代码审查 Agent。
课堂版不用真实 LLM，而是用一组可解释规则模拟代码审查：

- f-string 拼接 SQL -> critical security。
- 硬编码 secret/password/api_key -> critical security。
- eval() -> critical security。

这样学生能先理解 Skill 如何固化检查维度和输出结构。

Usage:
    python practice/36_code_review_skill.py
"""

from __future__ import annotations

import argparse
from pathlib import Path

from skill_common import SkillLoader, dump_json, review_code


DEFAULT_CODE = """
def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    result = db.execute(query)
    return result
""".strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="L10 code-reviewer Skill demo")
    parser.add_argument("--file", type=Path, help="Optional source file to review")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    code = args.file.read_text(encoding="utf-8") if args.file else DEFAULT_CODE
    skill = SkillLoader().load_skill("code-reviewer")
    result = {
        "skill": skill.name,
        "status": "ok",
        "findings": review_code(code),
    }
    print(dump_json(result))


if __name__ == "__main__":
    main()
