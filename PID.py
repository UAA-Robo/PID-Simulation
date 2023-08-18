class PIDValue:
    def __init__(self, value: float, name: str, adjust_amount: float = None):
        self.value = value
        self.name = name
        self.adjust_amount = adjust_amount

    def increment_value(self):
        if not self.adjust_amount:
            return
        self.value += self.adjust_amount
        print("increment", self.name, self.value)

    def decrement_value(self):
        if not self.adjust_amount:
            return
        self.value -= self.adjust_amount
        print("decrement", self.name, self.value)


class PID:

    def __init__(self, setpoint:float = 0.0, P: float = 0.0, I: float = 0,  D: float = 0.0):
        
        self.setpoint = PIDValue(setpoint, "Setpoint", 0.1)
        self.P = PIDValue(P, "P", 0.1)
        self.I = PIDValue(I, "I", 0.1)
        self.D = PIDValue(D, "D", 0.1)
        self.process = PIDValue(0, "Process Value")
        self.control = PIDValue(0, "Control Value")

        self.integral = 0.0
        self.previous_error = 0.0
    


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
            self.P.value = P
        if I:
            self.I.value = I
        if D:
            self.D.value = D


    def update_control_value(self, process_value: float, change_in_time: float) -> float:
        """ Approximation of PID to change the control value based on the new value.
        @param process_value    Value is affected by the control value (what want to reach the 
                                setpoint).
        @param change_in_time    Time since last measurement.
        @return    Control value which affects the process value. 
        """

        # Variables that don't have to be kept over time are not stored in the class
        self.process.value = process_value

        error = self.process.value - self.setpoint.value
        derivative = (error - self.previous_error) / change_in_time
        self.integral += error  * change_in_time

        self.previous_error = error

        self.control.value = self.P.value * error + self.I.value * self.integral\
            + self.D.value * derivative

        return self.control.value