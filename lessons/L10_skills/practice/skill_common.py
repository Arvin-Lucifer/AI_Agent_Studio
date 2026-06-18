#!/usr/bin/env python3
"""Shared helpers for L10 Skill demos.

第 10 章的主题是 Skill：把一类稳定用户意图封装成可发现、可加载、
可执行、可评测的能力包。

建议阅读顺序：
1. 先看 SkillLoader：理解 SKILL.md 如何被解析和发现。
2. 再看 weather/code_review/office 三组 mock 工具：理解 Tool 是 Skill 的执行层。
3. 最后看 route_office_skills()：理解渐进披露为什么先路由、再加载子 Skill。
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

import yaml


LESSON_DIR = Path(__file__).resolve().parents[1]
SKILLS_DIR = LESSON_DIR / "skills"
DATA_DIR = LESSON_DIR / "data"


@dataclass(frozen=True)
class SkillSpec:
    """解析后的 Skill 定义。

    metadata 是给路由器看的摘要；instructions 是触发后才加载的完整说明。
    """

    name: str
    description: str
    trigger: str
    version: str
    tags: List[str]
    instructions: str
    path: Path


class SkillLoader:
    """加载和发现 SKILL.md。

    课堂版只扫描本章 `skills/` 目录；生产系统通常会接 Skill Registry。
    """

    def __init__(self, skills_dir: Path = SKILLS_DIR):
        self.skills_dir = skills_dir

    def parse_skill_md(self, path: Path) -> SkillSpec:
        content = path.read_text(encoding="utf-8")
        parts = content.split("---", 2)
        if len(parts) < 3:
            raise ValueError(f"Invalid SKILL.md without frontmatter: {path}")
        frontmatter = yaml.safe_load(parts[1]) or {}
        instructions = parts[2].strip()
        return SkillSpec(
            name=str(frontmatter.get("name", path.parent.name)),
            description=str(frontmatter.get("description", "")).strip(),
            trigger=str(frontmatter.get("trigger", "")).strip(),
            version=str(frontmatter.get("version", "0.0.0")),
            tags=list(frontmatter.get("tags", []) or []),
            instructions=instructions,
            path=path.parent,
        )

    def discover_skills(self) -> List[SkillSpec]:
        """发现所有 SKILL.md，返回完整定义。

        注意：真实 progressive disclosure 通常只预加载 name/description。
        这里返回完整对象是为了课堂检查方便。
        """
        specs = []
        for path in sorted(self.skills_dir.rglob("SKILL.md")):
            specs.append(self.parse_skill_md(path))
        return specs

    def load_skill(self, skill_name: str) -> SkillSpec:
        matches = [spec for spec in self.discover_skills() if spec.name == skill_name]
        if not matches:
            raise KeyError(f"Skill not found: {skill_name}")
        return matches[0]


WEATHER_MOCK: Dict[str, Dict[str, Any]] = {
    "北京": {"temp": 8.5, "feels_like": 6.0, "humidity": 40, "description": "晴", "rain_probability": 10},
    "beijing": {"temp": 8.5, "feels_like": 6.0, "humidity": 40, "description": "晴", "rain_probability": 10},
    "上海": {"temp": 18.0, "feels_like": 17.5, "humidity": 82, "description": "小雨", "rain_probability": 75},
    "shanghai": {"temp": 18.0, "feels_like": 17.5, "humidity": 82, "description": "小雨", "rain_probability": 75},
    "广州": {"temp": 28.0, "feels_like": 30.0, "humidity": 70, "description": "晴", "rain_probability": 15},
    "guangzhou": {"temp": 28.0, "feels_like": 30.0, "humidity": 70, "description": "晴", "rain_probability": 15},
    "深圳": {"temp": 26.0, "feels_like": 27.0, "humidity": 65, "description": "多云", "rain_probability": 30},
    "shenzhen": {"temp": 26.0, "feels_like": 27.0, "humidity": 65, "description": "多云", "rain_probability": 30},
}

AIR_QUALITY_MOCK: Dict[str, Dict[str, Any]] = {
    "北京": {"aqi": 180, "pm25": 135, "dominant": "pm25"},
    "beijing": {"aqi": 180, "pm25": 135, "dominant": "pm25"},
    "上海": {"aqi": 45, "pm25": 18, "dominant": "o3"},
    "shanghai": {"aqi": 45, "pm25": 18, "dominant": "o3"},
    "广州": {"aqi": 75, "pm25": 35, "dominant": "pm25"},
    "guangzhou": {"aqi": 75, "pm25": 35, "dominant": "pm25"},
    "深圳": {"aqi": 60, "pm25": 28, "dominant": "pm25"},
    "shenzhen": {"aqi": 60, "pm25": 28, "dominant": "pm25"},
}


def get_weather(city: str) -> Dict[str, Any]:
    key = city.strip().lower()
    data = WEATHER_MOCK.get(city) or WEATHER_MOCK.get(key)
    if data is None:
        return {"ok": False, "city": city, "error": "未找到城市天气数据"}
    return {"ok": True, "city": city, **data, "source": "mock"}


def get_air_quality(city: str) -> Dict[str, Any]:
    key = city.strip().lower()
    data = AIR_QUALITY_MOCK.get(city) or AIR_QUALITY_MOCK.get(key)
    if data is None:
        return {"ok": False, "city": city, "error": "未找到城市空气质量数据"}
    return {"ok": True, "city": city, **data, "source": "mock"}


def extract_city(text: str) -> str | None:
    for city in ["北京", "上海", "广州", "深圳", "beijing", "shanghai", "guangzhou", "shenzhen"]:
        if city.lower() in text.lower():
            return city
    return None


def build_weather_advice(weather: Dict[str, Any], air: Dict[str, Any]) -> List[str]:
    advice = []
    if not weather.get("ok") or not air.get("ok"):
        return ["数据不足，无法给出可靠出行建议。"]
    if weather["temp"] < 10:
        advice.append("气温偏低，建议穿厚外套或羽绒服。")
    if weather["rain_probability"] > 60:
        advice.append("降雨概率较高，建议带伞。")
    if air["aqi"] > 150:
        advice.append("空气质量较差，减少户外活动，必要时戴口罩。")
    if air["aqi"] < 50 and weather["description"] == "晴":
        advice.append("天气和空气质量都不错，适合户外运动。")
    return advice or ["整体条件正常，按日常安排出行即可。"]


def review_code(code: str) -> List[Dict[str, Any]]:
    """课堂版静态审查器。

    重点不是覆盖所有漏洞，而是演示 Skill 如何把检查维度固化下来。
    """
    findings: List[Dict[str, Any]] = []
    if re.search(r"f[\"'].*select .*where", code, flags=re.IGNORECASE | re.DOTALL):
        findings.append(
            {
                "severity": "critical",
                "category": "security",
                "location": "SQL query construction",
                "description": "疑似使用 f-string 拼接 SQL，存在 SQL 注入风险。",
                "fix": "使用参数化查询，例如 db.execute('SELECT * FROM users WHERE id = ?', [user_id])。",
                "confidence": 0.92,
            }
        )
    if re.search(r"(api_key|secret|password)\s*=\s*['\"][^'\"]+['\"]", code, flags=re.IGNORECASE):
        findings.append(
            {
                "severity": "critical",
                "category": "security",
                "location": "credential assignment",
                "description": "疑似硬编码密钥或密码。",
                "fix": "改为从环境变量、密钥管理服务或运行时配置读取。",
                "confidence": 0.86,
            }
        )
    if "eval(" in code:
        findings.append(
            {
                "severity": "critical",
                "category": "security",
                "location": "eval",
                "description": "直接执行 eval 可能导致任意代码执行。",
                "fix": "使用安全解析器或白名单表达式求值。",
                "confidence": 0.9,
            }
        )
    if not findings:
        findings.append(
            {
                "severity": "suggestion",
                "category": "maintainability",
                "location": "general",
                "description": "未发现高风险问题；建议补充测试和错误处理说明。",
                "fix": "添加边界输入测试，并在 PR 描述中写清影响范围。",
                "confidence": 0.6,
            }
        )
    return findings


OFFICE_KEYWORDS = {
    "schedule-manager": ["安排会议", "会议", "日程", "有空", "预约", "日历"],
    "email-notifier": ["发邮件", "邮件", "通知", "提醒", "告知"],
    "doc-generator": ["生成文档", "会议纪要", "周报", "项目总结", "模板", "创建文档"],
}


def route_office_skills(user_text: str) -> Tuple[List[str], str]:
    """规则路由模拟 office-router。

    真实系统可用 LLM JSON 路由；课堂版用规则保证可重复。
    """
    selected = []
    for skill_name, keywords in OFFICE_KEYWORDS.items():
        if any(keyword in user_text for keyword in keywords):
            selected.append(skill_name)
    if not selected:
        return [], "未命中办公子技能，需要澄清用户意图。"
    order = ["schedule-manager", "email-notifier", "doc-generator"]
    selected = [name for name in order if name in selected]
    return selected, "根据关键词命中并按依赖顺序排列。"


def check_availability(date: str, start_hour: int, end_hour: int) -> Dict[str, Any]:
    busy_slots = [(10, 11), (14, 15)]
    conflict = any(not (end_hour <= start or start_hour >= end) for start, end in busy_slots)
    return {
        "date": date,
        "requested": f"{start_hour}:00-{end_hour}:00",
        "available": not conflict,
        "busy_slots": [f"{start}:00-{end}:00" for start, end in busy_slots],
    }


def create_event(title: str, date: str, start_time: str, end_time: str, attendees: Iterable[str]) -> Dict[str, Any]:
    return {
        "status": "preview_required",
        "title": title,
        "date": date,
        "start_time": start_time,
        "end_time": end_time,
        "attendees": list(attendees),
        "message": "创建会议属于写操作，真实执行前需要用户确认。",
    }


def send_email(to: Iterable[str], subject: str, body: str) -> Dict[str, Any]:
    return {
        "status": "preview_required",
        "to": list(to),
        "subject": subject,
        "body": body,
        "message": "发送邮件属于对外副作用操作，真实发送前需要用户确认。",
    }


def create_doc(title: str, content: str) -> Dict[str, Any]:
    return {
        "status": "created_mock",
        "title": title,
        "url": "https://docs.example.local/mock-doc-001",
        "content_preview": content[:120],
    }


def dump_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)
