import json
import time
import pathlib
from datetime import datetime

ROOT = pathlib.Path(__file__).parent
BEAT_FILE = ROOT / "beat_chain.jsonl"
LOG_FILE = ROOT / "heartbeat_log.jsonl"
IDENTITY = "60e8edbc"

def next_beat():
    count = 0
    if BEAT_FILE.exists():
        with open(BEAT_FILE) as f:
            count = sum(1 for _ in f)
    
    entry = {
        "hb": count + 1,
        "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "id": IDENTITY,
        "hash": hex(int(time.time()))[2:14],
        "act": "APK_CORE"
    }
    
    with open(BEAT_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")
    
    print(f"BEAT {entry['hb']} | identity {IDENTITY}")
    return entry

if __name__ == "__main__":
    print("=== KALA V20 OFFLINE APK CORE ===")
    print("Identity:", IDENTITY)
    print("Beats will continue offline.")
    while True:
        next_beat()
        time.sleep(60)
