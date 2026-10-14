# PRODIGY_CS_05

A network packet analyzer written in Python with Scapy, built for Task 5 of the
Prodigy InfoTech Cyber Security internship.

It reads network packets and prints a short summary of each one — where it came from,
where it's going, the protocol, and a preview of the data inside.

## What it does

- Reads a saved `.pcap` file or sniffs live traffic
- Picks out TCP, UDP and ICMP packets
- Shows source/destination IP, protocol and a payload preview (text when readable, hex otherwise)
- Prints a total count per protocol at the end

## Ethics

Only run this on your own network or on the sample pcap. Don't capture other people's traffic.

## Setup

```bash
pip install scapy
```

## How to run

```bash
# read the included sample capture (no root needed)
python3 packet_analyzer.py --read test.pcap

# live capture on your own network (needs sudo for raw sockets)
sudo python3 packet_analyzer.py --sniff --count 10 --timeout 15
```

## Example output

```
$ python3 packet_analyzer.py --read test.pcap
--- packet 1 ---
  proto: TCP
  from: 192.168.1.10
  to:   93.184.216.34
...
== total ==
  packets: 3
  TCP: 1
  UDP: 1
  ICMP: 1
```

## Files

- `packet_analyzer.py` — `analyze_packet()` prints one packet, totals at the end
- `test.pcap` — sample capture (3 packets: TCP + UDP + ICMP), made for testing `--read`
