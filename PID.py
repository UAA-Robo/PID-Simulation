from ControllerValue import ControllerValue 

class PID:

    def __init__(self, setpoint:float = 0.0, P: float = 0.0, I: float = 0,  D: float = 0.0):
        
        self._setpoint = ControllerValue(setpoint, "Setpoint", 0.1)
        self._P = ControllerValue(P, "P", 0.1)
        self._I = ControllerValue(I, "I", 0.1)
        self._D = ControllerValue(D, "D", 0.1)
        self._process = ControllerValue(0, "PID Process Value")
        self._control = ControllerValue(0, "PID Control Value")

        self._integral = 0.0
        self._previous_error = 0.0
    
    @property
    def setpoint(self): return self._setpoint
    @property
    def P(self): return self._P
    @property
    def I(self): return self._I
    @property
    def D(self): return self._D
    @property
    def process(self): return self._process
    @property
    def control(self): return self._control


    def update_values(self, setpoint:float = None, P: float = None, I: float = None,  
                        D: float = None) -> None:
        """ Sets PID constants.  
        @param setpoint    Value that you want the PID to try to reach
        @param P:   Proportional constant (how much change needed to reach setpoint)
        @param I:   Integral constant (how much to deviate from current val)
        @param D:   Derivative constant (how fast to reach setpoint)
        """
        if setpoint:
            self.setpoint.value = setpoint
        if P:
            self._P.set_value(P)
        if I:
            self._I.set_value(I)
        if D:
            self._D.set_value(D)


    def update_control_value(self, process_value: float, change_in_time: float) -> float:
        """ Approximation of PID to change the control value based on the new value.
        @param process_value    Value is affected by the control value (what want to reach the 
                                setpoint).
        @param change_in_time    Time since last measurement in seconds.
        @return    Control value which affects the process value. 
        """

        # Variables that don't have to be kept over time are not stored in the class
        self._process.value = process_value

        error = self._process.value - self._setpoint.value
        derivative = (error - self._previous_error) / change_in_time
        self._integral += error  * change_in_time

        self._previous_error = error

        self._control.value = (self._P.value * error + self._I.value * self._integral
            + self._D.value * derivative)

        return self._control.value