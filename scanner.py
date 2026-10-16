import socket
#first=int(input("Instert the port u wanna scan : "))
host="127.0.0.1"
start=int(input("First port of the range: "))
end=int(input("Last port:"))
def is_port_open(host,port,timeout=5):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create the connection TCP
    sock.settimeout(timeout) #if the port doesn't answer it doesn't wait
    result=sock.connect_ex((host,port)) # try to connect and if he succes, so the port is open, he return 0
    sock.close()
    return result == 0
def scan_range(host, start, end):
    open_ports=[]
    for port in range(start, end+1):
        if is_port_open(host,port):
            print(f"Port {port} is OPEN")
            open_ports.append(port)
    return open_ports

found = scan_range(host, start, end)

#print(is_port_open("127.0.0.1", first))
print(f"Scan finished. Open ports: {found}")