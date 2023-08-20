from Controller import Controller

class BangBang(Controller):
    """
    @brief   Implements a Bang-bang feedback controller.
    """
    def __init__(self, setpoint:float = 0.0, control_low:float=0.0, control_high:float=100.0):
        super().__init__("Bang Bang", setpoint, control_low, control_high)


    def update_control_value(self, process_value: float, *args) -> float:
        """ Approximation of BangBang to change the control value based on the new value.
        @param process_value    Value that is affected by the control value (what want to reach the 
                                setpoint).
        @return    Control Value which affects the process value. 
        """

        self._process.value = process_value

        if self._process.value < self._setpoint.value:
            self._control.value = self._CONTROL_LOW
        else:
            self._control.value = self._CONTROL_HIGH

        return self._control.value