import socket, time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(0.5)
start = time.time()
result = sock.connect_ex(("127.0.0.1", 9999))
print("Result:", result, "Time:", round(time.time() - start, 2), "seconds")
sock.close()