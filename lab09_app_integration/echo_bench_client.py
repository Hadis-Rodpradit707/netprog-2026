import socket
import sys
import time
import json

PORT = 5000  # must match the port used by echo_server.py (Lab 2)


def run_benchmark(server_ip, port=PORT, count=50, msg_size=64):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_ip, port))
    payload = b"x" * msg_size
    rtts_ms = []
    for i in range(count):
        # TODO 1
        start = time.perf_counter()
        sock.sendall(payload)
        # TCP is a byte stream: keep reading until the whole echo is back
        received = 0
        while received < msg_size:
            chunk = sock.recv(msg_size - received)
            if not chunk:
                raise ConnectionError("server closed the connection")
            received += len(chunk)
        # TODO 2
        rtts_ms.append((time.perf_counter() - start) * 1000)
    sock.close()
    return rtts_ms


if __name__ == "__main__":
    server_ip = sys.argv[1]
    label = sys.argv[2] if len(sys.argv) > 2 else "run"
    rtts_ms = run_benchmark(server_ip)
    avg = sum(rtts_ms) / len(rtts_ms)
    std = (sum((r - avg) ** 2 for r in rtts_ms) / len(rtts_ms)) ** 0.5
    print(f"{label}: min={min(rtts_ms):.3f}ms avg={avg:.3f}ms max={max(rtts_ms):.3f}ms "
          f"std={std:.3f}ms n={len(rtts_ms)}")
    with open(f"rtt_{label}.json", "w") as f:
        json.dump(rtts_ms, f)
