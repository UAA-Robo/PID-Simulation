from Controller import Controller
from ControllerValue import ControllerValue 

class BangBang(Controller):
    def __init__(self, setpoint:float = 0.0, control_low:float=0.0, control_high:float=100.0):
        super().__init__("Bang Bang", setpoint, control_low, control_high)


    def update_control_value(self, process_value: float, *args) -> float:
        """ Approximation of BangBang to change the control value based on the new value.
        @param process_value    Value is affected by the control value (what want to reach the 
                                setpoint).
        @param time_period    NOT used, only included so this function can be called like the
                              PID function (should really be child class of a controller class)

        @return    Control value which affects the process value. 
        """

        self._process.value = process_value

        if self._process.value < self._setpoint.value:
            self._control.value = self._CONTROL_LOW
        else:
            self._control.value = self._CONTROL_HIGH

        return self._control.value