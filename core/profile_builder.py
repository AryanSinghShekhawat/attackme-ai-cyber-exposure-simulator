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
    base_seed = hash_to_float(username)

    np.random.seed(int(base_seed * 1000))

    phishing_risk = normalize(np.random.normal(0.5 + base_seed * 0.2, 0.1))
    credential_reuse = normalize(np.random.normal(0.6, 0.15))
    public_exposure = normalize(np.random.normal(0.4 + base_seed * 0.3, 0.1))
    device_security = normalize(np.random.normal(0.5, 0.1))

    return {
        "phishing": phishing_risk,
        "credential_reuse": credential_reuse,
        "public_exposure": public_exposure,
        "device_security": device_security
    }