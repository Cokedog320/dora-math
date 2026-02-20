from __future__ import annotations

import random
from dataclasses import dataclass

QUESTION_COUNT = 10
MAX_OPERAND = 10
ANSWER_MAX = MAX_OPERAND
ROUNDS_TO_KEEP = 2
MIN_ADD_SUM = 6
MIN_SUB_RESULT = 3
MIN_OPERAND = 2


@dataclass(frozen=True)
class Question:
    a: int
    op: str
    b: int
    ans: int


def _generate_addition_question(randomizer: random.Random) -> Question:
    """生成十以内且不含 0/1 的加法题，且和至少为 6。"""
    total = randomizer.randint(MIN_ADD_SUM, MAX_OPERAND)
    a = randomizer.randint(MIN_OPERAND, total - MIN_OPERAND)
    b = total - a
    return Question(a=a, op="+", b=b, ans=a + b)


def _generate_subtraction_question(randomizer: random.Random) -> Question:
    """生成十以内且结果至少为 3 的减法题，且减数至少为 2。"""
    b = randomizer.randint(MIN_OPERAND, MAX_OPERAND - MIN_SUB_RESULT)
    ans = randomizer.randint(MIN_SUB_RESULT, MAX_OPERAND - b)
    a = b + ans
    return Question(a=a, op="-", b=b, ans=a - b)


def generate_questions(count: int, rng: random.Random | None = None) -> list[Question]:
    """生成十以内的加减法题，并避免过于简单（如加 0/减 0/结果 0）。"""
    randomizer = rng or random

    ops = ["+"] * (count // 2) + ["-"] * (count - count // 2)
    randomizer.shuffle(ops)

    questions: list[Question] = []
    seen: set[tuple[int, str, int]] = set()

    for op in ops:
        for _ in range(100):
            q = _generate_addition_question(randomizer) if op == "+" else _generate_subtraction_question(randomizer)
            signature = (q.a, q.op, q.b)
            if signature not in seen:
                seen.add(signature)
                questions.append(q)
                break
        else:
            # 极少出现：唯一题目空间不足时，允许重复以避免死循环。
            questions.append(_generate_addition_question(randomizer) if op == "+" else _generate_subtraction_question(randomizer))

    return questions


def cleanup_old_rounds(session_state: dict, current_round: int, rounds_to_keep: int = ROUNDS_TO_KEEP) -> None:
    """只保留最近几局题目，避免会话状态无限增长。"""
    min_round_to_keep = max(1, current_round - rounds_to_keep + 1)
    keys_to_delete = []

    for key in session_state:
        if not key.startswith("questions_round_"):
            continue

        try:
            round_no = int(key.rsplit("_", maxsplit=1)[-1])
        except ValueError:
            continue

        if round_no < min_round_to_keep:
            keys_to_delete.append(key)

    for key in keys_to_delete:
        del session_state[key]
