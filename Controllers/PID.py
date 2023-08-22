from Controllers.Controller import Controller
from Controllers.ControllerParameter import ControllerParameter 

class PID(Controller):
    """
    @brief   Implements a PID feedback controller.
    """
    def __init__(self, setpoint:float = 0.0, control_low:float=0.0, control_high:float=100.0, 
                 P: float = 0.0, I: float = 0,  D: float = 0.0):
        super().__init__("PID", setpoint, control_low, control_high)

        self._P = ControllerParameter(P, "Proportion", 0.1)
        self._I = ControllerParameter(I, "Integral", 0.1)
        self._D = ControllerParameter(D, "Derivate", 0.1)
        self._tuning_parameters = [self._P, self._I, self._D]

        # Variables that affect the PID over time
        self._integral = 0.0
        self._previous_error = 0.0
    
    @property
    def P(self): return self._P
    @property
    def I(self): return self._I
    @property
    def D(self): return self._D


    def update_control_value(self, process_value: float, change_in_time: float) -> float:
        """ Approximation of PID to change the control value based on the new value.
        @param process_value    Value is affected by the control value (what want to reach the 
                                setpoint).
        @param change_in_time    Time since last measurement in seconds.
        @return    Control value which affects the process value. 
        """

        self._process.value = process_value

        error = self._process.value - self._setpoint.value
        derivative = (error - self._previous_error) / change_in_time
        self._integral += error  * change_in_time

        self._previous_error = error

        self._control.value = (self._P.value * error + self._I.value * self._integral
            + self._D.value * derivative)

        return self._control.value