import streamlit as st
import random

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

# A. 初始化“游戏局数”编号 (这是强制刷新的关键！)
if 'game_round' not in st.session_state:
    st.session_state.game_round = 1

# B. 生成题目 (绑定在当前局数上)
# 我们用 game_round 作为缓存的一部分，局数一变，题目自动重新生成
current_game_key = f"questions_round_{st.session_state.game_round}"

if current_game_key not in st.session_state:
    new_questions = []
    for _ in range(10):
        a = random.randint(0, 10)
        op = random.choice(['+', '-'])
        if op == '+': 
            b = random.randint(0, 10 - a)
            ans = a + b
        else: 
            b = random.randint(0, a)
            ans = a - b
        new_questions.append({"a": a, "op": op, "b": b, "ans": ans})
    st.session_state[current_game_key] = new_questions

# 获取当前题目
questions = st.session_state[current_game_key]

# --- 3. 题目显示区 ---
correct_count = 0

for i, q in enumerate(questions):
    st.divider()
    c1, c2 = st.columns([1, 1])
    
    with c1:
        st.markdown(f"**第 {i+1} 题**")
        st.markdown(f"## {q['a']} {q['op']} {q['b']} = ?")
    
    with c2:
        # --- 关键修改：Key 必须包含局数 ---
        # 比如第一局是 "ans_0_round_1"，第二局变成 "ans_0_round_2"
        # 名字变了，Streamlit 就不得不生成一个新的空框
        input_key = f"ans_{i}_round_{st.session_state.game_round}"
        
        val = st.number_input(
            "请输入答案", 
            min_value=0, 
            max_value=20, 
            value=None,  
            step=1,
            placeholder="?", 
            key=input_key,  # 这里用了动态 Key
            label_visibility="collapsed"
        )
        
        if val is None:
            st.write("✏️ ...")
        elif val == q['ans']:
            st.success("✅ 对啦！")
            correct_count += 1
        else:
            st.warning("🤔 再想想")

# --- 4. 结算与重置 ---
st.divider()

if correct_count == 10:
    st.balloons()
    st.success("🎉 太棒了！全部通关！")

# 重置按钮
if st.button("🔄 换一组新题目"):
    # 只需要做一件事：让局数 +1
    st.session_state.game_round += 1
    # 之前的题目数据不用管，留着也没事，反正 Key 变了取不到
    st.rerun()
