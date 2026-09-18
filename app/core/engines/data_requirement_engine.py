import pathlib
ROOT=pathlib.Path.home() / "kala"
DAILY=ROOT/"data"/"daily"
INBOX=ROOT/"data"/"inbox"
LAYER2_CANDIDATES=[ROOT/"KALA_LAYER2_DATA", ROOT/"data"/"layer2", ROOT/"data"/"market_data", ROOT/"data"/"market_data_registry"]

def scan(p):
    if not p.exists(): return []
    return [f for f in p.glob("*.csv") if f.stat().st_size > 100]

print(f"REQUIRED daily: {len(scan(DAILY))} files {sum(f.stat().st_size for f in scan(DAILY))//1024}KB")
print(f"MINIMUM inbox: {len(scan(INBOX))} files {sum(f.stat().st_size for f in scan(INBOX))//1024}KB")
for cand in LAYER2_CANDIDATES:
    files=scan(cand)
    if files:
        print(f"INDEX {cand.name}: {len(files)} files {sum(f.stat().st_size for f in files)//1024}KB")
        for f in sorted(files)[:5]:
            print(f"  {f.name} {f.stat().st_size//1024}KB {sum(1 for _ in open(f))} lines")
    else:
        print(f"INDEX {cand.name}: 0 files")

import pathlib as pl
arch=pl.Path.home()/"kala_archive"
print(f"ARCHIVE: {arch} total")
