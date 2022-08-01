from flask import Flask, render_template, request, redirect, url_for, jsonify
from waitress import serve
from termcolor import colored
import serial
import time
from operators.memory import Memory
from operators.device import Device, Channel
from operators.request_handler import RequestHandler, pass_data
import os
os.system('color')
app = Flask(__name__)
# setting up serial connection parameters
ser = serial.Serial()
ser.baudrate = 9600
# ser.baudrate = 19200
while True:
    try:
        ser.port = input("HMP4040 serial port: ").upper()
        ser.open()
    except serial.SerialException:
        print(colored("Wrong port - try again", 'red'))
    else:
        ser.close()
        break

# create objects
memory = Memory("data.json")
ch1 = Channel(1, ser)
ch2 = Channel(2, ser)
ch3 = Channel(3, ser)
ch4 = Channel(4, ser)
general = Device(ser)
channels = {"ch1": ch1, "ch2": ch2, "ch3": ch3, "ch4": ch4, "general": general}
handler = RequestHandler(channels)

# clearing states just in case
memory.clear_states(channels)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print("method: ", colored("POST", "green"), f" on time: {time.ctime()}")
        print(colored(request.form.to_dict(), 'white'))
        # Processing posted data and updating .json file
        handler.state_setter(request.form.to_dict(), memory)
        handler.params_setter(request.form.to_dict(), memory)

        # return below prevents from errors caused by resubmitting form
        return redirect(url_for('index'))
    if request.method == "GET":
        print("method: ", colored("GET", "cyan"), f" on time: {time.ctime()}")
    # return below renders web interface
    return render_template('index.html', **pass_data(memory.data))


@app.route("/automation", methods=['GET', 'POST'])
def automation():
    if request.method == "GET":
        print("method: ", colored("GET", "cyan"), f" on time: {time.ctime()}")
        return jsonify(memory.data)


if __name__ == "__main__":
    # app.run()
    serve(app, host="0.0.0.0", threads=2)
    # app.run(host="0.0.0.0")
    # clearing states when server turned off
    memory.clear_states(channels)
