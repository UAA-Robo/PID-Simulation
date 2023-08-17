
class PID:

    def __init__(self, setpoint:float = 0.0, P: float = 0.0, I: float = 0,  D: float = 0.0):
        
        self.setpoint = setpoint
        self.P = P
        self.I = I
        self.D = D

        self.integral = 0.0
        self.previous_error = 0.0
        self.process_value = 0.0


    def update_constants(self, setpoint:float = None, P: float = None, I: float = None,  
                        D: float = None) -> None:
        """ Sets PID constants.  
        @param setpoint    Value that you want the PID to try to reach
        @param P:   Proportional constant (how much change needed to reach setpoint)
        @param I:   Integral constant (how much to deviate from current val)
        @param D:   Derivative constant (how fast to reach setpoint)
        """
        if setpoint:
            self.setpoint = setpoint
        if P:
            self.P = P
        if I:
            self.I = I
        if D:
            self.D = D


    def update_control_value(self, process_value: float, change_in_time: float) -> float:
        """ Approximation of PID to change the control value based on the new value.
        @param process_value    Value is affected by the control value (what want to reach the 
                                setpoint).
        @param change_in_time    Time since last measurement.
        @return    Control value which affects the process value. 
        """

        
        self.process_value = process_value

        self.error = process_value - self.setpoint
        self.derivative = (self.error - self.previous_error) / change_in_time
        self.integral += self.error  * change_in_time

        self.previous_error = self.error

        self.control_value = self.P * self.error + self.I * self.integral + self.D * self.derivative

        return self.control_value