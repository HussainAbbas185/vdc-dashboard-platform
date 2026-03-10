
import os
import json
import datetime
import hashlib

AUDIT_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "audit_log.json"))
LEDGER_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "blockchain_ledger.json"))

def log_action(user, action, details, category="General", impact="Low"):
    """
    Logs a user action with categorization and Blockchain-Style Hashing.
    Ensures an Immutable Audit Trail for Enterprise Security.
    """
    timestamp = datetime.datetime.now().isoformat()
    
    # 1. Standard Audit Log Entry
    entry = {
        "timestamp": timestamp,
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

    # 2. Immutable Ledger (Blockchain Simulation)
    write_to_ledger(entry)

def write_to_ledger(entry):
    """
    Simulates a Blockchain Ledger by hashing the current block with the previous block's hash.
    """
    ledger = []
    if os.path.exists(LEDGER_FILE):
        try:
            with open(LEDGER_FILE, "r") as f:
                ledger = json.load(f)
        except:
            ledger = []

    prev_hash = "0" * 64 if not ledger else ledger[-1]["hash"]
    
    # Create the block
    block_data = f"{prev_hash}{json.dumps(entry, sort_keys=True)}"
    current_hash = hashlib.sha256(block_data.encode()).hexdigest()
    
    block = {
        "index": len(ledger),
        "timestamp": entry["timestamp"],
        "data": entry,
        "prev_hash": prev_hash,
        "hash": current_hash
    }
    
    ledger.append(block)
    
    with open(LEDGER_FILE, "w") as f:
        json.dump(ledger, f, indent=2)

def get_audit_trail():
    """Reads the standard audit log."""
    logs = []
    if os.path.exists(AUDIT_FILE):
        with open(AUDIT_FILE, "r") as f:
            for line in f:
                try:
                    logs.append(json.loads(line))
                except: continue
    return logs[::-1]

def get_blockchain_ledger():
    """Reads the immutable blockchain ledger."""
    if os.path.exists(LEDGER_FILE):
        with open(LEDGER_FILE, "r") as f:
            return json.load(f)[::-1]
    return []

def verify_ledger():
    """Verifies the integrity of the blockchain ledger."""
    if not os.path.exists(LEDGER_FILE):
        return True, "No ledger found."
    
    try:
        with open(LEDGER_FILE, "r") as f:
            ledger = json.load(f)
        
        for i in range(1, len(ledger)):
            prev_block = ledger[i-1]
            curr_block = ledger[i]
            
            # Verify Link
            if curr_block["prev_hash"] != prev_block["hash"]:
                return False, f"Integrity Breach at Block {i}: Link Mismatch."
            
            # Verify Hash
            block_data = f"{curr_block['prev_hash']}{json.dumps(curr_block['data'], sort_keys=True)}"
            expected_hash = hashlib.sha256(block_data.encode()).hexdigest()
            if curr_block["hash"] != expected_hash:
                return False, f"Integrity Breach at Block {i}: Hash Corruption."
                
        return True, f"Ledger Integrity Verified. {len(ledger)} Blocks secure."
    except Exception as e:
        return False, f"System Error during verification: {str(e)}"
