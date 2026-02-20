import streamlit as st
import joblib
import matplotlib.pyplot as plt
from core.profile_builder import build_profile
from core.attack_graph import generate_attack_paths
from core.monte_carlo import run_simulation
from core.threat_actor import THREAT_ACTORS

model = joblib.load("risk_model.pkl")

st.set_page_config(page_title="AttackMe AI", layout="wide")

st.title("AttackMe AI – Adaptive Cyber Exposure Emulator")


# -------------------------
# USER INPUT
# -------------------------
username = st.text_input("Enter Gmail or Username")
enable_mfa = st.checkbox("Enable MFA Protection")

run_clicked = st.button("Run Simulation")


# -------------------------
# RISK CLASSIFIER
# -------------------------
def classify_risk(score):
    if score < 0.25:
        return "Low", "🟢"
    elif score < 0.5:
        return "Moderate", "🟡"
    elif score < 0.75:
        return "High", "🔴"
    else:
        return "Critical", "🔥"


# -------------------------
# MITIGATION SIMULATION
# -------------------------
def simulate_mitigation(profile, actor_profile):

    # Baseline simulation
    base_paths = generate_attack_paths(profile)
    baseline_mean, _, _, _, _ = run_simulation(base_paths, actor_profile)

    # Improved profile
    improved_profile = profile.copy()

    if "credential_reuse" in improved_profile:
        improved_profile["credential_reuse"] *= 0.5

    if "phishing_risk" in improved_profile:
        improved_profile["phishing_risk"] *= 0.6

    improved_paths = generate_attack_paths(improved_profile)
    improved_mean, _, _, _, _ = run_simulation(improved_paths, actor_profile)

    reduction = baseline_mean - improved_mean

    return baseline_mean, improved_mean, reduction


# -------------------------
# MAIN SIMULATION
# -------------------------
if run_clicked:

    if not username:
        st.warning("Please enter a username or Gmail.")
        st.stop()

    # Build profile
    profile = build_profile(username)

    # Apply MFA simulation
    if enable_mfa and "credential_reuse" in profile:
        profile["credential_reuse"] *= 0.6

    # ML Prediction
    features = [[
        profile["credential_reuse"],
        profile.get("phishing_risk", 0),
        profile.get("public_exposure", 0)
    ]]

    predicted_risk = model.predict(features)[0]

    st.subheader("🤖 AI Model Risk Prediction")
    st.write(f"Predicted Risk Score (ML): {predicted_risk:.2f}")

    # Generate attack paths
    paths = generate_attack_paths(profile)

    actor_results = {}

    # Run simulation for all actors
    for actor_name, actor_profile in THREAT_ACTORS.items():

        mean_risk, std_dev, results, most_path, path_counter = run_simulation(
            paths, actor_profile
        )

        actor_results[actor_name] = {
            "mean": mean_risk,
            "std": std_dev,
            "top_path": most_path,
            "distribution": results
        }

    # -------------------------
    # Actor Comparison
    # -------------------------
    st.subheader("Threat Actor Comparison")

    comparison_data = {
        actor: actor_results[actor]["mean"]
        for actor in actor_results
    }

    st.bar_chart(comparison_data)

    # -------------------------
    # Detailed Results
    # -------------------------
    for actor_name in actor_results:

        st.markdown(f"### {actor_name}")

        mean_score = actor_results[actor_name]['mean']
        risk_level, icon = classify_risk(mean_score)

        st.write(f"Compromise Probability: {mean_score:.2f}")
        st.write(f"Risk Classification: {icon} {risk_level}")
        st.write(f"Risk Volatility: {actor_results[actor_name]['std']:.2f}")
        st.write(f"Most Frequent Attack Path: {actor_results[actor_name]['top_path']}")

    # -------------------------
    # Most Dangerous Actor
    # -------------------------
    most_dangerous = max(actor_results, key=lambda x: actor_results[x]["mean"])

    st.subheader("🚨 Most Dangerous Threat Actor")
    st.error(f"{most_dangerous} poses the highest compromise probability.")

    # -------------------------
    # Intelligent Mitigation
    # -------------------------
    st.subheader("🛡 Intelligent Defense Recommendation")

    baseline_mean, improved_mean, reduction = simulate_mitigation(
        profile,
        THREAT_ACTORS[most_dangerous]
    )

    improvement_percent = (reduction / baseline_mean) * 100 if baseline_mean > 0 else 0

    st.write(f"Baseline Risk: {baseline_mean:.2f}")
    st.write(f"Post-Mitigation Risk: {improved_mean:.2f}")
    st.write(f"Projected Risk Reduction: {improvement_percent:.1f}%")

    if improvement_percent > 20:
        st.success("High-impact mitigation detected. Strengthening credential hygiene significantly lowers exposure.")
    elif improvement_percent > 10:
        st.info("Moderate mitigation impact detected.")
    else:
        st.warning("Limited mitigation impact. Advanced controls recommended.")

    # -------------------------
    # Risk Distribution Graph
    # -------------------------
    st.subheader("Risk Distribution (Monte Carlo Simulation)")

    fig, ax = plt.subplots()
    ax.hist(actor_results[most_dangerous]["distribution"], bins=30)
    ax.set_xlabel("Compromise Probability")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)