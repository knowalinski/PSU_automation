from flask import Flask, render_template, request, redirect, url_for, jsonify
from waitress import serve
from termcolor import colored
import serial
import time
from operators.memory import Memory, import_config
from operators.device import Device, Channel
from operators.request_handler import RequestHandler, pass_data
import os

'''This is the server side of PSU automation. It is responsible for generating a webGUI and processing queries into 
commands understood by the PSU (SCPI protocol) '''

# it just makes log window look fancy
os.system('color')

app = Flask(__name__)

# setting up serial connection parameters
serial_params = import_config()
ser = serial.Serial()
ser.baudrate = serial_params[1]
print(serial_params)
while True:
    try:
        ser.port = serial_params[0]
        ser.open()
    except serial.SerialException:
        print(colored("Wrong port - edit config.txt and restart program", 'red'))
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
        print("method: ", colored("[POST]", "green"), f" on time: [{time.ctime()}]")
        print(colored(request.form.to_dict(), 'magenta'))
        # Processing posted data and updating .json file
        handler.state_setter(request.form.to_dict(), memory)
        handler.params_setter(request.form.to_dict(), memory)

        # return below prevents from errors caused by resubmitting form
        return redirect(url_for('index'))
    if request.method == "GET":
        print("method: ", colored("[GET]", "cyan"), f" on time: [{time.ctime()}]")
    # return below renders web interface
    return render_template('index.html', **pass_data(memory.data))


@app.route("/automation", methods=['GET', 'POST'])
def automation():
    # this route is used as a place from which the client downloads data
    if request.method == "GET":
        print("method: ", colored("[GET]", "cyan"), f" on time: [{time.ctime()}]")
        return jsonify(memory.data)


if __name__ == "__main__":
    # waitress server - it works stably unlike the one from Flask
    serve(app, host="0.0.0.0", threads=2)
    # app.run()
    # app.run(host="0.0.0.0")

    # clearing states when server turned off
    memory.clear_states(channels)
