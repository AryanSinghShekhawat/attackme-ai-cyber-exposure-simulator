import streamlit as st
import json
from attack_engine import generate_attack_profile
import pandas as pd
import matplotlib.pyplot as plt
from report_generator import generate_pdf_report

# =============================
# SESSION STATE INIT
# =============================

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
# ENTERPRISE UI STYLE (FIXED LABEL COLOR)
# =============================

st.markdown("""
<style>

/* Center container */
.center-button-container {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 40px;
    margin-bottom: 40px;
}

/* BIG Responsive Button */
.center-button-container button {
    width: 80%;
    max-width: 600px;
    height: 80px;
    font-size: 26px;
    font-weight: bold;
    border-radius: 15px;
    background: linear-gradient(135deg, #ff416c, #ff4b2b);
    color: white;
    border: none;
    transition: 0.3s ease-in-out;
}

div.stButton > button:hover {
    transform: scale(1.05);
    background: linear-gradient(135deg, #ff4b2b, #ff416c);
}

/* Fullscreen Loading Overlay */
.loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    backdrop-filter: blur(8px);
    background: rgba(0, 0, 0, 0.6);
    z-index: 9999;
    display: flex;
    justify-content: center;
    align-items: center;
}

/* Spinner Animation */
.loader {
    border: 8px solid #f3f3f3;
    border-top: 8px solid #ff4b2b;
    border-radius: 50%;
    width: 80px;
    height: 80px;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

</style>
""", unsafe_allow_html=True)

# =============================
# HEADER
# =============================

st.title("🛡️ AttackMe – AI Cyber Exposure Simulator")
st.markdown("""
A behavioral threat modeling simulation.  
Predicting your most probable compromise pathway.
""")

st.divider()

# =============================
# INPUT SECTION (WITH SELECT DEFAULT)
# =============================

col1, col2 = st.columns(2)

with col1:
    reuse_passwords = st.selectbox("Password Reuse Across Platforms", ["Select","Yes", "No"])
    public_social = st.selectbox("Public Social Media Presence", ["Select","Yes", "No"])
    two_fa = st.selectbox("Multi-Factor Authentication Enabled", ["Select","Yes", "No"])
    public_wifi = st.selectbox("Frequent Public WiFi Usage", ["Select","Yes", "No"])

with col2:
    click_links = st.selectbox("Interaction with Unknown Links", ["Select","Often", "Sometimes", "Never"])
    share_info = st.selectbox("Sharing Personal Data Online", ["Select","Yes", "No"])
    cracked_software = st.selectbox("Installation of Unverified/Cracked Software", ["Select","Yes", "No"])

# =============================
# SCORING ENGINE
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

MAX_SCORE = sum(risk_weights.values())
normalized_score = round((score / MAX_SCORE) * 100) if MAX_SCORE else 0

# =============================
# EXECUTIVE SUMMARY
# =============================

st.markdown("## 🧾 Executive Risk Overview")

if normalized_score >= 75:
    summary = "High probability of targeted compromise. Immediate mitigation required."
    badge = "badge-high"
elif normalized_score >= 50:
    summary = "Multiple exploitable vectors detected. Risk reduction recommended."
    badge = "badge-medium"
else:
    summary = "Moderate exposure. Strategic hardening advised."
    badge = "badge-low"

st.markdown(f"""
<div class="exec-box">
<h3>Exposure Score: {normalized_score}%</h3>
<p>{summary}</p>
<span class="badge {badge}">{summary.split('.')[0]}</span>
</div>
""", unsafe_allow_html=True)

# =============================
# MAIN DASHBOARD
# =============================

col_left, col_right = st.columns([2,2])

with col_left:
    st.markdown("## 📈 Attack Probability Model")

    # Normalize vectors so max = 100
    attack_vectors = {
        "Phishing": normalized_score,
        "Credential Stuffing": normalized_score,
        "Malware Injection": normalized_score,
        "Session Hijacking": normalized_score,
        "Social Engineering": normalized_score
    }

    df = pd.DataFrame({
        "Attack Vector": list(attack_vectors.keys()),
        "Probability (%)": list(attack_vectors.values())
    })

    fig, ax = plt.subplots(figsize=(6,4))
    ax.bar(df["Attack Vector"], df["Probability (%)"])
    ax.set_ylim(0,100)
    ax.set_ylabel("Probability (%)")
    ax.tick_params(axis='x', rotation=30)
    plt.tight_layout()

    st.pyplot(fig)

with col_right:
    st.markdown("## 📊 Exposure Dashboard")
    st.progress(normalized_score)

    st.markdown(f"""
    <div class="metric-box">
    <h2>{normalized_score}%</h2>
    <p>Behavioral Exposure</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# =============================
# RUN SIMULATION
# =============================

# Centered Big Button
st.markdown('<div class="center-button-container">', unsafe_allow_html=True)

run_simulation = st.button("🚀 Run Threat Simulation")

st.markdown('</div>', unsafe_allow_html=True)

if run_simulation:
    # Show loading overlay
    loading_placeholder = st.empty()
    loading_placeholder.markdown("""
        <div class="loading-overlay">
            <div class="loader"></div>
        </div>
    """, unsafe_allow_html=True)

    # Simulate processing (replace with your real function)
    import time
    time.sleep(3)

    # Clear loading screen
    loading_placeholder.empty()

    # Now run your actual simulation logic here
    # CALL YOUR EXISTING FUNCTION BELOW
    # result = run_attack_simulation(...)
    # st.write(result)

    st.session_state.risk_history.append(normalized_score)

    summary_input = f"""
    Password reuse: {reuse_passwords}
    Public social exposure: {public_social}
    MFA enabled: {two_fa}
    Public WiFi usage: {public_wifi}
    Unknown link interaction: {click_links}
    Sharing personal info: {share_info}
    Cracked software usage: {cracked_software}
    """

    with st.spinner("Executing AI threat modeling..."):
        try:
            result = generate_attack_profile(summary_input)
            data = json.loads(result)
        except Exception as e:
            st.error(f"Simulation failed: {e}")
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

    card("Initial Entry Vector", data.get("entry_point","N/A"))
    card("Reconnaissance Methodology", data.get("recon_method","N/A"))
    card("Exploitation Technique", data.get("exploitation_method","N/A"))
    card("Privilege Escalation", data.get("privilege_escalation","N/A"))
    card("Impact Assessment", data.get("impact","N/A"))

    # =============================
    # MITIGATION SECTION (ADDED)
    # =============================

    st.markdown("## 🛡 Recommended Security Controls")

    mitigations = data.get("mitigation_actions") or []

    if isinstance(mitigations, list) and mitigations:
        for action in mitigations:
            st.markdown(f"""
            <div class="result-card">
                {action}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No mitigation data returned from AI.")

# =============================
    # RISK TREND CHART
    # =============================

    st.markdown("## 📊 Risk Trend Over Time")

    trend_df = pd.DataFrame({
        "Simulation": list(range(1, len(st.session_state.risk_history)+1)),
        "Risk Score": st.session_state.risk_history
    })

    fig2, ax2 = plt.subplots(figsize=(6,4))
    ax2.plot(trend_df["Simulation"], trend_df["Risk Score"])
    ax2.set_xlabel("Simulation Run")
    ax2.set_ylabel("Risk Score (%)")
    plt.tight_layout()

    st.pyplot(fig2, use_container_width=False)

    # =============================
    # PDF REPORT
    # =============================

    try:
        pdf_file = generate_pdf_report(normalized_score, data)
        with open(pdf_file, "rb") as file:
            st.download_button(
                "📄 Download Full Security Report",
                file,
                "AttackMe_Report.pdf",
                "application/pdf"
            )
    except:
        st.error("PDF generation failed.")