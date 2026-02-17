import streamlit as st
import random

# --- 1. 探险家视觉风格 ---
st.set_page_config(page_title="朵拉的数学探险", page_icon="🏹")

st.markdown("""
    <style>
    .main { background-color: #f0f7ff; }
    .q-card {
        background: white; padding: 20px; border-radius: 15px; 
        border-left: 10px solid #4a90e2; margin-bottom: 20px;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
    }
    .q-text { font-size: 26px; font-weight: bold; color: #333; }
    .stNumberInput input { font-size: 28px !important; text-align: center; color: #4a90e2; }
    .stButton>button { 
        background-color: #4a90e2 !important; color: white !important; 
        font-size: 22px !important; border-radius: 50px !important; height: 3em !important; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 逻辑：生成 10 道题 (已修复 Bug) ---
if 'expedition_questions' not in st.session_state:
    questions = []
    for _ in range(10):
        a = random.randint(0, 10)
        op = random.choice(['+', '-'])
        if op == '+':
            # 这里的 0 确保了就算 a 是 10，也能生成 10 + 0
            b = random.randint(0, 10 - a) 
            ans = a + b
        else:
            b = random.randint(0, a)
            ans = a - b
        questions.append({"a": a, "op": op, "b": b, "ans": ans})
    st.session_state.expedition_questions = questions

# --- 3. 界面展示 ---
st.title("🏹 朵拉的数学探险")
st.write("勇敢的小探险家，准备好挑战这 10 道题了吗？")

user_ans = []
with st.form("math_form"):
    for i, q in enumerate(st.session_state.expedition_questions):
        st.markdown(f"<div class='q-card'><span class='q-text'>第 {i+1} 题：&nbsp;&nbsp; {q['a']} {q['op']} {q['b']} = ?</span></div>", unsafe_allow_html=True)
        ans = st.number_input(f"答案{i}", min_value=0, max_value=20, value=None, key=f"ans_{i}", label_visibility="collapsed")
        user_ans.append(ans)
    
    st.write("")
    submit = st.form_submit_button("🏁 提交并查看成绩")

# --- 4. 判卷反馈 ---
if submit:
    score = sum(1 for i, q in enumerate(st.session_state.expedition_questions) if user_ans[i] == q['ans'])
    st.divider()
    if score == 10:
        st.balloons()
        st.success("🎊 太棒了！满分通关！你是最厉害的探险家！")
    else:
        st.info(f"📊 探险结束！你获得了 {score} 枚勋章！继续加油！")
    
    if st.button("再来一轮"):
        del st.session_state.expedition_questions
        st.rerun()
