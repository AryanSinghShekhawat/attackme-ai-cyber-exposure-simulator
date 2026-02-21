# core/profile_builder.py

import numpy as np
import hashlib


def normalize(value):
    return max(0, min(1, value))


def hash_to_float(text):
    hash_val = hashlib.md5(text.encode()).hexdigest()
    int_val = int(hash_val[:8], 16)
    return (int_val % 1000) / 1000.0


def build_profile(username):

    # -------------------------
    # DOMAIN DETECTION
    # -------------------------
    if "@" in username:
        domain = username.split("@")[1].lower()
    else:
        domain = None

    # -------------------------
    # DETERMINISTIC RANDOM SEED
    # -------------------------
    base_seed = hash_to_float(username)
    np.random.seed(int(base_seed * 1000))

    # -------------------------
    # BASE BEHAVIORAL PROFILE
    # -------------------------
    phishing_risk = normalize(np.random.normal(0.5 + base_seed * 0.2, 0.1))
    credential_reuse = normalize(np.random.normal(0.6, 0.15))
    public_exposure = normalize(np.random.normal(0.4 + base_seed * 0.3, 0.1))
    device_security = normalize(np.random.normal(0.5, 0.1))

    # -------------------------
    # DOMAIN INTELLIGENCE LAYER
    # -------------------------
    if domain:

        # Free providers → more phishing
        if domain in ["gmail.com", "yahoo.com", "outlook.com"]:
            phishing_risk += 0.15
            public_exposure += 0.1

        # Corporate domains
        elif domain.endswith(".com"):
            public_exposure += 0.2
            credential_reuse -= 0.1

        # Educational domains
        elif domain.endswith(".edu"):
            phishing_risk += 0.25

        # Government domains
        elif domain.endswith(".gov"):
            public_exposure += 0.3
            credential_reuse -= 0.2

        # Finance / high-value keywords
        if any(keyword in domain for keyword in ["bank", "finance", "capital"]):
            public_exposure += 0.3

    # -------------------------
    # FINAL NORMALIZATION
    # -------------------------
    phishing_risk = normalize(phishing_risk)
    credential_reuse = normalize(credential_reuse)
    public_exposure = normalize(public_exposure)
    device_security = normalize(device_security)

    return {
        "phishing_risk": phishing_risk,
        "credential_reuse": credential_reuse,
        "public_exposure": public_exposure,
        "device_security": device_security
    }