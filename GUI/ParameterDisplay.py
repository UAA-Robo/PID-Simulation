import customtkinter as ctk 
from Controllers.ControllerParameter import ControllerParameter

class ParameterDisplay(ctk.CTkFrame):
    def __init__(self,
                 app: ctk.CTk, # TODO: see if need this!
                 master:any,
                 controller_parameter: ControllerParameter,
                 update_period: float = 0.2,  # second
                 width: int = 110,
                 height: int = 32,
                 ):

        super().__init__(master=master, width=width, height=height)

        self.app = app
        self.controller_parameter = controller_parameter
        self.UPDATE_PERIOD = update_period
        self.configure(fg_color=("gray78", "gray28"),)  # set frame color

        self.grid_columnconfigure((1), weight=0)  # Value text doesn't expand
        # self.grid_columnconfigure((0,1), weight=1)  # entry and label expands

        self.label = ctk.CTkLabel(self, text = controller_parameter.name)
        self.label.grid(row=0, column=0, padx=5, pady=3)

        self.value = ctk.CTkLabel(self,text = controller_parameter.value, text_color="black",
                                  fg_color="yellow", corner_radius=5, width=50)
        self.value.grid(row=0, column=1, padx=5, pady=3)

        self.update_value_callback() # Start continuos callback
    
    # Function override for default padx and pady vals
    def grid(self, padx: int = 10, pady: int = 3, **kwargs):
        super().grid(padx=padx, pady=pady, **kwargs)


    def update_value_callback(self):
        self.value.configure(text=f"{self.controller_parameter.value:.2f}")
        self.app.after(int(self.UPDATE_PERIOD * 1000), self.update_value_callback)