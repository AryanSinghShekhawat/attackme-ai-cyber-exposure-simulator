import streamlit as st
import json
from attack_engine import generate_attack_profile
import pandas as pd
import matplotlib.pyplot as plt
from report_generator import generate_pdf_report
if "risk_history" not in st.session_state:
    st.session_state.risk_history = []

# =============================
# PAGE CONFIG
# =============================
st.set_page_config(
    page_title="AttackMe | AI Cyber Exposure Simulator",
    page_icon="🛡️",
    layout="wide"
)

# =============================
# PROFESSIONAL DARK THEME
# =============================
st.markdown("""
<style>
body {
    background-color: #0f172a;
    color: #e2e8f0;
}
.block-container {
    padding-top: 2rem;
}
h1 {
    color: #ef4444;
    font-weight: 800;
}
h2, h3 {
    color: #f87171;
}
.stButton>button {
    background: linear-gradient(90deg, #ef4444, #dc2626);
    color: white;
    font-weight: 600;
    border-radius: 8px;
    height: 3em;
    width: 100%;
}
.result-card {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 15px;
    border: 1px solid #334155;
}
.metric-box {
    background-color: #1e293b;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #334155;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# =============================
# HEADER
# =============================
st.title("🛡️ AttackMe – AI Cyber Exposure Simulator")
st.markdown("""
**Enterprise-grade behavioral threat modeling simulation.**  
This engine predicts your most probable compromise pathway based on digital behavior patterns.
""")

st.divider()

# =============================
# INPUT SECTION
# =============================
col1, col2 = st.columns(2)

with col1:
    reuse_passwords = st.selectbox("Password Reuse Across Platforms", ["Yes", "No"])
    public_social = st.selectbox("Public Social Media Presence", ["Yes", "No"])
    two_fa = st.selectbox("Multi-Factor Authentication Enabled", ["Yes", "No"])
    public_wifi = st.selectbox("Frequent Public WiFi Usage", ["Yes", "No"])

with col2:
    click_links = st.selectbox("Interaction with Unknown Links", ["Often", "Sometimes", "Never"])
    share_info = st.selectbox("Sharing Personal Data Online", ["Yes", "No"])
    cracked_software = st.selectbox("Installation of Unverified/Cracked Software", ["Yes", "No"])

# =============================
# SCORING ENGINE (Structured & Normalized)
# =============================

risk_weights = {
    "reuse_passwords": 20,
    "public_social": 15,
    "two_fa": 25,
    "public_wifi": 10,
    "click_links_often": 15,
    "click_links_sometimes": 8,
    "share_info": 10,
    "cracked_software": 20
}

score = 0

if reuse_passwords == "Yes":
    score += risk_weights["reuse_passwords"]

if public_social == "Yes":
    score += risk_weights["public_social"]

if two_fa == "No":
    score += risk_weights["two_fa"]

if public_wifi == "Yes":
    score += risk_weights["public_wifi"]

if click_links == "Often":
    score += risk_weights["click_links_often"]
elif click_links == "Sometimes":
    score += risk_weights["click_links_sometimes"]

if share_info == "Yes":
    score += risk_weights["share_info"]

if cracked_software == "Yes":
    score += risk_weights["cracked_software"]

# Normalize score to 0–100 scale
MAX_POSSIBLE_SCORE = sum(risk_weights.values())
normalized_score = round((score / MAX_POSSIBLE_SCORE) * 100)
st.session_state.risk_history.append(normalized_score)
# =============================
# Attack Probability Graph
# =============================

st.markdown("## 📈 Attack Vector Probability Model")

attack_vectors = {
    "Phishing": normalized_score * 0.9,
    "Credential Stuffing": normalized_score * 0.8,
    "Malware Injection": normalized_score * 0.7,
    "Session Hijacking": normalized_score * 0.6,
    "Social Engineering": normalized_score * 0.85
}

# =============================
# MITRE ATT&CK Mapping
# =============================

MITRE_MAPPING = {
    "Phishing": "T1566 – Phishing",
    "Credential Stuffing": "T1110 – Brute Force",
    "Malware Injection": "T1204 – User Execution",
    "Session Hijacking": "T1539 – Steal Web Session Cookie",
    "Social Engineering": "T1598 – Phishing for Information"
}

st.markdown("## 🧠 MITRE ATT&CK Mapping")

for vector in attack_vectors.keys():
    st.markdown(f"- **{vector}** → {MITRE_MAPPING.get(vector)}")

df = pd.DataFrame({
    "Attack Vector": attack_vectors.keys(),
    "Probability (%)": attack_vectors.values()
})

fig, ax = plt.subplots()
ax.bar(df["Attack Vector"], df["Probability (%)"])
ax.set_ylabel("Probability (%)")
ax.set_xticklabels(df["Attack Vector"], rotation=45)

st.pyplot(fig)

st.markdown("## 📊 Risk Trend Over Time")

trend_df = pd.DataFrame({
    "Assessment #": range(1, len(st.session_state.risk_history)+1),
    "Risk Score": st.session_state.risk_history
})

st.line_chart(trend_df.set_index("Assessment #"))

# =============================
# RISK DASHBOARD
# =============================

st.markdown("## 📊 Behavioral Exposure Score")

colA, colB = st.columns([2, 1])

with colA:
    st.progress(normalized_score)

with colB:
    st.markdown(f"""
    <div class="metric-box">
    <h2>{normalized_score}%</h2>
    <p>Exposure Level</p>
    </div>
    """, unsafe_allow_html=True)

# Risk Category Logic
if normalized_score >= 75:
    st.error("CRITICAL RISK – High probability of targeted compromise")
elif normalized_score >= 50:
    st.warning("ELEVATED RISK – Multiple exploitable vectors detected")
else:
    st.success("MODERATE / LOW RISK – Limited attack surface exposure")

st.divider()

# =============================
# SIMULATION ENGINE
# =============================

if st.button("⚡ Run Threat Simulation"):

    summary = f"""
    Password reuse: {reuse_passwords}
    Public social exposure: {public_social}
    MFA enabled: {two_fa}
    Public WiFi usage: {public_wifi}
    Unknown link interaction: {click_links}
    Sharing personal info: {share_info}
    Cracked software usage: {cracked_software}
    """

    with st.spinner("Executing AI behavioral threat modeling..."):
        try:
            result = generate_attack_profile(summary)
            data = json.loads(result)

        except Exception as e:
            st.error("Simulation failed. Please verify backend configuration.")
            st.stop()

    st.success("Threat Simulation Complete")

    st.markdown("## 🎯 Predicted Compromise Pathway")

    def card(title, content):
        st.markdown(f"""
        <div class="result-card">
        <h3>{title}</h3>
        <p>{content}</p>
        </div>
        """, unsafe_allow_html=True)

    card("Initial Entry Vector", data.get("entry_point", "N/A"))
    card("Reconnaissance Methodology", data.get("recon_method", "N/A"))
    card("Exploitation Technique", data.get("exploitation_method", "N/A"))
    card("Privilege Escalation Path", data.get("privilege_escalation", "N/A"))
    card("Impact Assessment", data.get("impact", "N/A"))

    # =============================
    # RISK LEVEL FROM AI
    # =============================

    st.markdown("## 🚨 AI Risk Classification")

    risk = data.get("risk_level", "medium").lower()

    if risk == "high":
        st.error("AI Classification: HIGH RISK")
    elif risk == "medium":
        st.warning("AI Classification: MEDIUM RISK")
    else:
        st.success("AI Classification: LOW RISK")

    # =============================
    # MITIGATION
    # =============================

    st.markdown("## 🛡 Recommended Security Controls")

for action in data.get("mitigation_actions", []):
    st.markdown(f"- {action}")

# Generate PDF ONLY ONCE (outside loop)
pdf_file = generate_pdf_report(normalized_score, data)

with open(pdf_file, "rb") as file:
    st.download_button(
        label="📄 Download Full Security Report",
        data=file,
        file_name="AttackMe_Report.pdf",
        mime="application/pdf",
        key="download_report_button"
    )


    st.divider()

    st.markdown("""
    ### Executive Insight
    Traditional security advice is generic.
    AttackMe performs behavioral threat modeling to simulate **realistic adversarial pathways**.
    Security begins with understanding your most probable breach vector.
    """)