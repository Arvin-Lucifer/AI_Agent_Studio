#!/usr/bin/env python3
"""L03: parallel execution for multiple tool calls.

当模型一次返回多个彼此独立的 tool_calls 时，可以并发执行工具以降低总等待时间。
并发只改变执行方式，不改变消息协议：每个结果仍然要带回对应的 tool_call_id。

建议阅读顺序：
1. 先看 load_basic_demo_module()：本文件复用 05 的工具和模型调用逻辑。
2. 再看 execute_tool_call()：它是“单个工具调用”的执行单元。
3. 最后看 run_agent_parallel()：理解多个工具如何并发执行、再统一回填消息。

Usage:
    python practice/06_parallel_function_calling.py --demo
"""

from __future__ import annotations

import argparse
import concurrent.futures
import importlib.util
import json
import time
from pathlib import Path
from typing import Any, Dict, List


def load_basic_demo_module() -> Any:
    """复用 05 的工具定义；文件名以数字开头，所以用 importlib 按路径加载。"""
    # 05_function_calling.py 以数字开头，不能直接写 import 05_function_calling。
    # importlib 按文件路径加载，可以复用 05 里的工具、注册表和 chat_once。
    module_path = Path(__file__).with_name("05_function_calling.py")
    spec = importlib.util.spec_from_file_location("l03_function_calling_basic", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module from {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# basic 相当于“基础工具调用模块”的别名。
# 这样本文件只关注并发执行，不重复定义天气、时间、计算等工具。
basic = load_basic_demo_module()


def execute_tool_call(tool_call: Any) -> Dict[str, str]:
    """执行单个工具调用，并记录耗时，便于观察并发效果。"""
    # 这个函数故意设计成无共享状态：
    # 输入一个 tool_call，输出一个 result dict，很适合放进线程池并发执行。
    name = tool_call.function.name
    args = basic.parse_tool_args(tool_call.function.arguments)
    start = time.perf_counter()
    result = basic.tool_result_for(name, args)
    duration_ms = int((time.perf_counter() - start) * 1000)
    return {
        "tool_call_id": tool_call.id,
        "name": name,
        "args": json.dumps(args, ensure_ascii=False),
        "result": result,
        "duration_ms": str(duration_ms),
    }


def run_agent_parallel(user_input: str, max_steps: int = 4, max_workers: int = 4) -> str:
    """运行支持并发工具执行的 Agent。"""
    basic.load_project_env()
    client, model = basic.build_client()
    messages: List[Dict[str, Any]] = [
        {"role": "system", "content": basic.SYSTEM_PROMPT},
        {"role": "user", "content": user_input},
    ]
    # 注意：并发发生在“执行多个工具”这一步。
    # 模型调用本身仍然是一轮一轮的：先让模型决定 tool_calls，再执行工具，再回给模型。

    print(f"\n[USER] {user_input}")
    message = basic.chat_once(client, model, messages)

    for step in range(1, max_steps + 1):
        if not message.tool_calls:
            answer = message.content or ""
            print(f"[ASSISTANT] {answer}")
            return answer

        print(f"[AGENT] step={step}, parallel_tool_calls={len(message.tool_calls)}")
        messages.append(basic.assistant_message_to_dict(message))

        # ThreadPoolExecutor 适合这里的 I/O 型工具调用；真实慢 API 可获得更明显收益。
        # 如果工具之间有依赖关系，比如“先查用户 id，再查订单”，就不能简单并发。
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(execute_tool_call, tool_call) for tool_call in message.tool_calls]
            # 按提交顺序收集结果，打印和回填消息时更容易和原始 tool_calls 对上。
            # future.result() 会等待对应工具结束；这里保留原顺序，而不是按完成先后乱序写回。
            results = [future.result() for future in futures]

        for item in results:
            print(f"[TOOL CALL] {item['name']}({item['args']}) duration_ms={item['duration_ms']}")
            print(f"[TOOL RESULT] {item['result']}")
            # 即使并发执行，回填协议没有变化：
            # 每条 tool 消息必须带自己的 tool_call_id，模型才能知道结果对应哪次调用。
            messages.append({
                "role": "tool",
                "tool_call_id": item["tool_call_id"],
                "content": item["result"],
            })

        # 所有工具结果都回填后，再让模型综合多个结果生成最终回答。
        message = basic.chat_once(client, model, messages)

    final = "工具调用轮次超过上限，已停止以避免循环。"
    print(f"[ASSISTANT] {final}")
    return final


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="L03 parallel Function Calling demo")
    parser.add_argument("prompt", nargs="?", default="", help="User prompt")
    parser.add_argument("--demo", action="store_true", help="Run demo prompt")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.demo:
        run_agent_parallel("现在几点了？北京天气怎么样？再帮我算一下 (17 * 23) + (45 / 9)。")
        return
    if not args.prompt:
        raise SystemExit("Please provide a prompt or use --demo")
    run_agent_parallel(args.prompt)


if __name__ == "__main__":
    main()
