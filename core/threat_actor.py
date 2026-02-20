# core/threat_actor.py

THREAT_ACTORS = {
    "Script Kiddie": {
        "skill_multiplier": 0.8,
        "persistence": 0.6
    },
    "Financial Criminal": {
        "skill_multiplier": 1.2,
        "persistence": 1.0
    },
    "Corporate Spy": {
        "skill_multiplier": 1.4,
        "persistence": 1.3
    }
}

def get_actor_profile(actor_name):
    return THREAT_ACTORS.get(actor_name)