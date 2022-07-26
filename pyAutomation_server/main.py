# TODO: add CSS to make it more readable
# TODO: refactor code


from flask import Flask, render_template, request
import serial
import time
import json

# creating instance of flask app
app = Flask(__name__)

# defining parameters of serial connection
ser = serial.Serial()
ser.baudrate = 9600
ser.port = "COM4"


class Device:
    def __init__(self, serial_id):
        self.serial_id = serial_id
        self.switch = 0

    def override_switch(self, new_switch):
        self.switch = new_switch

    def switch_state(self):
        return 0 if self.switch == 1 else 1

    def state_command(self):
        self.switch = self.switch_state()
        return f"OUTP:GEN {self.switch}\n"

    def set_state(self):
        self.serial_id.open()
        time.sleep(.015)
        self.serial_id.write(self.state_command().encode())
        time.sleep(.015)
        self.serial_id.close()


class Channel(Device):
    def __init__(self, channel_id, serial_id):
        super().__init__(serial_id)
        self.channel_id = channel_id

    def set_params(self, voltage, current):
        self.serial_id.open()
        time.sleep(.015)
        self.serial_id.write(f"INST:NSEL {self.channel_id}\nAPPL {voltage}, {current}\n".encode())
        time.sleep(.015)
        self.serial_id.close()

    def state_command(self):
        self.switch = self.switch_state()
        return f"INST:NSEL {self.channel_id}\nOUTP:SEL {self.switch}\n"


ch1 = Channel(1, ser)
ch2 = Channel(2, ser)
ch3 = Channel(3, ser)
ch4 = Channel(4, ser)
general = Device(ser)
channels = {"ch1": ch1, "ch2": ch2, "ch3": ch3, "ch4": ch4, "general": general}


with open("data.json", "r") as f:
    data = json.load(f)
    for key in channels:
        channels[key].override_switch(1)
        channels[key].set_state()


def update_state(file, channel, value):
    dat = json.load(file)
    dat["states"][channel] = value
    with open("data.json", "w") as json_file:
        json.dump(dat, json_file, indent=4, sort_keys=True)


def state_analise(file):
    if 'ch1' in request.form.to_dict():
        ch1.set_state()
        update_state(file, "ch1", ch1.switch)
    if 'ch2' in request.form.to_dict():
        ch2.set_state()
        update_state(file, "ch2", ch2.switch)
    if 'ch3' in request.form.to_dict():
        ch3.set_state()
        update_state(file, "ch3", ch3.switch)
    if 'ch4' in request.form.to_dict():
        ch4.set_state()
        update_state(file, "ch4", ch4.switch)
    if 'main' in request.form.to_dict():
        general.set_state()
        update_state(file, "general", general.switch)


def update_params(file, channel, voltage, current):
    dat = json.load(file)
    dat["params"][channel]["voltage"] = voltage
    dat["params"][channel]["current"] = current
    with open("data.json", "w") as json_file:
        json.dump(dat, json_file, indent=4, sort_keys=True)


def params_analise(file):
    params = request.form.to_dict().values()
    if 'ch1v' in request.form.to_dict():
        ch1.set_params(*params)
        update_params(file, "ch1", *params)
    if 'ch2v' in request.form.to_dict():
        ch2.set_params(*params)
        update_params(file, "ch2", *params)
    if 'ch3v' in request.form.to_dict():
        ch3.set_params(*params)
        update_params(file, "ch3", *params)
    if 'ch4v' in request.form.to_dict():
        ch4.set_params(*params)
        update_params(file, "ch4", *params)


@app.route("/", methods=['GET', 'POST', 'PUT'])
def index():
    if request.method == 'POST':
        print(request.form.to_dict())
        with open("data.json", "r") as file:
            state_analise(file)
            params_analise(file)
    with open("data.json", "r") as file:
        data = json.load(file)
    states = {
        "ch1_state": data["states"]["ch1"],
        "ch2_state": data["states"]["ch2"],
        "ch3_state": data["states"]["ch3"],
        "ch4_state": data["states"]["ch4"],
        "out_state": data["states"]["general"],
        "CH1V": data["params"]["ch1"]["voltage"],
        "CH1A": data["params"]["ch1"]["current"],
        "CH2V": data["params"]["ch2"]["voltage"],
        "CH2A": data["params"]["ch2"]["current"],
        "CH3V": data["params"]["ch3"]["voltage"],
        "CH3A": data["params"]["ch3"]["current"],
        "CH4V": data["params"]["ch4"]["voltage"],
        "CH4A": data["params"]["ch4"]["current"]}
    return render_template('index.html', **states, )


if __name__ == "__main__":
    app.run()
    # app.run(host="0.0.0.0")
