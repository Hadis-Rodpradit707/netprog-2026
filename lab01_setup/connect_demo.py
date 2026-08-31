import socket
import time

s = socket.create_connection(("www.python.org", 443))
print("Connected:", s.getpeername())
time.sleep(5)  # keep it open so you can inspect it
s.close()
