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

# --- 2. 核心逻辑（带缓存） ---
if 'math_game_final' not in st.session_state:
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
    st.session_state.math_game_final = new_questions

# --- 3. 题目显示区 ---
# 检查题目是否生成
if not st.session_state.math_game_final:
    st.error("⚠️ 题目生成失败，请点击下方的重置按钮")

correct_count = 0

for i, q in enumerate(st.session_state.math_game_final):
    st.divider()
    # 两列布局
    c1, c2 = st.columns([1, 1])
    
    with c1:
        # 显示题目
        st.markdown(f"**第 {i+1} 题**")
        st.markdown(f"## {q['a']} {q['op']} {q['b']} = ?")
    
    with c2:
        # --- 核心修改点在这里 ---
        # value=None 让框框默认是空的
        # placeholder="?" 给一个灰色问号提示
        val = st.number_input(
            "请输入答案", 
            min_value=0, 
            max_value=20, 
            value=None,  # 这里的 None 是关键，去掉了 0
            step=1,
            placeholder="?", 
            key=f"ans_{i}", 
            label_visibility="collapsed"
        )
        
        # 实时判断逻辑
        if val is None:
            # 如果是空的，显示占位符
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
    # 清除缓存，重来
    del st.session_state.math_game_final
    st.rerun()
