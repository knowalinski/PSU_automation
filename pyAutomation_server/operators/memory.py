import json
from termcolor import colored


class Memory:
    def __init__(self, file_name):
        self.file_name = file_name
        with open(self.file_name, "r") as f:
            self.data = json.load(f)

    def get_data(self):
        # updating self.data dictionary with .json file
        with open(self.file_name, "r") as f:
            self.data = json.load(f)

    def update(self):
        # updating .json file with self.data dictionary
        with open(self.file_name, "w") as f:
            json.dump(self.data, f, indent=4, sort_keys=True)

    def _get_update(body):
        def wrapper(self, *arg, **kw):
            self.get_data()
            body(self, *arg, **kw)
            self.update()
        return wrapper

    @_get_update
    def update_states(self, channel, value):
        # updating info about states of PSU outputs
        self.data["states"][channel] = value

    @_get_update
    def update_params(self, channel, voltage, current):
        # updating info about parameters of PSU outputs
        self.data["params"][channel]["voltage"] = voltage
        self.data["params"][channel]["current"] = current

    @_get_update
    def clear_states(self, channels):
        for key in channels:
            channels[key].override_switch(1)
            channels[key].set_state()
            self.data["states"][key] = 0
        print(colored("\n STATES CLEARED \n\n",'green', attrs=['reverse']))
