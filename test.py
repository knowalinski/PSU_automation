import requests
import time

url = "http://127.0.0.1:5000/"

data = {"ch1": ""}
channels = ["ch1", "ch2", "ch3", "ch4", "main"]
# for channel in channels:
#     requests.post(url, data={channel: ""})
#     print(channel)
#     time.sleep(1)

# for i in range(30):
#     requests.post(url, data={"ch1v": i, "ch1a": "1"})
#     time.sleep(5)

for i in range(300):
    requests.post(url, data={"ch1v": i/10, "ch1a": "1"})

