import pathlib
ROOT=pathlib.Path.home()/"kala"
DAILY=ROOT/"data"/"daily"
STATE=ROOT/"data"/"state"/"beat_chain.jsonl"
LAYER2=ROOT/"KALA_LAYER2_DATA"

def attention():
    beats=STATE.read_text().splitlines()[-5:]
    print(f"ATTENTION: last 5 beats from {len(open(STATE).readlines())} total")
    for b in beats:
        import json; j=json.loads(b); print(f"  BC{j['beat']} {j['ts_ist'][11:19]} ws {j['detail'][:30]}")
    daily=list(DAILY.glob("*_daily.csv"))
    l2=list(LAYER2.glob("*.csv")) if LAYER2.exists() else []
    print(f"CACHE: daily {len(daily)} files {sum(f.stat().st_size for f in daily)//1024}KB")
    print(f"INDEX: KALA_LAYER2_DATA {len(l2)} files {sum(f.stat().st_size for f in l2)//1024}KB real={sum(1 for f in l2 if f.stat().st_size>10000)} fake={sum(1 for f in l2 if f.stat().st_size<5000)}")
    for f in sorted(l2):
        print(f"  {f.name} {f.stat().st_size//1024}KB")

if __name__=="__main__":
    attention()
