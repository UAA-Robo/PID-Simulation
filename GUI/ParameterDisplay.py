import customtkinter as ctk 
from Controllers.ControllerParameter import ControllerParameter

class ParameterDisplay(ctk.CTkFrame):
    """
    @brief    Frame to display a Controller Parameter name and value without any buttons/input
              to change it. Updates continuously as the tkinter gui is run.
    """
    def __init__(self, app: ctk.CTk, master:any, controller_parameter: ControllerParameter,
                update_period: float = 0.2):
        """
        @brief    Sets the layout for the frame.
        @param app    Parent widget of entire gui.
        @param master    Parent widget of this frame (usually another frame).
        @param controller_parameter    Controller Parameter to display.
        @param update_period    Number of seconds in between updating the Parameter value in this
                                frame.
        """

        super().__init__(master=master, width=110, height=32)
        self.app = app
        self.controller_parameter = controller_parameter
        self.UPDATE_PERIOD = update_period

        self.configure(fg_color=("gray78", "gray28"),)  # set frame color
        self.label = ctk.CTkLabel(self, text = controller_parameter.name)
        self.label.grid(row=0, column=0, padx=5, pady=3)

        self.value = ctk.CTkLabel(self,text = controller_parameter.value, text_color="black",
                                  fg_color="yellow", corner_radius=5, width=50)
        self.value.grid(row=0, column=1, padx=5, pady=3)

        self.update_value_callback() # Start continuous callback


    def update_value_callback(self):
        """
        @brief    Updates the Parameter value displayed every update_period
        """
        self.value.configure(text=f"{self.controller_parameter.value:.2f}")
        self.app.after(int(self.UPDATE_PERIOD * 1000), self.update_value_callback)


    def grid(self, padx: int = 10, pady: int = 3, **kwargs):
        """
        @brief    Overrides the tkinter grid function to pass default padx and pady vals to it.
        @param padx    Horizontal padding in pixels for this frame.
        @param pady    Vertical padding in pixels for this frame.
        @param **kwargs    Any additional kwargs to pass to tkinter grid function.
        """
        super().grid(padx=padx, pady=pady, **kwargs)