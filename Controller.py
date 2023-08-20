from ControllerValue import ControllerValue

class Controller:
    def __init__(self, controller_name:str, setpoint:float, control_low:float, control_high:float):
        self._CONTROLLER_NAME = controller_name
        self._setpoint = ControllerValue(setpoint, controller_name + " Setpoint", 0.1)
        self._CONTROL_LOW = control_low
        self._CONTROL_HIGH = control_high

        self._process = ControllerValue(0, controller_name + " Process Value")
        self._control = ControllerValue(0, controller_name + " Control Value")
        self._tuning_parameters = []

    @property
    def controller_name(self): return self._CONTROLLER_NAME
    @property
    def setpoint(self): return self._setpoint
    @property
    def process(self): return self._process
    @property
    def control(self): return self._control
    @property
    def tuning_parameters(self): return self._tuning_parameters


    def update_control_value(self, process_value: float, *kwargs) -> float:
        self.control_value = process_value
        return self._control.value