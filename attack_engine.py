from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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