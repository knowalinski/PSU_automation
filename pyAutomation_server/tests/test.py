import requests
import time
import json

post_url = "http://127.0.0.1:5000"
get_url = post_url + "/automation"

data_check = {}


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


while True:
    time.sleep(.001)
    try:
        with open("tests/capl_data.json", "r") as f:
            data = json.load(f)
    except json.decoder.JSONDecodeError:
        pass
    else:
        ch = Channel(data)
        if data_check != data:
            response = requests.get(get_url).json()
            requests.post(post_url, data=ch.params_response())
            if response['states'][f"ch{ch.channel}"] == 0:
                requests.post(post_url, data=ch.state_response())
        data_check = data

# while True:
#     time.sleep(.001)
#     try:
#         with open("tests/capl_data.json", "r") as f:
#             data = json.load(f)
#     except json.decoder.JSONDecodeError:
#         pass
#     else:
#         if data_check != data:
#             response = requests.get(url).json()
#             # response = response.text
#             # print(response)
#             # print(type(response))
#             if response['states'][f"ch{data['channel']}"] == 1:
#                 requests.post(url, data = {f"ch{data['channel']}":""})

# while True:
#     time.sleep(.0001)
#     try:
#         with open("tests/capl_data.json", "r") as f:
#             data = json.load(f)
#     except json.decoder.JSONDecodeError:
#         pass
#     else:
#         if data_check != data:
#             data_check = data
#             requests.post(url, data=data_check["state"])
#             time.sleep(.01)
#             requests.post(url, data=data_check["params"])
#             time.sleep(.01)
