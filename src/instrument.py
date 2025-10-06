from RsInstrument import *

class Instrument:

    def FSC_init(inst_ip = '192.168.0.106'):
        inst = RsInstrument(f'TCPIP::{inst_ip}::INSTR', id_query=True, reset=True)
        inst_name = inst.query("*IDN?")
        print(inst_name)
        if inst_name.find("FSV6"):
            print(f"Connected successfully to FSV6 at IP address {inst_ip}")            
        else:
            raise ConnectionError(f"Failed to connect to instrument at {inst_ip}")

        return inst