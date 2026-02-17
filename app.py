import streamlit as st
import random

# --- 1. 基础设置 ---
st.set_page_config(page_title="朵拉数学探险", page_icon="🏹")

# 设置字体大一点，方便看
st.markdown("""
    <style>
    .stNumberInput input { font-size: 30px !important; text-align: center; font-weight: bold; color: #1565C0; }
    div[data-testid="stMetricValue"] { font-size: 40px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏹 朵拉的数学探险")
st.caption("👇 填入答案后，记得按回车(Enter)或者点一下空白处哦！")

# --- 2. 题目生成逻辑 ---
if 'questions' not in st.session_state:
    st.session_state.questions = []
    for _ in range(10):
        a = random.randint(0, 10)
        op = random.choice(['+', '-'])
        if op == '+': 
            b = random.randint(0, 10 - a)
            ans = a + b
        else: 
            b = random.randint(0, a)
            ans = a - b
        st.session_state.questions.append({"a": a, "op": op, "b": b, "ans": ans})

# --- 3. 答题区 ---
correct_count = 0

for i, q in enumerate(st.session_state.questions):
    # 使用列布局：左边题目，右边输入框
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(f"第 {i+1} 题： {q['a']} {q['op']} {q['b']} = ❓")
    
    with col2:
        # 输入框
        user_val = st.number_input(f"答案{i}", min_value=0, max_value=20, value=0, key=f"q_{i}", label_visibility="collapsed")

    # 实时判断
    if user_val == q['ans']:
        st.success(f"✅ 答对啦！答案是 {q['ans']}")
        correct_count += 1
    elif user_val != 0:
        st.warning("🤔 再算算？")
    else:
        st.write("waiting...") # 占位符
    
    st.divider()

# --- 4. 全对奖励 ---
if correct_count == 10:
    st.balloons()
    st.markdown("## 🎊 哇！10道题全对！朵拉太棒了！")
    if st.button("🔄 再来一组新题"):
        del st.session_state.questions
        st.rerun()
