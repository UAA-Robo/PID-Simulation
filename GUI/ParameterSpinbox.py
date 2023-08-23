import tkinter as tk 
import customtkinter as ctk 
from Controllers.ControllerParameter import ControllerParameter

class ParameterSpinbox(ctk.CTkFrame):
    """
    @brief    Frame to display a Controller Parameter name and value with increment/decrement
              buttons and a input entry to change it. Only updates value being displayed when a 
              button or input is used. 
    """

    def __init__(self, master:any, controller_parameter: ControllerParameter):
        """
        @brief    Sets the layout for the frame
        @param master    Parent widget of this frame (usually another frame).
        @param controller_parameter    Controller Parameter to display.
        """
        width, height = 100, 32
        super().__init__(master=master, width=width, height=height)
        self.controller_parameter = controller_parameter

        self.configure(fg_color=("gray78", "gray28"),)  # Set frame color

        # Label column expands to push buttons to the right
        self.grid_columnconfigure((0), weight=1)  

        self.label = ctk.CTkLabel(self,text = controller_parameter.name)
        self.label.grid(row=0, column=0, padx=5, pady=3, sticky=tk.EW)

        self.subtract_button = ctk.CTkButton(self, text="-", width=height-6, height=height-6,
                                                       command=self.subtract_button_callback)
        self.subtract_button.grid(row=0, column=1, padx=(3, 0), pady=3)

        self.entry = ctk.CTkEntry(self, width=width-(1.5 *height), height=height-6, border_width=0)
        self.entry.grid(row=0, column=2, padx=3, pady=3) 

        # Update value on when return key is pressed
        self.entry.bind('<Return>', command=self.update_entry_callback)  
        self.entry.insert(0, self.controller_parameter.value) # Default value

        self.add_button = ctk.CTkButton(self, text="+", width=height-6, height=height-6,
                                                  command=self.add_button_callback)
        self.add_button.grid(row=0, column=3, padx=(0, 3), pady=3)



    def update_entry_callback(self, event):
        """
        @brief    Updates the Parameter Value in the ControllerParameter class when input is
                  entered and displays it in the frame  
        """
        self.controller_parameter.value = self.entry.get()

            
    def add_button_callback(self):
        """
        @brief    Increments the Parameter Value in the ControllerParameter class when + button is 
                  pressed and displays it in the frame.
        """
        try:
            self.controller_parameter.value += self.controller_parameter.adjust_amount
            self.entry.delete(0, "end")
            self.entry.insert(0, f"{self.controller_parameter.value:.2f}")
        except ValueError:
            return

    def subtract_button_callback(self):
        """
        @brief    Increments the Parameter Value in the ControllerParameter class when - button is 
                  pressed and displays it in the frame.
        """
        try:
            self.controller_parameter.value -= self.controller_parameter.adjust_amount
            self.entry.delete(0, "end")
            self.entry.insert(0, f"{self.controller_parameter.value:.2f}")
        except ValueError:
            return
    
    # Function overide for default padx and pady vals
    def grid(self, padx: int = 10, pady: int = 3, sticky:str = tk.EW,**kwargs):
        """
        @brief    Overrides the tkinter grid function to pass default padx and pady vals to it.
        @param padx    Horizontal padding in pixels for this frame.
        @param pady    Vertical padding in pixels for this frame.
        @param **kwargs    Any additional kwargs to pass to tkinter grid function.
        """
        super().grid(padx=padx, pady=pady, sticky=sticky, **kwargs)
