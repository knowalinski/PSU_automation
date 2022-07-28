import time


class Device:
    def __init__(self, serial_id):
        self.serial_id = serial_id
        self.switch = 0

    def override_switch(self, new_switch):
        # allow to modify self.switch variable outside of class
        self.switch = new_switch

    def switch_state(self):
        return 0 if self.switch == 1 else 1

    def state_command(self):
        self.switch = self.switch_state()
        return f"OUTP:GEN {self.switch}\n"

    def _serial_handler(body):
        # decorator preventing PSU timeouts
        def wrapper(self, *arg, **kw):
            self.serial_id.open()
            time.sleep(.015)
            body(self, *arg, **kw)
            time.sleep(.015)
            self.serial_id.close()

        return wrapper

    @_serial_handler
    def set_state(self):
        self.serial_id.write(self.state_command().encode())


class Channel(Device):
    def __init__(self, channel_id, serial_id):
        super().__init__(serial_id)
        self.channel_id = channel_id

    @Device._serial_handler
    def set_params(self, voltage, current):
        self.serial_id.write(f"INST:NSEL {self.channel_id}\nAPPL {voltage}, {current}\n".encode())

    def state_command(self):
        self.switch = self.switch_state()
        return f"INST:NSEL {self.channel_id}\nOUTP:SEL {self.switch}\n"
