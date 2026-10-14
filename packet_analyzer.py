#!/usr/bin/env python3
# packet analyzer - prodigy task 5
# reads a pcap or sniffs my own network, prints src/dst ip + proto + payload

import argparse
import datetime
import sys

try:
    from scapy.all import IP, TCP, UDP, ICMP, Raw, rdpcap, sniff
    from scapy.error import Scapy_Exception
except ImportError:
    print("need scapy: pip install scapy", file=sys.stderr)
    sys.exit(1)

NOTE = "for learning only - only look at your own network or pcaps you made."

counts = {"TCP": 0, "UDP": 0, "ICMP": 0, "other": 0, "total": 0}


def payload(pkt, n=64):
    data = b""
    try:
        for layer in (TCP, UDP, ICMP):
            if pkt.haslayer(layer):
                data = bytes(pkt[layer].payload)
                break
        if not data and pkt.haslayer(Raw):
            data = bytes(pkt[Raw].load)
    except Exception:
        data = b""
    if not data:
        return "-", "-"
    part = data[:n]
    hx = part.hex()
    txt = "".join(chr(b) if 32 <= b < 127 else "." for b in part)
    return hx, txt


def analyze_packet(pkt):
    try:
        ts = datetime.datetime.fromtimestamp(float(pkt.time)).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        ts = "-"

    if pkt.haslayer(IP):
        src = pkt[IP].src
        dst = pkt[IP].dst
    else:
        src = "-"
        dst = "-"

    if pkt.haslayer(TCP):
        proto = "TCP"
    elif pkt.haslayer(UDP):
        proto = "UDP"
    elif pkt.haslayer(ICMP):
        proto = "ICMP"
    else:
        proto = "other"

    size = len(pkt)
    hx, txt = payload(pkt)

    counts[proto] = counts.get(proto, 0) + 1
    counts["total"] += 1
    i = counts["total"]

    print("--- packet " + str(i) + " ---")
    print("  time: " + ts)
    print("  from: " + str(src))
    print("  to:   " + str(dst))
    print("  proto: " + proto)
    print("  len: " + str(size))
    print("  data hex: " + hx)
    print("  data txt: " + txt)
    return proto


def show_total():
    print("\n== total ==")
    print("  packets: " + str(counts["total"]))
    print("  TCP: " + str(counts["TCP"]))
    print("  UDP: " + str(counts["UDP"]))
    print("  ICMP: " + str(counts["ICMP"]))
    print("  other: " + str(counts["other"]))


def clear():
    for k in counts:
        counts[k] = 0


def read_file(path):
    clear()
    try:
        pkts = rdpcap(path)
    except FileNotFoundError:
        print("not found: " + path, file=sys.stderr)
        sys.exit(1)
    except Scapy_Exception as e:
        print("cant read pcap: " + str(e), file=sys.stderr)
        sys.exit(1)
    if len(pkts) == 0:
        print("empty pcap")
        return
    print("reading " + str(len(pkts)) + " from " + path + "\n")
    for p in pkts:
        analyze_packet(p)
    show_total()


def do_sniff(count=10, timeout=15):
    clear()
    print("sniffing count=" + str(count) + " timeout=" + str(timeout))
    print(NOTE)
    try:
        pkts = sniff(count=count, timeout=timeout)
    except PermissionError:
        print("\nneed sudo for live capture. or just use --read test.pcap", file=sys.stderr)
        sys.exit(1)
    except Scapy_Exception as e:
        print("\n" + str(e), file=sys.stderr)
        print("try sudo on your own network, or use --read mode", file=sys.stderr)
        sys.exit(1)
    if not pkts:
        print("nothing captured")
        return
    print("\ngot " + str(len(pkts)) + "\n")
    for p in pkts:
        analyze_packet(p)
    show_total()


def main(argv=None):
    p = argparse.ArgumentParser(description="packet analyzer - " + NOTE)
    p.add_argument("--read", metavar="PCAP")
    p.add_argument("--sniff", action="store_true")
    p.add_argument("--count", type=int, default=10)
    p.add_argument("--timeout", type=int, default=15)
    a = p.parse_args(argv)
    if a.read:
        read_file(a.read)
    elif a.sniff:
        do_sniff(count=a.count, timeout=a.timeout)
    else:
        p.print_help()
        print("\nexamples:")
        print("  python3 packet_analyzer.py --read test.pcap")
        print("  sudo python3 packet_analyzer.py --sniff --count 10")
        print("\n" + NOTE)
        sys.exit(2)


if __name__ == "__main__":
    main()
