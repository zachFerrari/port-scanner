import socket
#**= the lines identified by this simbol are coming from the first scratch of the program which used to control only one port for time.

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

#first=int(input("Instert the port u wanna scan : "))#**
host="127.0.0.1"
start=int(input("First port of the range: "))
end=int(input("Last port:"))
def is_port_open(host,port,timeout=0.1):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create the connection TCP
    sock.settimeout(timeout) #if the port doesn't answer it doesn't wait
    result=sock.connect_ex((host,port)) # try to connect and if he succes, so the port is open, he return 0
    sock.close()
    return result == 0
def scan_range(host, start, end):
    open_ports=[]
    for port in range(start, end+1):
        if is_port_open(host,port):
            name = SERVICES.get(port, "unknown")
            print(f"Port {port} is OPEN ({name})")
            open_ports.append(port)
    return open_ports

found = scan_range(host, start, end)

#print(is_port_open("127.0.0.1", first)) #**
print(f"Scan finished. Open ports: {found}")