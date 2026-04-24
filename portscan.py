import socket
import datetime
import subprocess

COMMON_PORTS = {
    21:   "FTP",
    22:   "SSH",
    23:   "Telnet",
    25:   "SMTP",
    53:   "DNS",
    80:   "HTTP",
    110:  "POP3",
    143:  "IMAP",
    443:  "HTTPS",
    3306: "MySQL",
    3389: "RDP",
    8080: "HTTP-Alt"
}

def get_service_name(port):
    return COMMON_PORTS.get(port, "Unknown")

def resolve_host(host):
    try:
        return socket.gethostbyname(host)
    except socket.gaierror:
        return None

def get_banner(host, port, timeout=1):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host, port))
        sock.send(b"Hello\r\n")
        banner = sock.recv(1024).decode(errors="ignore").strip()
        sock.close()
        return banner if banner else "No banner"
    except:
        return "No banner"

def scan_port(host, port, timeout=1):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return "open" if result == 0 else "closed"
    except socket.timeout:
        return "filtered"
    except socket.error:
        return "error"

def quick_scan(host):
    common = list(COMMON_PORTS.keys())
    print(f"\n[*] Running QUICK SCAN on {host}...")
    print("-" * 55)
    results = []
    for port in common:
        status = scan_port(host, port)
        if status == "open":
            service = get_service_name(port)
            print(f"  [OPEN] Port {port:5} | Service: {service}")
            results.append({"port": port, "status": status, "service": service})
    print("-" * 55)
    print(f"[*] Done. {len(results)} open port(s) found.\n")
    return results

def scan_range(host, start_port, end_port):
    results = []
    print(f"\n[*] Scanning {host} — Ports {start_port} to {end_port}")
    print(f"[*] Started at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 55)
    for port in range(start_port, end_port + 1):
        status = scan_port(host, port)
        if status == "open":
            service = get_service_name(port)
            banner  = get_banner(host, port)
            print(f"  [OPEN] Port {port:5} | Service: {service:10} | Banner: {banner}")
            results.append({
                "port":    port,
                "status":  status,
                "service": service,
                "banner":  banner
            })
    print("-" * 55)
    print(f"[*] Scan complete. {len(results)} open port(s) found.\n")
    return results

def save_results(host, results, filename="scan_results.txt"):
    with open(filename, "w") as f:
        f.write(f"Scan Report for: {host}\n")
        f.write(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 55 + "\n")
        if not results:
            f.write("No open ports found.\n")
        else:
            for r in results:
                f.write(f"Port {r['port']} | {r['status']} | {r.get('service', '?')} | {r.get('banner', '')}\n")
    print(f"[*] Results saved to '{filename}'")

def main():
    subprocess.call('clear', shell=True)

    print("=" * 55)
    print("        Simple Port Scanner — Portfolio Project")
    print("=" * 55)

    print("\n[!] DISCLAIMER: Only scan hosts you own or have")
    print("    explicit permission to scan. Unauthorized")
    print("    scanning is illegal.\n")
    confirm = input("Do you have permission to scan the target? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("[!] Exiting. Please only scan targets you own.")
        return

    host_input = input("\nEnter target IP or hostname: ").strip()
    ip = resolve_host(host_input)

    if not ip:
        print(f"[!] Could not resolve '{host_input}'. Check the address and try again.")
        return

    print(f"[*] Resolved '{host_input}' → {ip}")

    print("\nSelect scan mode:")
    print("  [1] Quick Scan  (common ports only)")
    print("  [2] Range Scan  (you choose the port range)")
    choice = input("\nEnter choice (1 or 2): ").strip()

    if choice == "1":
        results = quick_scan(ip)
    elif choice == "2":
        try:
            start = int(input("Start port: ").strip())
            end   = int(input("End port:   ").strip())
            if start < 1 or end > 65535 or start > end:
                print("[!] Invalid port range. Ports must be between 1 and 65535.")
                return
            results = scan_range(ip, start, end)
        except ValueError:
            print("[!] Please enter valid numbers for ports.")
            return
    else:
        print("[!] Invalid choice.")
        return

    if results:
        save = input("Save results to file? (yes/no): ").strip().lower()
        if save == "yes":
            save_results(host_input, results)

if __name__ == "__main__":
    main()
