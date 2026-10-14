# My Prodigy Task 5 - Packet Analyzer

Reads packets and prints from/to ip, protocol and a bit of the payload. Made with scapy.

Please only use on your own network or the sample pcap. Don't sniff other people's traffic.

## how to run

```
pip install scapy

python3 packet_analyzer.py --read test.pcap
```

Live capture (needs sudo, own wifi only):
```
sudo python3 packet_analyzer.py --sniff --count 10 --timeout 15
```

`test.pcap` is one I generated myself (3 packets, TCP + UDP + ICMP), no real traffic in it.

## files

- `packet_analyzer.py` - `analyze_packet()` prints one packet, totals at the end
- `test.pcap` - sample file to try `--read` with
