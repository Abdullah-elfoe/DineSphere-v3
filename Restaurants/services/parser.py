def get_user_logs(username):
    from .mongo import logs_collection

    logs = logs_collection.find(
        {"event": username}
    ).sort("timestamp", -1)

    return list(logs)

def format_logs_to_text(logs):
    lines = []

    for log in logs:
        timestamp = log.get("timestamp")
        data = log.get("data", {})

        lines.append("=" * 50)
        lines.append(f"Time      : {timestamp}")
        
        for key, value in data.items():
            lines.append(f"{key.capitalize():10}: {value}")
        
        lines.append("")  # spacing

    return "\n".join(lines)