import streamlit as st
import random

# --- 1. 页面设置 ---
st.set_page_config(page_title="朵拉的数学探险", page_icon="🏹")

# 强制大字体，iPad上更好点
st.markdown("""
    <style>
    /* 输入框字体放大，且居中 */
    .stNumberInput input { font-size: 30px !important; text-align: center; color: #1565C0; font-weight: bold; }
    /* 题目文字放大 */
    div[data-testid="stMarkdownContainer"] p { font-size: 22px; }
    div[data-testid="stMarkdownContainer"] h2 { font-size: 32px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏹 朵拉的数学探险")
st.caption("👇 直接点空白框输入答案，不用删 0 哦！")

# --- 2. 核心逻辑（初始化或获取题目） ---
if 'math_game_final' not in st.session_state:
    new_questions = []
    # 生成 10 道题
    for _ in range(10):
        # 这里的逻辑是 10 以内加减法
        a = random.randint(0, 10)
        op = random.choice(['+', '-'])
        if op == '+': 
            # 保证和不超过 10
            b = random.randint(0, 10 - a)
            ans = a + b
        else: 
            # 保证不出现负数
            b = random.randint(0, a)
            ans = a - b
        new_questions.append({"a": a, "op": op, "b": b, "ans": ans})
    st.session_state.math_game_final = new_questions

# --- 3. 题目显示区 ---
if not st.session_state.math_game_final:
    st.error("⚠️ 题目生成中...")

correct_count = 0

# 遍历题目并显示
for i, q in enumerate(st.session_state.math_game_final):
    st.divider()
    c1, c2 = st.columns([1, 1])
    
    with c1:
        # 显示算式
        st.markdown(f"**第 {i+1} 题**")
        st.markdown(f"## {q['a']} {q['op']} {q['b']} = ?")
    
    with c2:
        # 输入框
        # 注意：这里的 key 是 ans_0, ans_1 ... ans_9
        val = st.number_input(
            "请输入答案", 
            min_value=0, 
            max_value=20, 
            value=None,  
            step=1,
            placeholder="?", 
            key=f"ans_{i}", 
            label_visibility="collapsed"
        )
        
        # 实时判断
        if val is None:
            st.write("✏️ ...")
        elif val == q['ans']:
            st.success("✅ 对啦！")
            correct_count += 1
        else:
            st.warning("🤔 再想想")

# --- 4. 结算与重置 ---
st.divider()

# 全部做对显示气球
if correct_count == 10:
    st.balloons()
    st.success("🎉 太棒了！全部通关！")

# --- 修改核心在这里 ---
if st.button("🔄 换一组新题目"):
    # 1. 清除题目数据
    if 'math_game_final' in st.session_state:
        del st.session_state.math_game_final
    
    # 2. 【关键一步】循环清除 10 个输入框的缓存值
    for i in range(10):
        key_name = f"ans_{i}"
        if key_name in st.session_state:
            del st.session_state[key_name]
            
    # 3. 重新运行页面
    st.rerun()
