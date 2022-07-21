from flask import Flask, render_template, Response, request
import serial
import time

serialcom = serial.Serial('COM3', 19200, timeout=1)

app = Flask(__name__)


def ledOn():
    serialcom.write(str('twuj stary').encode())


def ledOff():
    serialcom.write(str('myje gary').encode())


def disconnect():
    serialcom.close()


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'on' in request.form.to_dict():
            ledOn()
        if 'off' in request.form.to_dict():
            ledOff()
        if 'dis' in request.form.to_dict():
            disconnect()
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0")
