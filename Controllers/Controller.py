from Controllers.ControllerParameter import ControllerParameter

class Controller:
    """
    @brief   Parent class of the specific controllers implemented in this program. Contains control
             variables common to all controllers. 
    """
    def __init__(self, controller_name:str, setpoint:float, control_low:float, control_high:float):
        self._CONTROLLER_NAME = controller_name
        self._setpoint = ControllerParameter(setpoint, "Setpoint", 1)
        self._CONTROL_LOW = control_low
        self._CONTROL_HIGH = control_high

        self._process = ControllerParameter(0, "Process Value")
        self._control = ControllerParameter(0, "Control Value")
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


    def update_control_value(self, process_value: float, *args) -> float:
        """
        @brief    Does not change the control value.
        @param process_value    Most recent actual or simulated measurement of the Process Value.
                                Does not affect this controller.
        @param *args    Child Controllers (such as PID) has extra values passed needed to 
                          calculate the control value.
        @return    Returns the previous control value.
        """
        return self._control.value