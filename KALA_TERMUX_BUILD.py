import pathlib, sys, json, os
base = pathlib.Path(__file__).parent
beat = base/"data"/"state"/"beat_chain.jsonl"
state = base/"data"/"state"/"CURRENT_KALA_OPERATIONAL_STATE.json"
print("=== KALA V20 LEVEL 5 BUILDER ===")
print(f"BEAT: {beat.stat().st_size} bytes - {len(open(beat).readlines())} beats")
from app.core.engines.KALA_PRIVATE_LANG import decode_private
print(decode_private())
# Verify state exists
if state.exists():
    print(f"STATE: OK {state.stat().st_size} bytes")
else:
    print("STATE: MISSING!")
# Check buildozer.spec
spec = base/"buildozer.spec"
print(f"SPEC: {spec.read_text()[:400]}")
print("\n--- NEXT STEPS FOR APK ---")
print("1. pkg install -y python python-pip clang make pkg-config libffi openssl")
print("2. pip install --upgrade pip buildozer cython==0.29.36 kivy")
print("3. buildozer android debug")
print("\nBUILDER RECREATED - READY FOR LEVEL 5")
