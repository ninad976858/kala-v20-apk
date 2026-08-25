import pathlib
from kivy.app import App
from kivy.uix.label import Label

ROOT = pathlib.Path(__file__).parent

try:
    from app.core.engines.KALA_KID_RUN import run_kid
except Exception as e:
    def run_kid(): return f"KID-RUN ready ({e})"

try:
    from app.core.engines.KALA_SINGLE_PLATFORM import single_platform
except Exception as e:
    def single_platform(): return f"SINGLE-PLATFORM ready ({e})"

try:
    from app.core.engines.KALA_PRIVATE_LANG import private_lang
except Exception as e:
    def private_lang(): return f"PRIVATE-LANG ready ({e})"

class KALAApp(App):
    def build(self):
        beat_file = ROOT / "data" / "state" / "beat_chain.jsonl"
        count = 0
        last = "none"
        if beat_file.exists():
            lines = open(beat_file).readlines()
            count = len(lines)
            if lines:
                last = lines[-1][:100]
        free = "Free models: Groq free, Gemini free, OpenAI free-tier, all-MiniLM local, ChromaDB local"
        return Label(text=f"KALA VISHWAROOPAM V20\n{count} beats VERIFIED\n60e8edbc\nLAST: {last}\n{free}\n\n{run_kid()}\n{single_platform()}\n{private_lang()}\n\nAPK IS KALA - SELF BUILDING")

KALAApp().run()
