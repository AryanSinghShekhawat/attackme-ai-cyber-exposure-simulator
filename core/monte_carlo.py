# core/monte_carlo.py

import random
import numpy as np


def run_simulation(paths, actor_profile, iterations=1000):
    results = []
    path_success_counter = {key: 0 for key in paths.keys()}

    for _ in range(iterations):

        # Randomly choose attack path
        path_name = random.choice(list(paths.keys()))
        base_prob = paths[path_name]

        skill_variation = random.uniform(0.8, 1.2)

        outcome = base_prob
        outcome *= actor_profile["skill_multiplier"]
        outcome *= actor_profile["persistence"]
        outcome *= skill_variation

        final_prob = min(outcome, 1)
        results.append(final_prob)

        if final_prob > 0.5:
            path_success_counter[path_name] += 1

    mean_risk = np.mean(results)
    std_dev = np.std(results)

    most_frequent_path = max(path_success_counter, key=path_success_counter.get)

    return mean_risk, std_dev, results, most_frequent_path, path_success_counter