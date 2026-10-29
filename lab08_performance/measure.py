import json
import sys
import time

from mn_wifi.net import Mininet_wifi
from mn_wifi.cli import CLI
from mininet.log import setLogLevel, info

DISTANCES = [5, 10, 15, 20, 25, 30]


def run_iperf3_udp(server_sta, client_sta, server_ip, duration=5, bitrate="10M"):
    # Free port 5201 in case an iperf3 server is left over from a failed run
    server_sta.cmd("pkill -9 iperf3")
    server_sta.cmd(f"iperf3 -s -1 -J > /tmp/server_{client_sta.name}.json &")
    time.sleep(1)  # give the server a moment to start listening
    # TODO 1 (timeout stops the client hanging if the station has lost the AP)
    client_sta.cmd(f"timeout {duration + 15} iperf3 -c {server_ip} -u -b {bitrate} "
                   f"-t {duration} -J > /tmp/client_{client_sta.name}.json")
    time.sleep(1)
    try:
        with open(f"/tmp/client_{client_sta.name}.json") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        data = {"error": f"no valid JSON from client ({e.__class__.__name__})"}

    if "error" in data or "sum" not in data.get("end", {}):
        # Client could not reach the server: record a total outage instead of crashing
        return {"throughput_mbps": 0.0, "jitter_ms": None, "loss_percent": 100.0,
                "error": data.get("error", "no end.sum in iperf3 JSON")}

    # TODO 2
    summary = data["end"]["sum"]
    result = {
        "throughput_mbps": round(summary["bits_per_second"] / 1e6, 3),
        "jitter_ms": round(summary["jitter_ms"], 3),
        "loss_percent": round(summary["lost_percent"], 3),
    }
    # end.sum is the sender's rate; iperf3 3.16 also reports what really arrived
    received = data["end"].get("sum_received")
    if received:
        result["received_mbps"] = round(received["bits_per_second"] / 1e6, 3)
    return result


def link_info(sta):
    """Return (associated AP interface, signal in dBm) for the station."""
    intf = sta.wintfs[0]
    assoc = sta.params.get('associatedTo') or intf.associatedTo
    signal = None
    for line in sta.cmd(f"iw dev {intf.name} link").splitlines():
        if "signal:" in line:
            signal = int(line.split()[1])
    return (str(assoc) if assoc else None), signal


def topology(single_distance=None):
    net = Mininet_wifi()

    info("*** Creating nodes\n")
    sta1 = net.addStation('sta1', position='5,50,0')
    sta2 = net.addStation('sta2', position='0,50,0')
    net.addAccessPoint('ap1', ssid='netprog-ap', mode='g', channel='1',
                       position='0,50,0', range=30, failMode='standalone')

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Starting network\n")
    net.build()
    net.start()
    time.sleep(2)  # let both stations finish associating

    distances = [single_distance] if single_distance is not None else DISTANCES
    results = []
    for d in distances:
        info(f"*** Measuring at distance {d}m\n")
        # TODO 3
        sta1.setPosition(f"{d},50,0")
        time.sleep(1)  # let the wireless link settle after moving
        assoc, signal = link_info(sta1)
        r = run_iperf3_udp(sta2, sta1, sta2.IP())
        # TODO 4
        r["distance_m"] = d
        r["associated_to"] = assoc
        r["signal_dbm"] = signal
        results.append(r)
        print(d, r)

    if single_distance is None:
        with open("results.json", "w") as f:
            json.dump(results, f, indent=2)
        info("*** Saved results.json\n")

    CLI(net)
    net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    if len(sys.argv) == 3 and sys.argv[1] == "--single":
        topology(single_distance=int(sys.argv[2]))   # Task 2: one measurement
    else:
        topology()                                    # Task 3: full sweep
