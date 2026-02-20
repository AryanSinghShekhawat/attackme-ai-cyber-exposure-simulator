import streamlit as st
import json
from attack_engine import generate_attack_profile

st.set_page_config(page_title="AttackMe - AI Cyber Exposure Simulator", layout="wide")
st.markdown("""
<style>
body {
    background-color: #0f1117;
    color: white;
}
h1, h2, h3 {
    color: #ff4b4b;
}
</style>
""", unsafe_allow_html=True)


st.title(" AttackMe – AI Cyber Exposure Simulator")
st.write("Answer honestly. See your most likely compromise path.")

reuse_passwords = st.selectbox("Do you reuse passwords?", ["Yes", "No"])
public_social = st.selectbox("Are your social media profiles public?", ["Yes", "No"])
two_fa = st.selectbox("Do you use 2FA on all major accounts?", ["Yes", "No"])
public_wifi = st.selectbox("Do you use public WiFi frequently?", ["Yes", "No"])
click_links = st.selectbox("Do you click unknown links?", ["Often", "Sometimes", "Never"])
share_info = st.selectbox("Do you share personal info online?", ["Yes", "No"])
cracked_software = st.selectbox("Do you install cracked software?", ["Yes", "No"])
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
if st.button("Simulate My Attack Path"):

    summary = f"""
    Password reuse: {reuse_passwords}
    Public social exposure: {public_social}
    2FA usage: {two_fa}
    Public WiFi: {public_wifi}
    Clicking unknown links: {click_links}
    Sharing personal info: {share_info}
    Cracked software usage: {cracked_software}
    """

    with st.spinner("Simulating your compromise path..."):
        result = generate_attack_profile(summary)

    data = json.loads(result)

    st.subheader(" Your Attack Simulation")

    st.markdown("###  Entry Point")
    st.write(data["entry_point"])

    st.markdown("###  Recon Method")
    st.write(data["recon_method"])

    st.markdown("###  Exploitation Method")
    st.write(data["exploitation_method"])

    st.markdown("###  Privilege Escalation")
    st.write(data["privilege_escalation"])

    st.markdown("###  Impact")
    st.write(data["impact"])

    risk = data["risk_level"]

    if risk.lower() == "high":
        st.error("⚠ HIGH RISK")
    elif risk.lower() == "medium":
        st.warning("⚠ MEDIUM RISK")
    else:
        st.success("LOW RISK")

    st.markdown("### 🛡 Top 5 Mitigation Actions")
    for action in data["mitigation_actions"]:
        st.write("•", action)