#!/usr/bin/env python3
"""Post-deploy stability: compare CPU/memory/ping/routes to baseline and threshold ceilings."""

import json
import sys

from stability_lib import (
    collect_device_sample,
    compare_samples,
    load_checks_config,
    load_testbed,
    threshold_defaults,
)


def main() -> None:
    cfg = load_checks_config()
    thresholds = threshold_defaults(cfg)
    testbed = load_testbed()

    with open("pre_snapshot.json", encoding="utf-8") as f:
        pre_snapshot = json.load(f)

    issues_found = False

    for device_name, device in testbed.devices.items():
        device.connect(log_stdout=False)
        try:
            post_sample = collect_device_sample(device, cfg)
            pre_sample = pre_snapshot.get(device_name)
            if pre_sample is None:
                print(
                    f"[{device_name}] No pre-snapshot baseline; skipping stability compare."
                )
                continue

            issues = compare_samples(pre_sample, post_sample, thresholds)
            if issues:
                issues_found = True
                print(f"\n[{device_name}] Post-check stability issues:")
                for msg in issues:
                    print(f"  - {msg}")
            else:
                print(
                    f"[{device_name}] Post-check OK — within stability thresholds. ✓"
                )
        finally:
            device.disconnect()

    if issues_found:
        sys.exit(1)


if __name__ == "__main__":
    main()
