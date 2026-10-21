import time
from mn_wifi.net import Mininet_wifi
from mn_wifi.cli import CLI
from mininet.log import setLogLevel, info

def topology():
    net = Mininet_wifi()

    info("*** Creating nodes\n")
    sta1 = net.addStation('sta1', position='15,50,0')
    sta2 = net.addStation('sta2', position='85,50,0')
    sta3 = net.addStation('sta3', position='10,50,0')
    ap1 = net.addAccessPoint('ap1', ssid='netprog-ap1', mode='g', channel='1',
                             position='20,50,0', range=35, failMode='standalone')
    ap2 = net.addAccessPoint('ap2', ssid='netprog-ap2', mode='g', channel='6',
                             position='80,50,0', range=35, failMode='standalone')

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()
    net.addLink(ap1, ap2)

    # Mobility must be declared BEFORE net.build() in this Mininet-WiFi version
    info("*** Configuring mobility\n")
    net.startMobility(time=0)
    # TODO 2
    net.mobility(sta3, 'start', time=1, position='10,50,0')
    # TODO 3
    net.mobility(sta3, 'stop', time=20, position='90,50,0')
    net.stopMobility(time=21)

    info("*** Starting network\n")
    net.build()
    net.start()

    # Part E: background ping from sta3 to sta1 during the walk
    sta3.cmd('ping -i 0.5 10.0.0.1 > /tmp/sta3_ping.log &')

    info("*** Monitoring sta3 association during mobility\n")
    for t in range(22):
        # TODO 4: this Mininet-WiFi version stores the association on the wireless interface
        assoc = sta3.params.get('associatedTo') or sta3.wintfs[0].associatedTo
        x = round(float(sta3.position[0]), 1)
        print(f"t={t}s sta3 x={x}m associated to: {assoc}")
        time.sleep(1)

    CLI(net)
    net.stop()

if __name__ == "__main__":
    setLogLevel("info")
    topology()
