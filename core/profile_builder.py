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

    # Clean input
    username = username.strip().lower()

    # Seed from username (deterministic)
    base_seed = hash_to_float(username)
    np.random.seed(int(base_seed * 1000))

    # Core behavior-based signals
    phishing_risk = normalize(np.random.normal(0.5 + base_seed * 0.2, 0.1))
    credential_reuse = normalize(np.random.normal(0.6, 0.15))
    public_exposure = normalize(np.random.normal(0.4 + base_seed * 0.3, 0.1))
    device_security = normalize(np.random.normal(0.5, 0.1))

    # Heuristic adjustments based on username pattern

    # Short usernames = higher exposure
    if len(username) <= 5:
        public_exposure = normalize(public_exposure + 0.2)

    # Many numbers = weaker hygiene
    if sum(c.isdigit() for c in username) >= 3:
        credential_reuse = normalize(credential_reuse + 0.15)

    # Common influencer words
    if any(word in username for word in ["official", "real", "admin", "team"]):
        public_exposure = normalize(public_exposure + 0.25)

    return {
        "phishing_risk": phishing_risk,
        "credential_reuse": credential_reuse,
        "public_exposure": public_exposure,
        "device_security": device_security
    }