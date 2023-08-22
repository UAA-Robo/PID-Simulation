import customtkinter as ctk 
from Controllers.ControllerParameter import ControllerParameter

class ParameterSpinbox(ctk.CTkFrame):
    def __init__(self,
                 master:any,
                 controller_parameter: ControllerParameter,
                 width: int = 110,
                 height: int = 32,
                 ):

        super().__init__(master=master, width=width, height=height)
        self.controller_parameter = controller_parameter

        self.configure(fg_color=("gray78", "gray28"),)  # set frame color

        self.grid_columnconfigure((1, 3), weight=0)  # buttons don't expand
        self.grid_columnconfigure((0,1), weight=1)  # entry and label expands

        self.label = ctk.CTkLabel(self,text = controller_parameter.name)
        self.label.grid(row=0, column=0, padx=5, pady=3)

        self.subtract_button = ctk.CTkButton(self, text="-", width=height-6, height=height-6,
                                                       command=self.subtract_button_callback)
        self.subtract_button.grid(row=0, column=1, padx=(3, 0), pady=3)

        self.entry = ctk.CTkEntry(self, width=width-(2*height), height=height-6, border_width=0)
        self.entry.grid(row=0, column=2, columnspan=1, padx=3, pady=3, sticky="ew")
        self.entry.bind('<Return>', command=self.update_entry_callback)  # Update value on return
        self.entry.insert(0, self.controller_parameter.value) # default value

        self.add_button = ctk.CTkButton(self, text="+", width=height-6, height=height-6,
                                                  command=self.add_button_callback)
        self.add_button.grid(row=0, column=3, padx=(0, 3), pady=3)



    def update_entry_callback(self, event):
        self.controller_parameter.value = self.entry.get()

            
    def add_button_callback(self):
        try:
            value = float(self.entry.get()) + self.controller_parameter.adjust_amount
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return

    def subtract_button_callback(self):
        try:
            value = float(self.entry.get()) - self.controller_parameter.adjust_amount
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return
    
    # Function overide for default padx and pady vals
    def grid(self, padx: int = 3, pady: int = 3, **kwargs):
        super().grid(padx=padx, pady=pady, **kwargs)
