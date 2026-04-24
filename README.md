# Python-Port-Scanner
Python 3 port scanner featuring TCP connect scan, banner grabbing, service identification, threading, network range support, and result exporting.

## How to Run?
### Run directly from GitHub
```bash
curl -s https://raw.githubusercontent.com/stacey-byte/Python-Port-Scanner/main/portscan.py | python3
```
No download needed, fetches and runs the scanner in one command.


## Disclaimer
This tool is intended for educational purposes only. Only scan hosts you own or have explicit permission to scan. Unauthorized port scanning is illegal.

## What I Learned
- How TCP connections work using Python sockets
- Why banner grabbing is important : it reveals the software and version running on an open port
- How threading speeds up network scanning
- How to scan entire network ranges using CIDR notation

