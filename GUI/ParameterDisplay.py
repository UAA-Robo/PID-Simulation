import customtkinter as ctk 
from Controllers.ControllerParameter import ControllerParameter

class ParameterDisplay(ctk.CTkFrame):
    def __init__(self,
                 master:any,
                 controller_parameter: ControllerParameter,
                 width: int = 110,
                 height: int = 32,
                 ):

        super().__init__(master=master, width=width, height=height)
        self.controller_parameter = controller_parameter

        self.configure(fg_color=("gray78", "gray28"),)  # set frame color

        # self.grid_columnconfigure((1, 3), weight=0)  # buttons don't expand
        # self.grid_columnconfigure((0,1), weight=1)  # entry and label expands

        self.label = ctk.CTkLabel(self,text = controller_parameter.name)
        self.label.grid(row=0, column=0, padx=5, pady=3)

        self.value = ctk.CTkLabel(self,text = controller_parameter.value, text_color="black",
                                  fg_color="yellow", corner_radius=5, )
        self.value.grid(row=0, column=1, padx=5, pady=3)
    
    # Function overide for default padx and pady vals
    def grid(self, padx: int = 3, pady: int = 3, **kwargs):
        super().grid(padx=padx, pady=pady, **kwargs)


    def set(self, value: float):
        self.value.delete(0, "end")
        self.value.insert(0, str(float(value)))