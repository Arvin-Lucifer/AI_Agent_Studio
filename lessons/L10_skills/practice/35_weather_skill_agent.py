#!/usr/bin/env python3
"""L10 Step 35: weather-query Skill with two tools.

这个脚本对应讲义 Case 1：天气查询 Skill。
它演示 Skill = SKILL.md 声明 + 多个 Tool + 输出约束。

默认使用 mock 数据，避免课堂依赖真实天气 API。

Usage:
    python practice/35_weather_skill_agent.py --query "北京今天天气怎么样？适合出门吗？"
"""

from __future__ import annotations

import argparse

from skill_common import (
    SkillLoader,
    build_weather_advice,
    dump_json,
    extract_city,
    get_air_quality,
    get_weather,
)


def answer_weather_query(query: str) -> dict:
    skill = SkillLoader().load_skill("weather-query")
    city = extract_city(query)
    if city is None:
        return {
            "skill": skill.name,
            "status": "need_clarification",
            "message": "请补充城市，例如：北京今天天气怎么样？",
        }

    weather = get_weather(city)
    air = get_air_quality(city)
    return {
        "skill": skill.name,
        "status": "ok" if weather.get("ok") and air.get("ok") else "partial_failed",
        "city": city,
        "weather": weather,
        "air_quality": air,
        "advice": build_weather_advice(weather, air),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="L10 weather-query Skill demo")
    parser.add_argument("--query", default="北京今天天气怎么样？适合出门吗？")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(dump_json(answer_weather_query(args.query)))


if __name__ == "__main__":
    main()
