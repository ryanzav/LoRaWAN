#!/usr/bin/env python3
import sys
import argparse
from time import sleep
from SX127x.LoRa import *
from SX127x.LoRaArgumentParser import LoRaArgumentParser
from SX127x.board_config_ada import BOARD
import LoRaWAN
from LoRaWAN.MHDR import MHDR
from random import randrange
import reset_ada

import helium
import keys

BOARD.setup()
parser = LoRaArgumentParser("LoRaWAN sender")

global frame
global msg
frame = 1
msg = 'Test'

class LoRaWANotaa(LoRa):
    def __init__(self, verbose = False):
        super(LoRaWANotaa, self).__init__(verbose)

    def on_rx_done(self):
        print("RxDone")

        self.clear_irq_flags(RxDone=1)
        payload = self.read_payload(nocheck=True)
        print(payload)  
        lorawan = LoRaWAN.new(keys.nwskey, keys.appskey)
        lorawan.read(payload)
        print(lorawan.get_mhdr().get_mversion())
        print(lorawan.get_mhdr().get_mtype())
        print(lorawan.get_mic())
        print(lorawan.compute_mic())
        print(lorawan.valid_mic())
        print("".join(list(map(chr, lorawan.get_payload()))))
        print("\n")
        
        self.set_mode(MODE.STDBY)

        s = ''
        s += " pkt_snr_value      %f\n" % self.get_pkt_snr_value()
        s += " pkt_rssi_value     %d\n" % self.get_pkt_rssi_value()
        s += " rssi_value         %d\n" % self.get_rssi_value()
        print(s)
        # lorawan = LoRaWAN.new([], appkey)
        # lorawan.read(payload)
        # print(lorawan.get_payload())

    def on_tx_done(self):
        self.clear_irq_flags(TxDone=1)
        print("TxDone")


        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0,0,0,0,0,0])
        self.set_invert_iq(1)
        self.reset_ptr_rx()
        self.set_freq(helium.DOWNFREQ)#915)        
        self.set_spreading_factor(7)#12)
        self.set_bw(9) #500Khz
        self.set_rx_crc(False)#TRUE
        self.set_mode(MODE.RXCONT)
        with open('.last_frame', 'w') as f:
            f.write(str(frame))
         


    def start(self):
        global frame
        global msg
        self.tx_counter = 2
        lorawan = LoRaWAN.new(keys.nwskey, keys.appskey)
        
        lorawan.create(MHDR.UNCONF_DATA_UP, {'devaddr': keys.devaddr, 'fcnt': frame, 'data': list(map(ord, msg)) })

        self.write_payload(lorawan.to_raw())
        self.set_mode(MODE.TX)
        
        sleep(10)


def init():
    lora = LoRaWANotaa(True)

    # Setup
    lora.set_mode(MODE.SLEEP)
    lora.set_dio_mapping([1,0,0,0,0,0])
    lora.set_freq(helium.UPFREQ)
    lora.set_pa_config(pa_select=1)
    lora.set_spreading_factor(7)
    lora.set_pa_config(max_power=0x0F, output_power=0x0E)
    lora.set_sync_word(0x34)
    lora.set_rx_crc(True)
    lora.get_all_registers()
    #print(lora)
    assert(lora.get_agc_auto_on() == 1)

    try:
        print("Sending LoRaWAN tx\n")
        lora.start()
        lora.set_mode(MODE.SLEEP)
        #print(lora)
    except KeyboardInterrupt:
        sys.stdout.flush()
        print("\nKeyboardInterrupt")
    finally:
        sys.stdout.flush()
        lora.set_mode(MODE.SLEEP)
        BOARD.teardown()


def main():
    global frame
    global msg
    parser = argparse.ArgumentParser(add_help=True, description="Trasnmit a LoRa msg")
    parser.add_argument("--frame", help="Message frame")
    parser.add_argument("--msg", help="tokens file")
    args = parser.parse_args()
    if args.frame is None:
        with open(".last_frame", 'r') as last_frame_file:
            frame = int(last_frame_file.read()) + 1
    else:
        frame = int(args.frame)
    if args.msg is None:
        msg = "Test"
    else:
        msg = args.msg
    init()

if __name__ == "__main__":
    main()
