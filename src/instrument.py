from RsInstrument import *
import socket, sys, ipaddress
from scapy.all import ARP, Ether, srp, conf

class Instrument:

    RS_OUIS = ("00:90:B8",)   # Rohde & Schwarz OUI
    SCPI_PORT = 5025
    TIMEOUT = 2.0

    """
    Find Rohde&Schwarz FSC6 on local LAN:
    - ARP-scan the local /24 using scapy (fast)
    - Filter by MAC OUI (00:90:B8) *or* try connecting to SCPI socket 5025
    - If port 5025 is open, send '*IDN?' and read response
    """
    def get_local_net(self):
        # Find network address mask and use /24
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
        except Exception:
            ip = "192.168.1.100"
        finally:
            s.close()
        net = ip.rsplit(".", 1)[0] + ".0/24"
        return net

    def arp_scan(self, network_cidr, timeout=2):  # ARP-scan the local network
        conf.verb = 0
        pkt = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=network_cidr)
        ans, _ = srp(pkt, timeout=timeout)
        devices = []
        for _, r in ans:
            devices.append((r.psrc, r.hwsrc))
        return devices
    
    def fsc_search(self):   # SA search in LAN
        net = self.get_local_net()
        print(f"Scanning {net} via ARP ... (run as root/admin)")
        devs = self.arp_scan(net, timeout=2)
        print(f"ARP results: {len(devs)} devices found.")
        matches = []
        for ip, mac in devs:
            mac_up = mac.upper().replace("-", ":")
            is_rs = any(mac_up.startswith(oui) for oui in self.RS_OUIS)
            if is_rs:
                matches.append({"ip": ip, "mac": mac_up, "rs_by_mac": is_rs})
        if not matches:
            print("No analyzer found by OUI")
        else:
            print("Rohde & Schwarz instruments found:")
            for m in matches:
                print(f" - {m['ip']}  MAC={m['mac']}  OUI_match={m['rs_by_mac']}")
            found = next((x for x in matches), matches[0])
            return found['ip']
    
    def fsc_init(instr_ip):  # SA init by given IP
        instr = RsInstrument(f'TCPIP::{instr_ip}::INSTR', id_query=True, reset=True)
        instr_name = instr.query("*IDN?")
        print(instr_name)
        if instr_name.find("FSV6"):
            print(f"Connected successfully to FSV6 at IP address {instr_ip}")            
        else:
            raise ConnectionError(f"Failed to connect to instrument at {instr_ip}")

        return instr