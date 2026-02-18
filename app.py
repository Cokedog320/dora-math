import streamlit as st
import random

# --- 1. 页面设置 ---
st.set_page_config(page_title="朵拉的数学探险", page_icon="🏹")，，

# 注入 CSS 样式
st.markdown("""
    <style>
    .stNumberInput input { font-size: 30px !important; text-align: center; color: #1565C0; font-weight: bold; }
    div[data-testid="stMarkdownContainer"] p { font-size: 22px; }
    div[data-testid="stMarkdownContainer"] h2 { font-size: 32px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏹 朵拉的数学探险")

# --- 2. 核心逻辑 ---
if 'game_id' not in st.session_state:
    st.session_state.game_id = 0  # 增加一个 game_id 用于强制刷新组件 key

if 'questions' not in st.session_state:
    # 生成题目
    questions = []
    for _ in range(10):
        a = random.randint(0, 10)
        op = random.choice(['+', '-'])
        if op == '+': 
            b = random.randint(0, 10 - a)
            ans = a + b
        else: 
            b = random.randint(0, a)
            ans = a - b
        questions.append({"a": a, "op": op, "b": b, "ans": ans})
    st.session_state.questions = questions

# --- 3. 题目显示区 ---
correct_count = 0
questions = st.session_state.questions
game_id = st.session_state.game_id

for i, q in enumerate(questions):
    st.divider()
    c1, c2 = st.columns([1, 1])
    
    with c1:
        st.markdown(f"**第 {i+1} 题**")
        st.markdown(f"## {q['a']} {q['op']} {q['b']} = ?")
    
    with c2:
        # 关键修改：key 中加入 game_id。
        # 当 game_id 变化时，Streamlit 会认为这是全新的组件，从而重置状态。
        val = st.number_input(
            "请输入答案", 
            min_value=0, 
            max_value=20, 
            value=None, 
            step=1,
            placeholder="?", 
            key=f"q_{game_id}_{i}",  # <--- 这里加了 game_id
            label_visibility="collapsed"
        )
        
        if val == q['ans']:
            st.success("✅ 对啦！")
            correct_count += 1
        elif val is not None:
            st.warning("🤔 再想想")

# --- 4. 结算与重置 ---
st.divider()
if correct_count == 10:
    st.balloons()
    st.success("🎉 全部通关！")

if st.button("🔄 换一组新题目"):
    # 清除旧题目
    del st.session_state.questions
    # 关键修改：更新 game_id，这会强制所有输入框重建，变为空白
    st.session_state.game_id += 1 
    st.rerun()
