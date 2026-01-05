
import os
import json
import datetime

AUDIT_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "audit_log.json"))

def log_action(user, action, details, category="General", impact="Low"):
    """
    Logs a user action with categorization for startup intelligence.
    """
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "user": user,
        "action": action,
        "details": details,
        "category": category,
        "impact": impact
    }
    
    # Ensure directory exists
    log_dir = os.path.dirname(AUDIT_FILE)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    
    with open(AUDIT_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")
        
def get_audit_trail():
    """Reads the audit log."""
    logs = []
    if os.path.exists(AUDIT_FILE):
        with open(AUDIT_FILE, "r") as f:
            for line in f:
                try:
                    logs.append(json.loads(line))
                except: continue
    return logs[::-1] # Newest first
