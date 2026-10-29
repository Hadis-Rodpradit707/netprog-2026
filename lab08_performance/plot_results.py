import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

AP_RANGE = 30  # ap1 range configured in measure.py

with open("results.json") as f:
    results = json.load(f)

distances = [r["distance_m"] for r in results]
# end.sum in iperf3 3.16 is the SENDER's rate; sum_received is what actually arrived
throughput = [r["throughput_mbps"] for r in results]
received = [r.get("received_mbps", r["throughput_mbps"]) for r in results]
loss = [r["loss_percent"] for r in results]
jitter = [r["jitter_ms"] or 0 for r in results]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.3))

# Panel 1: throughput vs distance
ax1.plot(distances, received, marker="o", color="tab:blue", label="Received (delivered)")
ax1.plot(distances, throughput, marker="s", linestyle="--", color="grey",
         label="Sent (iperf3 end.sum)")
for x, y in zip(distances, received):
    ax1.annotate(f"{y:.2f}", (x, y), textcoords="offset points",
                 xytext=(-14, -12) if x == AP_RANGE else (0, -15),
                 ha="center", fontsize=8, color="tab:blue")
ax1.set_ylim(0, 11)
ax1.set_xlabel("Distance from AP (m)")
ax1.set_ylabel("Throughput (Mbps)")
ax1.set_title("Throughput vs. Distance")
ax1.legend(loc="lower left", fontsize=8)

# Panel 2: packet loss vs distance (jitter on a second axis)
l1 = ax2.plot(distances, loss, marker="o", color="crimson", label="Packet loss (%)")
for x, y in zip(distances, loss):
    ax2.annotate(f"{y:g}%", (x, y), textcoords="offset points", xytext=(0, 7),
                 ha="center", fontsize=8, color="crimson")
ax2.set_ylim(0, 5)
ax2.set_xlabel("Distance from AP (m)")
ax2.set_ylabel("Packet Loss (%)")
ax2.set_title("Packet Loss (and Jitter) vs. Distance")
ax2b = ax2.twinx()
l2 = ax2b.plot(distances, jitter, marker="^", color="darkorange", label="Jitter (ms)")
ax2b.set_ylim(0, max(jitter) * 1.6 if max(jitter) > 0 else 1)
ax2b.set_ylabel("Jitter (ms)")
ax2.legend(l1 + l2, [l.get_label() for l in l1 + l2], loc="upper left", fontsize=8)

for ax in (ax1, ax2):
    ax.set_xticks(distances)
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.axvline(AP_RANGE, color="grey", linestyle="--", linewidth=1)
    ax.text(AP_RANGE - 0.5, ax.get_ylim()[1] * 0.45, "AP range = 30 m", rotation=90,
            color="grey", va="center", ha="right", fontsize=8)

fig.tight_layout()
fig.savefig("performance_plot.png", dpi=150)
print("Saved performance_plot.png")
