# TODO: display channel parameters as placeholders
# TODO: add CSS to make it more readable
# TODO: refactor code
# TODO: deploy to local network


from flask import Flask, render_template, request
import serial
import time

# creating instance of flask app
app = Flask(__name__)

# defining parameters of serial connection
ser = serial.Serial()
ser.baudrate = 19200
ser.port = "COM3"


class Device:
    def __init__(self, serial_id):
        self.serial_id = serial_id
        self.switch = 0

    def switch_state(self):
        return 1 if self.switch == 0 else 0

    def scpi_command(self):
        self.switch = self.switch_state()
        return f"OUTP:GEN {self.switch}"

    def set_state(self):
        self.serial_id.open()
        time.sleep(.02)
        self.serial_id.write(self.scpi_command().encode())
        time.sleep(.02)
        self.serial_id.close()


class Channel(Device):
    def __init__(self, channel_id, serial_id):
        super().__init__(serial_id)
        self.channel_id = channel_id
        # self.statement = f"INST:NSEL {self.channel_id}\nOUTP:SEL {self.switch}"

    def set_params(self, voltage, current):
        self.serial_id.open()
        time.sleep(.02)
        self.serial_id.write(f"INST:NSEL {self.channel_id}\nAPPL {voltage}, {current}".encode())
        time.sleep(.02)
        self.serial_id.close()

    def scpi_command(self):
        self.switch = self.switch_state()
        return f"INST:NSEL {self.channel_id}\nOUTP:SEL {self.switch}"


general = Device(ser)
ch1 = Channel(1, ser)
ch2 = Channel(2, ser)
ch3 = Channel(3, ser)
ch4 = Channel(4, ser)


def state_analise():
    if 'ch1' in request.form.to_dict():
        ch1.set_state()
    if 'ch2' in request.form.to_dict():
        ch2.set_state()
    if 'ch3' in request.form.to_dict():
        ch3.set_state()
    if 'ch4' in request.form.to_dict():
        ch4.set_state()
    if 'main' in request.form.to_dict():
        general.set_state()


def params_analise():
    params = request.form.to_dict().values()
    if 'ch1v' in request.form.to_dict():
        ch1.set_params(*params)
    if 'ch2v' in request.form.to_dict():
        ch1.set_params(*params)
    if 'ch3v' in request.form.to_dict():
        ch1.set_params(*params)
    if 'ch4v' in request.form.to_dict():
        ch1.set_params(*params)



@app.route("/", methods=['GET', 'POST', 'PUT'])
def index():
    if request.method == 'POST':
        print(request.form.to_dict())
        state_analise()
        params_analise()

    states = {"ch1_state": ch1.switch, "ch2_state": ch2.switch, "ch3_state": ch3.switch, "ch4_state": ch4.switch,
              "out_state": general.switch}
    return render_template('index.html', **states)


if __name__ == "__main__":
    app.run()
