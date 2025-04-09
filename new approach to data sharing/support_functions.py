import json
import os
from datetime import datetime

def save_or_extend_json(data, file_path: str):
    # Normalize single dict entry into a wrapper with timestamp
    if not isinstance(data, dict):
        raise ValueError("Data must be a dictionary.")

    # Wrap if it's a single flat dict (e.g. {"status": "ok"})
    if all(not isinstance(v, dict) for v in data.values()):
        data = {
            f"entry_{datetime.now().strftime('%Y%m%d%H%M%S')}": {
                **data,
                "timestamp": datetime.now().isoformat()
            }
        }
    else:
        for key, value in data.items():
            if isinstance(value, dict):
                value["timestamp"] = datetime.now().isoformat()
            else:
                data[key] = {"value": value, "timestamp": datetime.now().isoformat()}

    # Merge with existing file
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                existing = json.load(f)
            if isinstance(existing, dict):
                existing.update(data)
            else:
                print("Warning: existing data is not a dictionary. Overwriting.")
                existing = data
        except json.JSONDecodeError:
            print("Warning: invalid JSON. Overwriting.")
            existing = data
    else:
        existing = data

    with open(file_path, 'w') as f:
        json.dump(existing, f, indent=4)
