import random

from math_game import (
    ANSWER_MAX,
    MAX_OPERAND,
    MIN_ADD_SUM,
    MIN_OPERAND,
    MIN_SUB_RESULT,
    cleanup_old_rounds,
    generate_questions,
)


def test_generate_questions_is_deterministic_with_seed():
    questions_a = generate_questions(5, rng=random.Random(42))
    questions_b = generate_questions(5, rng=random.Random(42))

    assert len(questions_a) == 5
    assert questions_a == questions_b


def test_generate_questions_are_within_range_and_non_trivial():
    rng = random.Random(0)
    questions = generate_questions(100, rng=rng)

    plus_count = 0
    minus_count = 0
    for q in questions:
        assert MIN_OPERAND <= q.a <= MAX_OPERAND
        assert MIN_OPERAND <= q.b <= MAX_OPERAND
        assert q.op in {"+", "-"}
        assert 1 <= q.ans <= ANSWER_MAX
        if q.op == "+":
            plus_count += 1
            assert q.ans == q.a + q.b
            assert q.ans <= MAX_OPERAND
            assert q.ans >= MIN_ADD_SUM
        else:
            minus_count += 1
            assert q.ans == q.a - q.b
            assert q.a > q.b
            assert q.ans >= MIN_SUB_RESULT

    assert abs(plus_count - minus_count) <= 1


def test_generate_questions_avoids_duplicates_when_possible():
    rng = random.Random(1)
    questions = generate_questions(10, rng=rng)

    signatures = {(q.a, q.op, q.b) for q in questions}
    assert len(signatures) == len(questions)


def test_cleanup_old_rounds_keeps_recent_rounds_only():
    state = {
        "questions_round_1": [1],
        "questions_round_2": [2],
        "questions_round_3": [3],
        "questions_round_4": [4],
        "ans_0_round_4": 2,
        "other_key": "keep",
    }

    cleanup_old_rounds(state, current_round=4, rounds_to_keep=2)

    assert "questions_round_1" not in state
    assert "questions_round_2" not in state
    assert "questions_round_3" in state
    assert "questions_round_4" in state
    assert state["ans_0_round_4"] == 2
    assert state["other_key"] == "keep"
