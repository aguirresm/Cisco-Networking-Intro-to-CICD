from genie.testbed import load
import json

# Load the testbed
testbed = load("testbed/lab_testbed.yaml")

snapshot = {}

for device_name, device in testbed.devices.items():
    device.connect(log_stdout=False)

    # Capture structured state
    snapshot[device_name] = {
        "interfaces": device.parse("show ip interface brief"),
        "vlans": device.parse("show vlan brief"),
    }

    device.disconnect()

# Save snapshot to file (passed as artifact to post-check)
with open("pre_snapshot.json", "w") as f:
    json.dump(snapshot, f, indent=2)

print("Pre-check complete. Snapshot saved.")