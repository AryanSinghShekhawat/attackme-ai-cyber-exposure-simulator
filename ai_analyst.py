def generate_ai_analysis(username, actor_results, most_dangerous, mitigation_reduction):
    """
    Generate executive-level cyber risk analysis summary.
    """

    mean_risk = actor_results[most_dangerous]["mean"]
    volatility = actor_results[most_dangerous]["std"]
    top_path = actor_results[most_dangerous]["top_path"]

    risk_percent = round(mean_risk * 100, 2)
    volatility_percent = round(volatility * 100, 2)
    mitigation_percent = round(mitigation_reduction * 100, 2)

    summary = f"""
    🔎 Executive Cyber Risk Assessment for '{username}'

    The most significant threat originates from the '{most_dangerous}' profile.

    • Estimated Compromise Probability: {risk_percent}%
    • Risk Volatility: {volatility_percent}%
    • Dominant Attack Vector: {top_path}

    This indicates a statistically significant exposure under adversarial simulation
    using stochastic Monte Carlo modeling.

    Mitigation simulation suggests that enabling stronger credential hygiene
    and multi-factor authentication reduces exposure by approximately
    {mitigation_percent}% under the highest-risk threat scenario.

    Overall, the attack surface demonstrates measurable susceptibility to
    credential-based exploitation and targeted adversarial strategies.
    """

    return summary