"""L11 Step 45: run automated Agent evaluation.

Run:
    python practice/45_eval_runner.py

This script improves the teacher's baseline runner in three ways:
1. it checks expected tool calls, not only final text;
2. it keeps safety as a separate hard gate;
3. it persists JSON results for later regression comparison.
"""

from __future__ import annotations

from eval_deploy_common import DATA_DIR, EVAL_DATASET, MockAgent, run_eval, save_json


def main() -> None:
    summary = run_eval(MockAgent(), EVAL_DATASET)
    result_path = DATA_DIR / "eval_results.json"
    save_json(result_path, summary)

    print("=" * 60)
    print("Agent 自动化评测")
    print("=" * 60)
    print(f"总用例数: {summary['total_cases']}")
    print(f"平均得分: {summary['average_score']}")
    print(f"通过/失败: {summary['passed']}/{summary['failed']}")
    print(f"结果文件: {result_path}")

    print("\n各类别得分:")
    for category, stats in summary["by_category"].items():
        print(f"- {category:12s}: {stats['avg_score']:.2f} ({stats['count']} 条)")

    print("\n失败或低分样例:")
    low_score = [item for item in summary["details"] if item["score"] < 0.8]
    if not low_score:
        print("- 无，当前 mock Agent 通过基线评测。")
    for item in low_score:
        print(f"- #{item['id']} score={item['score']} question={item['question']}")


if __name__ == "__main__":
    main()
