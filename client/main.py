import json
import time
from threading import Thread
import requests

'''The purpose of this program is to connect CANoe to the server that controls PSU'''

# loading url of service from separate file - allows user to edit configuration
with open("config.txt", "r") as file:
    config = json.load(file)
post_url = config["url"]
get_url = post_url + "/automation"

# loading previous dataset from file - prevents from unintentional state changing after reset
with open("capl_input.txt", "r") as file:
    init_data = json.load(file)
    data_check = init_data


class Channel:
    def __init__(self, json_data):
        self.json_data = json_data
        self.channel = 0
        self.voltage = 0
        self.current = 0

    def params_request(self):
        # create server request for setting up selected channel parameters
        self.channel = self.json_data["channel"]
        self.voltage = self.json_data["params"]["voltage"]
        self.current = self.json_data["params"]["current"]
        return {f"ch{self.channel}v": f"{self.voltage}", f"ch{self.channel}a": f"{self.current}"}

    def state_request(self):
        # create server request for changing state of selected channel
        self.channel = self.json_data["channel"]
        return {f"ch{self.channel}": ""}


def poke_server():
    # this function is for generating fake traffic. It prevents server from timing out.
    while True:
        requests.post(post_url, data={})
        print("Server poked")
        time.sleep(300)


def data_sender():
    global data_check

    while True:
        # sleep() below prevents script from generating significant CPU load
        time.sleep(.01)
        try:
            with open("capl_input.txt", "r") as f:
                data = json.load(f)
        except json.decoder.JSONDecodeError:
            pass
        else:
            ch = Channel(data)
            if data_check != data:
                response = requests.get(get_url).json()
                print(f"Params sent: {ch.params_request()}")
                requests.post(post_url, data=ch.params_request())
                if int(response['states'][f"ch{data['channel']}"]) != int(data['state']):
                    # if real state of channel isn't equal to state given from capl - change state
                    print(f"Status sent: {ch.state_request()}")
                    requests.post(post_url, data=ch.state_request())
                data_check = data


def main():
    # creating threads allows to run data_sender() and poke_server() in the same script
    poke_thread = Thread(target=poke_server)
    sender_thread = Thread(target=data_sender)
    sender_thread.start()
    poke_thread.start()


if __name__ == "__main__":
    main()
