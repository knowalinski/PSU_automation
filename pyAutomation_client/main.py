import json
import time
from threading import Thread
import requests
post_url = "http://127.0.0.1:5000"
get_url = post_url + "/automation"


class Channel:
    def __init__(self, json_data):
        self.json_data = json_data
        self.channel = 0
        self.voltage = 0
        self.current = 0

    def params_response(self):
        self.channel = self.json_data["channel"]
        self.voltage = self.json_data["params"]["voltage"]
        self.current = self.json_data["params"]["current"]
        return {f"ch{self.channel}v": f"{self.voltage}", f"ch{self.channel}a": f"{self.current}"}

    def state_response(self):
        self.channel = self.json_data["channel"]
        return {f"ch{self.channel}": ""}


def poke_server():
    while True:
        requests.post(post_url, data={})
        time.sleep(120)


def data_sender():

    data_check = {}
    while True:
        time.sleep(.1)
        try:
            with open("capl_data.json", "r") as f:
                data = json.load(f)
        except json.decoder.JSONDecodeError:
            pass
        else:
            ch = Channel(data)
            if data_check != data:
                response = requests.get(get_url).json()
                requests.post(post_url, data=ch.params_response())
                if int(response['states'][f"ch{data['channel']}"]) != int(data['state']):
                    # if real state of channel isn't equal to state given from capl change state
                    requests.post(post_url, data=ch.state_response())
                data_check = data


def main():
    poke_thread = Thread(target=poke_server)
    sender_thread = Thread(target=data_sender)
    sender_thread.start()
    poke_thread.start()


if __name__ == "__main__":
    print("i'm alive")
    main()
    # pass
