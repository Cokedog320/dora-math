 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/README.md b/README.md
index 12c526fc3d3d2f68976dde21d0bbb9d2ca5405cb..d2ca5c272d336161a8984a98606ffb83f4afe573 100644
--- a/README.md
+++ b/README.md
@@ -1,2 +1,211 @@
 # dora-math
-朵拉的数学练习
+
+朵拉的十以内加减法练习小程序（Streamlit）。
+
+## 给小白的最简单用法
+
+### 1) 安装依赖
+```bash
+pip install streamlit
+```
+
+### 2) 启动程序
+```bash
+streamlit run app.py
+```
+
+浏览器打开后，就可以开始做题。
+
+---
+
+## 你可以直接复制粘贴的代码（按文件覆盖）
+
+> 下面 2 个文件是核心。你如果把旧代码删乱了，直接按文件名覆盖即可。
+
+### `app.py`
+```python
+import streamlit as st
+
+from math_game import (
+    ANSWER_MAX,
+    QUESTION_COUNT,
+    Question,
+    cleanup_old_rounds,
+    generate_questions,
+)
+
+# --- 1. 页面设置 ---
+st.set_page_config(page_title="朵拉的数学探险", page_icon="🏹")
+
+# 强制大字体样式
+st.markdown("""
+    <style>
+    .stNumberInput input { font-size: 30px !important; text-align: center; color: #1565C0; font-weight: bold; }
+    div[data-testid="stMarkdownContainer"] p { font-size: 22px; }
+    div[data-testid="stMarkdownContainer"] h2 { font-size: 32px; }
+    </style>
+    """, unsafe_allow_html=True)
+
+st.title("🏹 朵拉的数学探险")
+st.caption("👇 直接点空白框输入答案")
+
+# --- 2. 核心逻辑 ---
+
+def get_or_create_questions(round_number: int) -> list[Question]:
+    """根据局数读取或生成题目。"""
+    current_game_key = f"questions_round_{round_number}"
+    if current_game_key not in st.session_state:
+        st.session_state[current_game_key] = generate_questions(QUESTION_COUNT)
+    return st.session_state[current_game_key]
+
+
+# A. 初始化“游戏局数”编号 (这是强制刷新的关键！)
+if "game_round" not in st.session_state:
+    st.session_state.game_round = 1
+
+# 获取当前题目
+questions = get_or_create_questions(st.session_state.game_round)
+
+# --- 3. 题目显示区 ---
+correct_count = 0
+
+for i, q in enumerate(questions):
+    st.divider()
+    c1, c2 = st.columns([1, 1])
+
+    with c1:
+        st.markdown(f"**第 {i+1} 题**")
+        st.markdown(f"## {q.a} {q.op} {q.b} = ?")
+
+    with c2:
+        # --- 关键修改：Key 必须包含局数 ---
+        # 比如第一局是 "ans_0_round_1"，第二局变成 "ans_0_round_2"
+        # 名字变了，Streamlit 就不得不生成一个新的空框
+        input_key = f"ans_{i}_round_{st.session_state.game_round}"
+
+        val = st.number_input(
+            "请输入答案",
+            min_value=0,
+            max_value=ANSWER_MAX,
+            value=None,
+            step=1,
+            placeholder="?",
+            key=input_key,
+            label_visibility="collapsed"
+        )
+
+        if val is None:
+            st.write("✏️ ...")
+        elif val == q.ans:
+            st.success("✅ 对啦！")
+            correct_count += 1
+        else:
+            st.warning("🤔 再想想")
+
+# --- 4. 结算与重置 ---
+st.divider()
+
+st.progress(correct_count / QUESTION_COUNT)
+st.caption(f"当前进度：{correct_count}/{QUESTION_COUNT}")
+
+if correct_count == QUESTION_COUNT:
+    st.balloons()
+    st.success("🎉 太棒了！全部通关！")
+
+# 重置按钮
+if st.button("🔄 换一组新题目"):
+    # 只需要做一件事：让局数 +1
+    st.session_state.game_round += 1
+    cleanup_old_rounds(st.session_state, st.session_state.game_round)
+    st.rerun()
+```
+
+### `math_game.py`
+```python
+from __future__ import annotations
+
+import random
+from dataclasses import dataclass
+
+QUESTION_COUNT = 10
+MAX_OPERAND = 10
+ANSWER_MAX = MAX_OPERAND
+ROUNDS_TO_KEEP = 2
+
+
+@dataclass(frozen=True)
+class Question:
+    a: int
+    op: str
+    b: int
+    ans: int
+
+
+def _generate_addition_question(randomizer: random.Random) -> Question:
+    """生成十以内且不含 0 的加法题。"""
+    a = randomizer.randint(1, MAX_OPERAND - 1)
+    b = randomizer.randint(1, MAX_OPERAND - a)
+    return Question(a=a, op="+", b=b, ans=a + b)
+
+
+def _generate_subtraction_question(randomizer: random.Random) -> Question:
+    """生成十以内且结果大于 0 的减法题。"""
+    a = randomizer.randint(2, MAX_OPERAND)
+    b = randomizer.randint(1, a - 1)
+    return Question(a=a, op="-", b=b, ans=a - b)
+
+
+def generate_questions(count: int, rng: random.Random | None = None) -> list[Question]:
+    """生成十以内的加减法题，并避免过于简单（如加 0/减 0/结果 0）。"""
+    randomizer = rng or random
+
+    ops = ["+"] * (count // 2) + ["-"] * (count - count // 2)
+    randomizer.shuffle(ops)
+
+    questions: list[Question] = []
+    seen: set[tuple[int, str, int]] = set()
+
+    for op in ops:
+        for _ in range(100):
+            q = _generate_addition_question(randomizer) if op == "+" else _generate_subtraction_question(randomizer)
+            signature = (q.a, q.op, q.b)
+            if signature not in seen:
+                seen.add(signature)
+                questions.append(q)
+                break
+        else:
+            # 极少出现：唯一题目空间不足时，允许重复以避免死循环。
+            questions.append(_generate_addition_question(randomizer) if op == "+" else _generate_subtraction_question(randomizer))
+
+    return questions
+
+
+def cleanup_old_rounds(session_state: dict, current_round: int, rounds_to_keep: int = ROUNDS_TO_KEEP) -> None:
+    """只保留最近几局题目，避免会话状态无限增长。"""
+    min_round_to_keep = max(1, current_round - rounds_to_keep + 1)
+    keys_to_delete = []
+
+    for key in session_state:
+        if not key.startswith("questions_round_"):
+            continue
+
+        try:
+            round_no = int(key.rsplit("_", maxsplit=1)[-1])
+        except ValueError:
+            continue
+
+        if round_no < min_round_to_keep:
+            keys_to_delete.append(key)
+
+    for key in keys_to_delete:
+        del session_state[key]
+```
+
+---
+
+## 自检命令（可选）
+
+```bash
+pytest -q
+python -m py_compile app.py math_game.py tests/test_math_game.py tests/conftest.py
+```
 
EOF
)
