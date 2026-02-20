# core/attack_graph.py

def generate_attack_paths(profile):
    paths = {
        "Phishing → Credential Theft → Account Takeover":
            profile["phishing"] * profile["credential_reuse"],

        "Public Info → Social Engineering → Fraud":
            profile["public_exposure"] * profile["phishing"],

        "Device Exploit → Credential Dump":
            profile["device_security"] * profile["credential_reuse"],

        "Combined Multi-Vector Attack":
            profile["phishing"] *
            profile["credential_reuse"] *
            profile["public_exposure"]
    }

    return paths