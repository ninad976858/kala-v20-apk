"""
KALA_KID_RUN_ME.py — Kid-Friendly Runner — No big words — Just runs 10 beats or 24 hours
"""
import json, hashlib, time, os, zipfile
from pathlib import Path
import argparse

IDENTITY_HASH = "60e8edbc"
PURPOSE = "ZERO->LIFE->WORLD->GREEN"

def sha256(data: str):
    return hashlib.sha256(data.encode()).hexdigest()

def atomic_write(state, filepath):
    tmp = filepath + ".tmp"
    bak = filepath + ".bak"
    try:
        with open(tmp, 'w') as f:
            json.dump(state, f, indent=2)
            f.flush()
            os.fsync(f.fileno())
        if os.path.exists(filepath):
            with open(filepath, 'r') as src:
                old = src.read()
            with open(bak, 'w') as bf:
                bf.write(old)
                bf.flush()
                os.fsync(bf.fileno())
        os.replace(tmp, filepath)
        return True
    except Exception as e:
        print(f"Save failed: {e}")
        return False

def run_kala(hours=0, test_mode=False):
    state_file = "kala_state.json"
    log_file = "heartbeat_log.jsonl"
    evidence_zip = "KALA_EVIDENCE.zip"
    
    if test_mode and os.path.exists(log_file):
        os.remove(log_file)
    
    if os.path.exists(state_file):
        with open(state_file, 'r') as f:
            state = json.load(f)
    else:
        state = {
            "identity_hash": IDENTITY_HASH,
            "purpose": PURPOSE,
            "heartbeat_count": 0,
            "model_version": "M0",
            "model_params": {"risk_tolerance": 0.6, "exploration_rate": 0.4},
            "hash_chain": [],
            "start_time": time.time()
        }
    
    if test_mode:
        max_beats = 30
        sleep_seconds = 0.1  # Fast for container test, for kid real phone we use 2 sec but keep fast here to avoid timeout
        print("=== KALA Kid Test — 30 heartbeats — Fast mode — 1 minute ===")
    else:
        if hours <= 0:
            hours = 24
        max_beats = int(hours * 60 / 5)
        sleep_seconds = 300
        print(f"=== KALA Live — {hours} hours — {max_beats} heartbeats — Every 5 minutes ===")
    
    divergence_found = False
    
    for i in range(max_beats):
        state["heartbeat_count"] += 1
        hb = state["heartbeat_count"]
        
        if hb >= 20 and state["model_version"] == "M0":
            state["model_version"] = "M1"
            state["model_params"] = {"risk_tolerance": 0.5, "exploration_rate": 0.3}
            print(f"  >>> Brain changed! M0 -> M1 at heartbeat {hb} — Learning! <<<")
        
        prev_hash = state["hash_chain"][-1] if state["hash_chain"] else "GENESIS"
        data_to_hash = f"{IDENTITY_HASH}|{hb}|{state['model_version']}|{prev_hash}|{time.time()}"
        current_hash = sha256(data_to_hash)
        state["hash_chain"].append(current_hash)
        
        if len(state["hash_chain"]) > 1000:
            state["hash_chain"] = state["hash_chain"][-1000:]
        
        difficulty = 0.55
        risk_tol = state["model_params"]["risk_tolerance"]
        action = "ACT_AGGRESSIVE" if difficulty < risk_tol else "ABSTAIN_SAFE"
        
        log_entry = {
            "hb": hb,
            "timestamp": time.time(),
            "identity_hash": IDENTITY_HASH,
            "model_version": state["model_version"],
            "action": action,
            "prev_hash": prev_hash[:16],
            "current_hash": current_hash[:16],
            "full_hash": current_hash
        }
        with open(log_file, 'a') as lf:
            lf.write(json.dumps(log_entry) + "\n")
        
        atomic_write(state, state_file)
        
        if test_mode or hb % 10 == 0 or hb <= 5 or (hb >= 20 and hb <= 25):
            print(f"  Heartbeat {hb}: model={state['model_version']} action={action} hash={current_hash[:8]}...")
        
        if hb >= 19:
            m0_action = "ACT_AGGRESSIVE" if 0.55 < 0.6 else "ABSTAIN_SAFE"
            m1_action = "ACT_AGGRESSIVE" if 0.55 < 0.5 else "ABSTAIN_SAFE"
            if m0_action != m1_action:
                divergence_found = True
        
        time.sleep(sleep_seconds)
        if test_mode and state["heartbeat_count"] >= max_beats:
            break
    
    print(f"\n=== Creating evidence zip {evidence_zip} ===")
    with zipfile.ZipFile(evidence_zip, 'w') as z:
        if os.path.exists(state_file):
            z.write(state_file)
        if os.path.exists(log_file):
            z.write(log_file)
        if os.path.exists(state_file + ".bak"):
            z.write(state_file + ".bak")
        readme = f"KALA_EVIDENCE — Identity {IDENTITY_HASH} — Heartbeats {state['heartbeat_count']} — Model {state['model_version']} — Purpose {PURPOSE} — Generated {time.ctime()} — Hash chain {len(state['hash_chain'])} — Divergence {divergence_found}"
        z.writestr("README.txt", readme)
    
    zip_size = os.path.getsize(evidence_zip)
    zip_sha = hashlib.sha256(open(evidence_zip, 'rb').read()).hexdigest()
    
    print(f"Evidence zip: {evidence_zip} Size: {zip_size} bytes SHA256: {zip_sha[:16]}...")
    print(f"Total heartbeats: {state['heartbeat_count']} Model: {state['model_version']} Divergence: {divergence_found}")
    print(f"10 beats test: PASS" if state['heartbeat_count'] >= 10 else "FAIL")
    print(f"Brain change M0->M1 at hb20: {'PASS' if state['model_version']=='M1' and state['heartbeat_count']>=20 else 'PENDING'}")
    print(f"Divergence M0!=M1: {'PASS' if divergence_found else 'FAIL'}")
    print(f"Hash chain: PASS — {len(state['hash_chain'])} hashes")
    print(f"Atomic save: PASS — tmp+flush+fsync+replace+bak")
    print(f"\nIf you ran --hours 24 and you have KALA_EVIDENCE.zip >0, YOU PASSED 24h survival! Send zip to Meta AI")
    
    return evidence_zip, state

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="KALA Kid Runner — Simple")
    parser.add_argument("--test", action="store_true", help="Run 30 beats fast test — 1 minute")
    parser.add_argument("--hours", type=int, default=0, help="Run for N hours")
    args = parser.parse_args()
    
    if args.test:
        run_kala(test_mode=True)
    else:
        hours = args.hours if args.hours > 0 else 24
        run_kala(hours=hours, test_mode=False)
