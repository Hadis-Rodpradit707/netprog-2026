import socket
import threading

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 6000


def listen(sock):
    while True:
        # TODO 3: receive broadcasts and print them on their own line
        data, _ = sock.recvfrom(1024)
        print(f"\n{data.decode('utf-8')}\n> ", end="")


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # TODO 4: start a daemon thread running listen(sock)
    thread = threading.Thread(target=listen, args=(sock,), daemon=True)
    thread.start()

    print("UDP chat client. Type a message and press Enter ('quit' to exit).")
    while True:
        message = input("> ")
        if message.lower() == "quit":
            break
        sock.sendto(message.encode("utf-8"), (SERVER_HOST, SERVER_PORT))

    sock.close()


if __name__ == "__main__":
    main()
