import streamlit as st

from math_game import (
    ANSWER_MAX,
    QUESTION_COUNT,
    Question,
    cleanup_old_rounds,
    generate_questions,
)

# --- 1. 页面设置 ---
st.set_page_config(page_title="朵拉的数学探险", page_icon="🏹")

# 强制大字体样式
st.markdown("""
    <style>
    .stNumberInput input { font-size: 30px !important; text-align: center; color: #1565C0; font-weight: bold; }
    div[data-testid="stMarkdownContainer"] p { font-size: 22px; }
    div[data-testid="stMarkdownContainer"] h2 { font-size: 32px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏹 朵拉的数学探险")
st.caption("👇 直接点空白框输入答案")

# --- 2. 核心逻辑 ---
def get_or_create_questions(round_number: int) -> list[Question]:
    """根据局数读取或生成题目。"""
    current_game_key = f"questions_round_{round_number}"
    if current_game_key not in st.session_state:
        st.session_state[current_game_key] = generate_questions(QUESTION_COUNT)
    return st.session_state[current_game_key]

# A. 初始化“游戏局数”编号 (这是强制刷新的关键！)
if "game_round" not in st.session_state:
    st.session_state.game_round = 1

# 获取当前题目
questions = get_or_create_questions(st.session_state.game_round)

# --- 3. 题目显示区 ---
correct_count = 0

for i, q in enumerate(questions):
    st.divider()
    c1, c2 = st.columns([1, 1])

    with c1:
        st.markdown(f"**第 {i+1} 题**")
        st.markdown(f"## {q.a} {q.op} {q.b} = ?")

    with c2:
        input_key = f"ans_{i}_round_{st.session_state.game_round}"

        val = st.number_input(
            "请输入答案",
            min_value=0,
            max_value=ANSWER_MAX,
            value=None,
            step=1,
            placeholder="?",
            key=input_key,
            label_visibility="collapsed"
        )

        if val is None:
            st.write("✏️ ...")
        elif val == q.ans:
            st.success("✅ 对啦！")
            correct_count += 1
        else:
            st.warning("🤔 再想想")

# --- 4. 结算与重置 ---
st.divider()

st.progress(correct_count / QUESTION_COUNT)
st.caption(f"当前进度：{correct_count}/{QUESTION_COUNT}")

if correct_count == QUESTION_COUNT:
    st.balloons()
    st.success("🎉 太棒了！全部通关！")

# 重置按钮
if st.button("🔄 换一组新题目"):
    st.session_state.game_round += 1
    cleanup_old_rounds(st.session_state, st.session_state.game_round)
    st.rerun()
