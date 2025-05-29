import json
import os

def update_vote_count(candidate):
    path = 'blockchain_data/vote_stats.json'
    stats = {}

    if os.path.exists(path):
        try:
            with open(path, 'r') as f:
                content = f.read().strip()
                if content:
                    stats = json.loads(content)
        except json.JSONDecodeError:
            stats = {}

    stats[candidate] = stats.get(candidate, 0) + 1

    with open(path, 'w') as f:
        json.dump(stats, f, indent=4)
