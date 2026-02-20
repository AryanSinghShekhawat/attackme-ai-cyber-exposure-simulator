import streamlit as st
import json
from attack_engine import generate_attack_profile

st.set_page_config(
    page_title="AttackMe - AI Cyber Exposure Simulator",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- Custom Cyber Theme ----------
st.markdown("""
<style>
body {
    background-color: #0b0f19;
    color: #e6edf3;
}
.block-container {
    padding-top: 2rem;
}
h1 {
    color: #ff4b4b;
    font-weight: 800;
}
h2, h3 {
    color: #ff6b6b;
}
.stButton>button {
    background-color: #ff4b4b;
    color: white;
    font-weight: bold;
    border-radius: 10px;
    height: 3em;
    width: 100%;
}
.stSelectbox label {
    font-weight: 600;
}
.result-card {
    background-color: #141a2a;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 15px;
    border: 1px solid #1f2937;
}
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.title("🚨 AttackMe – AI Cyber Exposure Simulator")
st.markdown(
    "Simulating your **most realistic digital compromise path** based on your behavior."
)
st.write("Answer honestly. See how you would actually be breached.")

st.markdown("---")

# ---------- Input Section ----------
col1, col2 = st.columns(2)

with col1:
    reuse_passwords = st.selectbox("Do you reuse passwords?", ["Yes", "No"])
    public_social = st.selectbox("Are your social media profiles public?", ["Yes", "No"])
    two_fa = st.selectbox("Do you use 2FA on all major accounts?", ["Yes", "No"])
    public_wifi = st.selectbox("Do you use public WiFi frequently?", ["Yes", "No"])

with col2:
    click_links = st.selectbox("Do you click unknown links?", ["Often", "Sometimes", "Never"])
    share_info = st.selectbox("Do you share personal info online?", ["Yes", "No"])
    cracked_software = st.selectbox("Do you install cracked software?", ["Yes", "No"])

# ---------- Risk Score ----------
score = 0

if reuse_passwords == "Yes":
    score += 20
if public_social == "Yes":
    score += 15
if two_fa == "No":
    score += 25
if public_wifi == "Yes":
    score += 10
if click_links == "Often":
    score += 15
if share_info == "Yes":
    score += 10
if cracked_software == "Yes":
    score += 20

st.markdown("### 🔎 Behavioral Exposure Score")
st.progress(score / 100)
st.write(f"Estimated Exposure Level: **{score}%**")

st.markdown("---")

# ---------- Simulation Button ----------
if st.button("⚡ Simulate My Attack Path"):

    summary = f"""
    Password reuse: {reuse_passwords}
    Public social exposure: {public_social}
    2FA usage: {two_fa}
    Public WiFi: {public_wifi}
    Clicking unknown links: {click_links}
    Sharing personal info: {share_info}
    Cracked software usage: {cracked_software}
    """

    with st.spinner("Running behavioral compromise simulation..."):
        result = generate_attack_profile(summary)

    data = json.loads(result)

    st.success("Simulation Complete")

    st.markdown("## 🎯 Your Personalized Attack Path")

    # Cards layout
    st.markdown(f"""
    <div class="result-card">
    <h3>Entry Point</h3>
    {data["entry_point"]}
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="result-card">
    <h3>Recon Method</h3>
    {data["recon_method"]}
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="result-card">
    <h3>Exploitation Method</h3>
    {data["exploitation_method"]}
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="result-card">
    <h3>Privilege Escalation</h3>
    {data["privilege_escalation"]}
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="result-card">
    <h3>Impact</h3>
    {data["impact"]}
    </div>
    """, unsafe_allow_html=True)

    # ---------- Risk Level ----------
    risk = data["risk_level"].lower()

    st.markdown("## 🚨 Risk Assessment")

    if risk == "high":
        st.error("⚠ HIGH RISK – Immediate mitigation recommended")
    elif risk == "medium":
        st.warning("⚠ MEDIUM RISK – Significant exposure detected")
    else:
        st.success("LOW RISK – Good security posture")

    # ---------- Mitigation ----------
    st.markdown("## 🛡 Recommended Mitigation Actions")

    for action in data["mitigation_actions"]:
        st.markdown(f"- {action}")

    st.markdown("---")

    st.markdown("""
    ### Why This Matters
    Most cybersecurity tools give generic advice.
    AttackMe models how **you specifically** would be compromised.
    Prevention starts with realistic threat simulation.
    """)