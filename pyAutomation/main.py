from pyvisa import ResourceManager, constants
import time

import os
import random


# TODO: create GUI for easy interaction with PSU
class Channel:
    def __init__(self, instrument, channel_id):
        self.instrument = instrument
        self.channel_id = channel_id

    def set_params(self, voltage, current):
        self.instrument.write('*IDN?')
        self.instrument.write(f"INST:NSEL {self.channel_id}\nAPPL {voltage}, {current}")
        self.instrument.read_bytes(1)
        self.instrument.read('\n')
        print(f"channel: {self.channel_id}\nvoltage: {voltage}\ncurrent: {current}")

    def state_switch(self, state):
        self.instrument.write('*IDN?')
        self.instrument.write(f"INST:NSEL {self.channel_id}\nOUTP:SEL {state}\n")
        self.instrument.read_bytes(1)
        self.instrument.read('\n')


def global_state(instrument, state):
    instrument.write('*IDN?')
    instrument.write(f"OUTP:GEN {state}")
    instrument.read_bytes(1)
    instrument.read('\n')


def main():
    with ResourceManager().open_resource("ASRL4::INSTR") as psu:
        ch1 = Channel(psu, 1)
        ch1.set_params(2, .5)
        ch1.state_switch(1)
        global_state(psu, 1)
        for i in range(61):
            ch1.set_params(i/2, .5)
            time.sleep(.5)
        time.sleep(5)
        global_state(psu, 0)


if __name__ == "__main__":
    main()
