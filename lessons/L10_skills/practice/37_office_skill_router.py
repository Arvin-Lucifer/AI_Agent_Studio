#!/usr/bin/env python3
"""L10 Step 37: office Skill router with progressive disclosure.

这个脚本对应讲义 Case 3：办公助手 Skill。
它演示“先路由，再按需加载子 Skill”的渐进披露：

1. office-router 只做意图判断。
2. 命中后才加载 schedule/email/doc 子 Skill。
3. 写操作默认返回 preview_required，提醒真实执行前需要用户确认。

Usage:
    python practice/37_office_skill_router.py
"""

from __future__ import annotations

import argparse
import re

from skill_common import (
    SkillLoader,
    check_availability,
    create_doc,
    create_event,
    dump_json,
    route_office_skills,
    send_email,
)


def _extract_emails(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)


def run_office_request(query: str) -> dict:
    loader = SkillLoader()
    router = loader.load_skill("office-router")
    skills, reason = route_office_skills(query)

    trace = [{"stage": "route", "router": router.name, "skills": skills, "reason": reason}]
    results = []
    attendees = _extract_emails(query)

    for skill_name in skills:
        skill = loader.load_skill(skill_name)
        trace.append({"stage": "load_skill", "skill": skill.name, "instructions_chars": len(skill.instructions)})
        if skill_name == "schedule-manager":
            availability = check_availability("2026-05-01", 9, 10)
            event_preview = create_event(
                title="项目评审会",
                date="2026-05-01",
                start_time="09:00",
                end_time="10:00",
                attendees=attendees,
            )
            results.extend([availability, event_preview])
        elif skill_name == "email-notifier":
            results.append(
                send_email(
                    to=attendees,
                    subject="项目评审会通知",
                    body="请参加 2026-05-01 09:00-10:00 的项目评审会。",
                )
            )
        elif skill_name == "doc-generator":
            results.append(
                create_doc(
                    title="项目评审会会议纪要模板",
                    content="## 会议主题\n项目评审会\n\n## 参会人\n- 待补充\n\n## 结论\n- 待补充\n",
                )
            )

    return {
        "status": "ok" if skills else "need_clarification",
        "query": query,
        "trace": trace,
        "results": results,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="L10 office progressive Skill router demo")
    parser.add_argument(
        "--query",
        default="帮我安排2026年5月1日上午9-10点的项目评审会，邀请 alice@example.com 和 bob@example.com，并发邮件通知他们，同时创建会议纪要模板。",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(dump_json(run_office_request(args.query)))


if __name__ == "__main__":
    main()
