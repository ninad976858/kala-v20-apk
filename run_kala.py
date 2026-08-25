#!/usr/bin/env python3
import json, datetime, pathlib, time, hashlib

ROOT = pathlib.Path.home() / "kala"
STATE = ROOT / "data" / "state"
BEAT_FILE = STATE / "beat_chain.jsonl"
LOG_FILE = ROOT / "heartbeat_log.jsonl"
EVIDENCE = ROOT / "data" / "evidence" / "live_evidence.jsonl"
IDENTITY = "60e8edbc"

STATE.mkdir(parents=True, exist_ok=True)
EVIDENCE.parent.mkdir(parents=True, exist_ok=True)

def get_last_beat():
    if not BEAT_FILE.exists():
        return 0, "b7acf443b62fdaba"
    last = None
    with open(BEAT_FILE) as f:
        for line in f:
            if line.strip():
                last = json.loads(line)
    if last:
        return last.get("beat", 0), last.get("hash", "b7acf443b62fdaba")
    return 0, "b7acf443b62fdaba"

def write_beat():
    count, prev_hash = get_last_beat()
    new_beat = count + 1
    new_hash = hashlib.sha256(f"{new_beat}{prev_hash}{IDENTITY}".encode()).hexdigest()[:16]
    
    entry = {
        "beat": new_beat,
        "prev_hash": prev_hash,
        "hash": new_hash,
        "identity_hash": IDENTITY,
        "timestamp": datetime.datetime.now().isoformat(),
        "real_revenue": 0,
        "status": "LIVE_TERMUX"
    }
    
    # Append to beat chain
    with open(BEAT_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")
    
    # Append to simple log
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")
    
    # Append evidence
    with open(EVIDENCE, "a") as f:
        f.write(json.dumps({
            "type": "heartbeat",
            "beat": new_beat,
            "identity": IDENTITY,
            "time": entry["timestamp"]
        }) + "\n")
    
    print(f"[{entry['timestamp']}] BEAT {new_beat} | identity {IDENTITY} | hash {new_hash}")
    return entry

print("=== KALA V20 OFFLINE TERMUX CORE ===")
print("Identity:", IDENTITY)
print("No network needed. Running continuously.")
print("Press Ctrl+C to stop later.\n")

while True:
    try:
        write_beat()
        time.sleep(300)   # every 5 minutes (change to 60 if you want faster)
    except KeyboardInterrupt:
        print("\nStopped by you. Evidence is saved.")
        break
    except Exception as e:
        print("Error:", e)
        time.sleep(30)
