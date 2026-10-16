import argparse
import socket
import time
import json #extension for the output file
from concurrent.futures import ThreadPoolExecutor  # manages the threads

SERVICES = {
    21: "FTP",
    22: "SSH",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    135: "RPC (Windows)",
    443: "HTTPS",
    445: "SMB (Windows)",
    3306: "MySQL",
    8000: "HTTP alternate",
}


def is_port_open(host, port, timeout=0.5):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create the TCP connection
    sock.settimeout(timeout)  # don't wait forever if the port doesn't answer
    result = sock.connect_ex((host, port))  # returns 0 if the connection succeeds
    sock.close()
    return result == 0


def scan_range(host, start, end, workers=100, timeout=0.5):
    ports = range(start, end + 1)
    with ThreadPoolExecutor(max_workers=workers) as executor:
        results = executor.map(lambda p: is_port_open(host, p, timeout), ports)
    open_ports = []
    for port, is_open in zip(ports, results):
        if is_open:
            name = SERVICES.get(port, "unknown")
            print(f"Port {port} is OPEN ({name})")
            open_ports.append(port)
    return open_ports


def main():
    parser = argparse.ArgumentParser(description="Simple TCP port scanner")
    parser.add_argument("host", help="Host to scan (e.g. 127.0.0.1)")
    parser.add_argument("-s", "--start", type=int, default=1, help="First port")
    parser.add_argument("-e", "--end", type=int, default=1024, help="Last port")
    parser.add_argument("-w", "--workers", type=int, default=100, help="Number of threads")
    parser.add_argument("-t", "--timeout", type=float, default=0.5, help="Timeout in seconds")
    parser.add_argument("-o", "--output", help="Save results to a JSON file")
    args = parser.parse_args()

    t0 = time.time()
    found = scan_range(args.host, args.start, args.end, args.workers, args.timeout)
    print(f"Scan finished in {time.time() - t0:.2f}s. Open ports: {found}")
    if args.output:
        report = { #new dictionary 
            "host": args.host,
            "range": [args.start, args.end],
            "open_ports": [
                {"port": p, "service": SERVICES.get(p, "unknown")} for p in found
            ],
        }
    with open(args.output, "w") as f:
        json.dump(report, f, indent=2)
    print(f"Report saved to {args.output}")

if __name__ == "__main__":
    main()