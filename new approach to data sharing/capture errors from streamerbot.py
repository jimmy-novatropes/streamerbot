import sys
import json
from datetime import datetime

def main():
    if len(sys.argv) < 2:
        print("❌ No arguments provided.")
        sys.exit(1)

    # Capture all arguments after the script name
    arguments = sys.argv[2:]

    # Join all arguments into one message (optional)
    full_message = " ".join(arguments)
    # Split the message
    parts = full_message.rsplit(" - ", 2)  # Split from the right, max 2 splits

    # Extract parts
    if len(parts) == 3:
        error_message = parts[0].strip()
        error_source = parts[1].strip()
        error_type = parts[2].strip()
    else:
        error_message = full_message
        error_source = "unknown"
        error_type = "unknown"

    log_entry = {
        # "arguments": arguments,         # List of all arguments separately
        # "full_message": full_message,    # One big string (optional)
        "error_message": error_message,
        "error_source": error_source,
        "error_type": error_type,
        "timestamp": datetime.utcnow().isoformat()
    }

    # Load or create error log file
    log_file = r"A:\Desktop\Novatropes Stream\error_log.json"
    try:
        with open(log_file, "r") as f:
            logs = json.load(f)
    except FileNotFoundError:
        logs = []

    logs.append(log_entry)
    with open(log_file, "w") as f:
        json.dump(logs, f, indent=2)

if __name__ == "__main__":
    main()
