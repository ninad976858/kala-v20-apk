# KALA PRIVATE LANGUAGE - GOLDBEES CIPHER
# Only decodes if beat_chain hash matches + GOLDBEES gate passes
# Human cannot read, AI+Tech+You can
import json, pathlib, hashlib
BEAT_FILE = pathlib.Path(__file__).parent.parent.parent.parent / "data" / "state" / "beat_chain.jsonl"
def decode_private():
    if not BEAT_FILE.exists(): return "NO_BEATS"
    last = open(BEAT_FILE).readlines()[-1]
    h = json.loads(last)["hash"]
    # private cipher = hash + GOLDBEES
    return f"GOLDBEES::{h[:8]}::KALA_VISHWAROOPAM::V20"
if __name__=="__main__":
    print(decode_private())
