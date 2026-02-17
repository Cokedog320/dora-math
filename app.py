import streamlit as st
import random

# --- 1. 探险家视觉风格 ---
st.set_page_config(page_title="朵拉的数学探险", page_icon="🏹")

st.markdown("""
    <style>
    .main { background-color: #fdf6e3; }
    .q-card {
        background: white; padding: 25px; border-radius: 15px; 
        border-left: 10px solid #ffaa00; margin-bottom: 20px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    .q-text { font-size: 28px; font-weight: bold; color: #2e7d32; }
    .stNumberInput input { font-size: 30px !important; text-align: center; color: #1e88e5; }
    .stButton>button { 
        background-color: #f57c00 !important; color: white !important; 
        font-size: 24px !important; border-radius: 50px !important; height: 3em !important; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 一次性生成 10 道题 ---
if 'quest_set' not in st.session_state:
    q_list = []
    for _ in range(10):
        a = random.randint(1, 10)
        op = random.choice(['+', '-'])
        if op == '+':
            b = random.randint(1, 10 - a)
            ans = a + b
        else:
            b = random.randint(1, a)
            ans = a - b
        q_list.append({"a": a, "op": op, "b": b, "ans": ans})
    st.session_state.quest_set = q_list

# --- 3. 页面展示 ---
st.title("🏹 朵拉的数学大探险")
st.write("勇敢的小探险家，完成这 10 道关卡即可获得勋章！")

user_ans = []
with st.form("adventure_form"):
    for i, q in enumerate(st.session_state.quest_set):
        st.markdown(f"<div class='q-card'><span class='q-text'>第 {i+1} 关： {q['a']} {q['op']} {q['b']} = ?</span></div>", unsafe_allow_html=True)
        ans = st.number_input(f"答案{i}", min_value=0, max_value=20, value=None, key=f"ans_{i}", label_visibility="collapsed")
        user_ans.append(ans)
    
    submit = st.form_submit_button("🏁 闯关结束，查看成绩！")

# --- 4. 判卷反馈 ---
if submit:
    score = sum(1 for i, q in enumerate(st.session_state.quest_set) if user_ans[i] == q['ans'])
    st.divider()
    if score == 10:
        st.balloons()
        st.success("🎊 满分！你是最棒的探险家！勋章已发送！")
    else:
        st.info(f"📊 探险结束！你获得了 {score} 枚勋章！")
    
    if st.button("开启新一轮探险"):
        del st.session_state.quest_set
        st.rerun()
