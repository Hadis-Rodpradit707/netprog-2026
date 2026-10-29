import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

with open("rtt_near.json") as f:
    near = json.load(f)
with open("rtt_far.json") as f:
    far = json.load(f)

avg_near = sum(near) / len(near)
avg_far = sum(far) / len(far)

plt.figure(figsize=(9, 4.5))
plt.plot(near, label=f"near (5m), avg {avg_near:.3f} ms", marker=".", color="tab:blue")
plt.plot(far, label=f"far (28m), avg {avg_far:.3f} ms", marker=".", color="tab:red")
plt.axhline(avg_near, color="tab:blue", linestyle="--", linewidth=1, alpha=0.7)
plt.axhline(avg_far, color="tab:red", linestyle="--", linewidth=1, alpha=0.7)
plt.ylim(bottom=0)
plt.grid(True, linestyle=":", alpha=0.6)
plt.xlabel("Message number")
plt.ylabel("Application RTT (ms)")
plt.title("Application-Level RTT: Near vs. Far")
plt.legend()
plt.tight_layout()
plt.savefig("rtt_plot.png", dpi=150)
print("Saved rtt_plot.png")
