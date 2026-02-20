from openai import OpenAI
import streamlit as st

# Use Streamlit Secrets (NOT dotenv)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


def generate_attack_profile(user_summary):

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """
You are a cybersecurity threat modeling engine.

You MUST respond strictly in this exact JSON structure:

{
  "entry_point": "",
  "recon_method": "",
  "exploitation_method": "",
  "privilege_escalation": "",
  "impact": "",
  "risk_level": "",
  "mitigation_actions": []
}

Do not add explanations.
Do not change key names.
Do not use markdown.
Only valid JSON.
"""
            },
            {
                "role": "user",
                "content": f"Generate an attack path for this profile:\n{user_summary}"
            }
        ],
        temperature=0.2,
        max_tokens=700,
        response_format={"type": "json_object"}
    )

    return response.choices[0].message.content