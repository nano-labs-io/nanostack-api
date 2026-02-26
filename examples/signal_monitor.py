#!/usr/bin/env python3
"""Monitor NanoStack signal atoms in real-time.

No dependencies required — uses only Python stdlib.

Usage:
    python3 signal_monitor.py
    python3 signal_monitor.py --pairs    # Show available trading pairs first
"""

import urllib.request
import json
import time
import sys

BASE = "https://api.nano-labs.io"

ECOSYSTEMS = {0: "evm", 1: "solana", 2: "cosmos", 3: "utxo", 4: "xrpl", 5: "move"}


def fetch(path):
    url = f"{BASE}{path}"
    req = urllib.request.Request(url, headers={"User-Agent": "nanostack-example/1.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())


def show_pairs():
    data = fetch("/v1/bots/pairs")
    pairs = data.get("pairs", [])
    print(f"\n{'ID':>4}  {'Base':>8} / {'Quote':<8}  {'Ecosystem':<10}  {'Chain'}")
    print("-" * 60)
    for p in pairs:
        eco = ECOSYSTEMS.get(p.get("ecosystem", 0), "?")
        print(f"{p['id']:>4}  {p['base']:>8} / {p['quote']:<8}  {eco:<10}  {p.get('chain_id', '?')}")


def monitor(interval=5, count=10):
    last_seq = 0
    print(f"\nMonitoring signal atoms (every {interval}s)...\n")
    print(f"{'Seq':>10}  {'Eco':<8}  {'Pair':>4}  {'Dev bps':>8}  {'Entropy':>10}  {'Venue':<12}  {'Price'}")
    print("-" * 90)

    while True:
        try:
            data = fetch(f"/v1/signal/atoms?n={count}")
            atoms = data.get("atoms", [])

            for atom in atoms:
                seq = atom.get("seq", 0)
                if seq <= last_seq:
                    continue
                last_seq = seq

                eco = ECOSYSTEMS.get(atom.get("ecosystem", 0), "?")
                print(
                    f"{seq:>10}  {eco:<8}  {atom.get('pair', 0):>4}  "
                    f"{atom.get('deviation_bps', 0):>+8}  "
                    f"{atom.get('entropy_score', 0):>10}  "
                    f"{atom.get('venue', '?'):<12}  "
                    f"{atom.get('price', '?')}"
                )

            time.sleep(interval)
        except KeyboardInterrupt:
            print("\nStopped.")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(interval)


if __name__ == "__main__":
    if "--pairs" in sys.argv:
        show_pairs()
    else:
        monitor()
