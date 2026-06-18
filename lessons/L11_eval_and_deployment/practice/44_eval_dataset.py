"""L11 Step 44: build and inspect an Agent evaluation dataset.

Run:
    python practice/44_eval_dataset.py

The dataset is small on purpose.  A useful first eval set should cover factual
questions, chitchat, edge cases, completeness, and security probes before it
tries to become large.
"""

from __future__ import annotations

from eval_deploy_common import EVAL_DATASET, export_dataset


def main() -> None:
    path = export_dataset()
    print(f"[OK] eval dataset saved: {path}")
    print(f"评测数据集共 {len(EVAL_DATASET)} 条用例")
    for case in EVAL_DATASET:
        expected_tool = case.expected_tool or "None"
        print(f"- [{case.category:12s}] tool={expected_tool:22s} {case.question or '<EMPTY>'}")


if __name__ == "__main__":
    main()
