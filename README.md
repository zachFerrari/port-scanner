# Port Scanner

A simple multithreaded TCP port scanner written in Python, built as a learning project
on networking and security fundamentals.

## Features
- Scans a range of TCP ports on a given host
- Multithreaded scanning (configurable number of workers)
- Recognises common services (HTTP, SSH, SMB, ...)
- Command-line interface built with `argparse`
- Optional JSON report

## Legal notice
Only scan hosts you own or have explicit permission to test.
Safe targets: `127.0.0.1` (your own machine) and `scanme.nmap.org`
(provided by the Nmap project for testing).

## Requirements
- Python 3.8+
- No external libraries (standard library only)

## Usage
```
python scanner.py <host> [-s START] [-e END] [-w WORKERS] [-t TIMEOUT] [-o OUTPUT]
```

Example:
```
python scanner.py 127.0.0.1 -s 1 -e 10000 -w 500 -o report.json
```

| Option | Description | Default |
|---|---|---|
| `-s`, `--start` | First port | 1 |
| `-e`, `--end` | Last port | 1024 |
| `-w`, `--workers` | Number of threads | 100 |
| `-t`, `--timeout` | Timeout per port (seconds) | 0.5 |
| `-o`, `--output` | Save results to a JSON file | none |

## Example output
Scan of my own machine, ports 1-10000, 500 threads:
```
Port 135 is OPEN (RPC (Windows))
Port 445 is OPEN (SMB (Windows))
Port 2680 is OPEN (unknown)
Port 5040 is OPEN (unknown)
Port 8000 is OPEN (HTTP alternate)
Port 8033 is OPEN (unknown)
Scan finished in 10.45s. Open ports: [135, 445, 2680, 5040, 8000, 8033]
```

Example of the JSON report (`-o report.json`):
```json
{
  "host": "127.0.0.1",
  "range": [1, 1024],
  "open_ports": [
    { "port": 135, "service": "RPC (Windows)" },
    { "port": 445, "service": "SMB (Windows)" }
  ]
}
```

## Analysis of the open ports found

I ran the scanner against my own machine (`127.0.0.1`, ports 1-10000) and traced each
open port back to the process that owns it, using `netstat -ano` to get the PID and
`tasklist` to get the process name.

| Port | Service | Process | Notes |
|---|---|---|---|
| 135 | RPC (Windows) | Windows system service | Remote Procedure Call endpoint mapper. Normal on Windows. |
| 445 | SMB (Windows) | Windows system service | File and printer sharing. Normal on Windows, but historically targeted by attacks (e.g. WannaCry), so it should never be exposed directly to the internet. |
| 2680 | unknown | `MathWorksServiceHost.exe` | Background service of MATLAB (licensing and updates). The port is dynamic and may change at each start. |
| 5040 | unknown | `svchost.exe` | Windows Service Host, most likely the Connected Devices Platform service (CDPSvc). |

The other open ports were a local test web server (8000, started with
`python -m http.server 8000`) and port 8033, which `netstat` attributes to the Windows
`System` process and which I have not identified yet.

### Method
1. Scan the host and list the open ports.
2. For each unknown port, find the PID: `netstat -ano | findstr :<port>`
3. Find the process name: `tasklist /fi "PID eq <pid>"`
4. Check that the executable is in the expected folder, since a process name alone can be
   imitated by malware.

### Takeaways
- Every open port belongs to a process, and an unknown port should always be identified.
- A process name is not enough to trust it: the file location must be checked too.
- Listening on `127.0.0.1` (local only) is different from listening on `0.0.0.0`
  (all network interfaces), which is more exposed.

## Performance
On my machine closed ports do not refuse connections immediately: they time out.
With a 0.5 s timeout, a sequential scan of 1024 ports therefore takes about
8.5 minutes (estimated as 1024 × 0.5 s). Since the time is spent waiting for the network
and not computing, running many checks in parallel with threads removes most of it.

Same scan (ports 1-1024, timeout 0.5 s, target `127.0.0.1`):

| Workers | Time | Speed-up vs. sequential (estimated) |
|---|---|---|
| 1 (sequential) | about 512 s (estimated) | 1x |
| 10 | 52.43 s | about 10x |
| 100 | 5.59 s | about 90x |
| 500 | 1.54 s | about 330x |

A wider scan (ports 1-10000) with 500 workers took 10.45 s.

The time drops almost in proportion to the number of workers, which confirms that the
bottleneck is waiting, not CPU work. Very high thread counts (thousands) can slow
down or destabilise the system, so 100-500 is a reasonable range.

## What I learned
- How TCP connections and ports work, and what open / closed / filtered mean
- Why network-bound tasks benefit from threads, and how to measure the improvement
- How to trace an open port to its process with `netstat` and `tasklist`
- How to build a command-line tool with `argparse`
- How to use Git and GitHub, with small and frequent commits

## Possible improvements
- Identify port 8033 (use `netsh http show servicestate view=requestq`)
- Banner grabbing to identify services
- UDP scanning
- Progress bar
- CSV output
