def pass_data(data):
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
    return states


class RequestHandler:
    def __init__(self, channels):
        self.channels = list(channels.values())

    def state_setter(self, requested, memory):
        if 'ch1' in requested:
            self.channels[0].set_state()
            memory.update_states("ch1", self.channels[0].switch)
        if 'ch2' in requested:
            self.channels[1].set_state()
            memory.update_states("ch2", self.channels[1].switch)
        if 'ch3' in requested:
            self.channels[2].set_state()
            memory.update_states("ch3", self.channels[2].switch)
        if 'ch4' in requested:
            self.channels[3].set_state()
            memory.update_states("ch4", self.channels[3].switch)
        if 'main' in requested:
            self.channels[4].set_state()
            memory.update_states("general", self.channels[4].switch)

    def params_setter(self, requested, memory):
        params = requested.values()
        if 'ch1v' in requested:
            self.channels[0].set_params(*params)
            memory.update_params("ch1", *params)
        if 'ch2v' in requested:
            self.channels[1].set_params(*params)
            memory.update_params("ch2", *params)
        if 'ch3v' in requested:
            self.channels[2].set_params(*params)
            memory.update_params("ch3", *params)
        if 'ch4v' in requested:
            self.channels[3].set_params(*params)
            memory.update_params("ch4", *params)
