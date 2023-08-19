class noPID:
    class PIDValue:
        def __init__(self, value: float, name: str, adjust_amount: float = None):
            self._value = value
            self._name = name
            self._adjust_amount = adjust_amount

        def increment_value(self) -> None:
            if not self._adjust_amount:
                return
            self._value += self._adjust_amount

        def decrement_value(self) -> None:
            if not self._adjust_amount:
                return
            self._value -= self._adjust_amount
        
        # Getters
        def value(self) -> float: return self._value
        def name(self) -> float: return self._name
        def adjust_amount(self) -> float: return self._adjust_amount

        # Setters
        def set_value(self, value:float) -> None: 
            self._value = float(value)
        def set_adjust_amount(self, adjust_amount:float) -> None: 
            self._adjust_amount = float(adjust_amount)



    def __init__(self, setpoint:float = 0.0, P: float = 0.0, I: float = 0,  D: float = 0.0):
        
        self._setpoint = self.PIDValue(setpoint, "Setpoint", 0.1)
        self._P = self.PIDValue(P, "P", 0.1)
        self._I = self.PIDValue(I, "I", 0.1)
        self._D = self.PIDValue(D, "D", 0.1)
        self._process = self.PIDValue(0, "Process Value")
        self._control = self.PIDValue(0, "Control Value")

        self._integral = 0.0
        self._previous_error = 0.0
    
    # Getters
    def setpoint(self) -> PIDValue: return self._setpoint
    def P(self) -> PIDValue: return self._P
    def I(self) -> PIDValue: return self._I
    def D(self) -> PIDValue: return self._D
    def process(self) -> PIDValue: return self._process
    def control(self) -> PIDValue: return self._control

    def previous_error(self) -> PIDValue: return self._previous_error

    
    
    # def get_P(self):
    #     return self._P

    # def update_values(self, setpoint:float = None, P: float = None, I: float = None,  
    #                     D: float = None) -> None:
    #     """ Sets PID constants.  
    #     @param setpoint    Value that you want the PID to try to reach
    #     @param P:   Proportional constant (how much change needed to reach setpoint)
    #     @param I:   Integral constant (how much to deviate from current val)
    #     @param D:   Derivative constant (how fast to reach setpoint)
    #     """
    #     if setpoint:
    #         self.setpoint.value = setpoint
    #     if P:
    #         self._P.set_value(P)
    #     if I:
    #         self._I.set_value(I)
    #     if D:
    #         self._D.set_value(D)


    def update_control_value(self, process_value: float, change_in_time: float) -> float:
        """ Approximation of PID to change the control value based on the new value.
        @param process_value    Value is affected by the control value (what want to reach the 
                                setpoint).
        @param change_in_time    Time since last measurement in seconds.
        @return    Control value which affects the process value. 
        """

        # Variables that don't have to be kept over time are not stored in the class
        self._process.set_value(process_value)

        #if tank level below setpoint, control value max
        #elif tank level above setpoint, control value min
        if self._process.value() < self._setpoint.value():
            self._control.set_value(0)
        elif self._process.value() >= self._setpoint.value():
            self._control.set_value(20)

        # error = self._process.value() - self._setpoint.value()
        # derivative = (error - self._previous_error) / change_in_time
        # self._integral += error  * change_in_time

        # self._previous_error = error

        # self._control.set_value(self._P.value() * error + self._I.value() * self._integral
        #     + self._D.value() * derivative)

        return self._control.value()