import socket
import threading

HOST = "0.0.0.0"
PORT = 6000

clients = set()
clients_lock = threading.Lock()


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    print(f"UDP chat server listening on {HOST}:{PORT}")

    while True:
        data, addr = sock.recvfrom(1024)
        with clients_lock:
            # TODO 1: if addr is new, remember it
            if addr not in clients:
                clients.add(addr)
                print(f"New client: {addr}")
            recipients = list(clients)

        # Task 5: prefix each broadcast with the sender's address
        message = f"[{addr[0]}:{addr[1]}]: {data.decode('utf-8')}"
        for client_addr in recipients:
            # TODO 2: broadcast the message to every remembered client
            sock.sendto(message.encode("utf-8"), client_addr)


if __name__ == "__main__":
    main()
