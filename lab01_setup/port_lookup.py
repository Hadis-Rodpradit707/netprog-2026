import socket


def classify_port(port):
    """Return the IANA range name for a port number (from Lesson 1)."""
    if 0 <= port <= 1023:
        return "Well-Known"
    elif 1024 <= port <= 49151:
        return "Registered"
    elif 49152 <= port <= 65535:
        return "Dynamic/Private"
    else:
        return "Invalid (out of 0-65535 range)"


def main():
    host = input("Hostname: ")
    port = int(input("Port: "))
    ip = socket.gethostbyname(host)
    print(f"{host} resolves to {ip}")
    print(f"Port {port} is classified as: {classify_port(port)}")


if __name__ == "__main__":
    main()
