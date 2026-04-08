#!/usr/bin/env python3
"""Baseline platform stability sample before Ansible deploy (CPU, memory, ping, optional routes)."""

import json
import sys

from stability_lib import (
    collect_device_sample,
    load_checks_config,
    load_testbed,
    precheck_device_ok,
)


def main() -> None:
    cfg = load_checks_config()
    testbed = load_testbed()
    snapshot = {}
    failed = False

    for device_name, device in testbed.devices.items():
        device.connect(log_stdout=False)
        try:
            sample = collect_device_sample(device, cfg)
            snapshot[device_name] = sample
            ok, issues = precheck_device_ok(sample)
            if not ok:
                failed = True
                print(f"\n[{device_name}] Pre-check failed:")
                for msg in issues:
                    print(f"  - {msg}")
            else:
                print(
                    f"[{device_name}] Pre-check OK — baseline sampled "
                    "(CPU / memory / ping / routes)."
                )
        finally:
            device.disconnect()

    with open("pre_snapshot.json", "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2)

    print("\nPre-check complete. Baseline written to pre_snapshot.json.")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
