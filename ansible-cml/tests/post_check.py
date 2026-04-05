from genie.testbed import load
from genie.utils.diff import Diff
import json

testbed = load("testbed/prod_testbed.yaml")

with open("pre_snapshot.json") as f:
    pre_snapshot = json.load(f)

issues_found = False

for device_name, device in testbed.devices.items():
    device.connect(log_stdout=False)

    post_state = {
        "interfaces": device.parse("show ip interface brief"),
        "vlans": device.parse("show vlan brief"),
    }

    device.disconnect()

    # Diff pre vs post
    diff = Diff(pre_snapshot[device_name], post_state)
    diff.findDiff()

    if diff.diffs:
        print(f"\n[{device_name}] Changes detected:")
        print(diff)
        issues_found = True
    else:
        print(f"[{device_name}] No unexpected changes. ✓")

if issues_found:
    exit(1)  # Fails the pipeline stage