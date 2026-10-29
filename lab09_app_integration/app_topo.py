from mn_wifi.net import Mininet_wifi
from mn_wifi.cli import CLI
from mininet.log import setLogLevel, info
import time


def topology():
    net = Mininet_wifi()
    info("*** Creating nodes\n")
    sta1 = net.addStation('sta1', position='0,50,0')
    sta2 = net.addStation('sta2', position='5,50,0')
    net.addAccessPoint('ap1', ssid='netprog-ap', mode='g', channel='1',
                       position='0,50,0', range=30, failMode='standalone')
    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()
    info("*** Starting network\n")
    net.build()
    net.start()
    time.sleep(2)  # let both stations finish associating

    sta1.cmd('pkill -f echo_server.py')  # clean up any stale server from a previous run
    sta1.cmd('python3 echo_server.py > /tmp/echo_server.log 2>&1 &')
    time.sleep(1)

    # Part D: one benchmark near the AP
    info("*** Running benchmark at distance=5\n")
    output = sta2.cmd(f'python3 echo_bench_client.py {sta1.IP()} near')
    print(output)

    # Part E: move sta2 close to the edge of ap1's range (range=30)
    sta2.setPosition('28,50,0')
    time.sleep(1)  # let the wireless link settle after moving

    info("*** Running benchmark at distance=28\n")
    output = sta2.cmd(f'python3 echo_bench_client.py {sta1.IP()} far')
    print(output)

    CLI(net)
    sta1.cmd('pkill -f echo_server.py')
    net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    topology()
