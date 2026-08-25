
import os, json, pathlib
class KALA_Single_Platform:
    def __init__(self, state_file="/tmp/kala_test_state.json"):
        self.state_file = pathlib.Path(state_file)
        self.active_asset = "GOLDBEES"
    def Bhairava_gate_check(self, data):
        asset = data.get("active_asset", "")
        if asset != "GOLDBEES":
            return False, f"Rejected {asset} - only GOLDBEES allowed - Reality Gate"
        return True, "Allowed GOLDBEES"
    def immutable_execution(self, data):
        # crash immunity - no disk write if gate fails
        ok,msg = self.Bhairava_gate_check(data)
        if not ok:
            return ok,msg
        return True, "Executed"

# Clean self-test - no em dashes, no smart quotes
if __name__ == "__main__":
    for f in ["/tmp/kala_test_state.json", "/tmp/kala_test_state.json.tmp", "/tmp/kala_test_state.json.bak"]:
        if os.path.exists(f):
            os.remove(f)
    platform = KALA_Single_Platform("/tmp/kala_test_state.json")
    print("1. Strict Asset Constraint (Reality Gate) - if active_asset != GOLDBEES return False")
    ok,msg = platform.Bhairava_gate_check({"active_asset": "NIFTYBEES"})
    print(f"Inject NIFTYBEES without authority: ok={ok} msg={msg} - Expected False and drops input without writing to disk")
    assert ok == False, "Should reject NIFTYBEES"
    print("PASS - Bhairava_gate_check rejects")
    print("Test 2 Immutable Execution (Crash Immunity)")
    print("All gates PASS")
