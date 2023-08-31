import tkinter as tk
import customtkinter as ctk

from GUI.ParameterSpinbox import ParameterSpinbox
from GUI.ParameterDisplay import ParameterDisplay
from GUI.Plot import Plot
from Controllers.Controller import Controller

class ControllerGUI:
    """
    @brief    GUI for graphically viewing changes in process values affected by controller(s) 
              overtime. Allows changing the setpoint and tuning values for the controller. 
    """
    def __init__(self, controllers:list[Controller]):
        """
        @param controllers    List of controllers with parent class Controller to display in 
                              the gui.
        """
        self.controllers = controllers
        self.PLOTTING_PERIOD = 0.2  # Time between plotting points (seconds)
        self.set_gui_layout()

    def start_gui(self) -> None:
        """
        @brief   Should be called to display the GUI popup.
        """
        self.app.mainloop()

    def set_gui_layout(self) -> None:
        """
        @brief   Formats the GUI (text and input) and the Process Value plot.
        """

        # GUI
        self.app = ctk.CTk()
        ctk.set_appearance_mode("dark")

        self.app.title("Controller Tuner")
        self.app.columnconfigure(1, weight=1)
        self.app.rowconfigure(0, weight=1)
        
        dark_color = "#323232"
        
        left_frame = tk.Frame(self.app, bg=dark_color)
        left_frame.grid(row=0, column=0, padx=10, pady=5, sticky=tk.NSEW, )

        right_frame = tk.Frame(self.app, bg=dark_color) 
        right_frame.grid(row=0, column=1, padx=10, pady=5, sticky=tk.NSEW)
        right_frame.grid_columnconfigure((0), weight=1, )
        right_frame.grid_rowconfigure((0), weight=1)

        left_frame_row = self.Counter()
        NUM_COLUMNS = 2

        ctk.CTkLabel(left_frame, text ="Feedback Controller Visualization", corner_radius=5, 
                     font=(None, 20))\
            .grid(row=left_frame_row.count(), column=0, columnspan=NUM_COLUMNS, pady=(40, 0))
        
        ParameterSpinbox(left_frame, [parameter.setpoint for parameter in self.controllers])\
                .grid(row=left_frame_row.count(), column=0, columnspan=NUM_COLUMNS, pady=(40, 0)
                      , sticky=tk.EW)

        for controller in self.controllers:
            ctk.CTkLabel(left_frame, text=controller.controller_name)\
                .grid(row=left_frame_row.count(), column=0, columnspan=NUM_COLUMNS, pady=(40, 0))
            
            
            ParameterDisplay(self.app, left_frame, controller.process)\
                .grid(row=left_frame_row.count(), column=0, columnspan=NUM_COLUMNS)


            for tuning_parameter in controller.tuning_parameters:
                ParameterSpinbox(left_frame, [tuning_parameter])\
                .grid(row=left_frame_row.count(), column= 0, columnspan=NUM_COLUMNS)

            left_frame_row.count()

        Plot(self.app, right_frame, self.controllers)


    class  Counter:
        """
        @brief Keeps tracks of a counter and automatically increments them when they are 
               used. Used for tkinter grid rows/columns
        """
        def __init__(self, is_incrementing: bool = True, initial_count: int = 0):
            self._count = initial_count
            self._IS_INCREMENTING = is_incrementing
        
        def count(self, is_incrementing: bool = None):
            if is_incrementing == None:
                is_incrementing = self._IS_INCREMENTING

            # Emulates incrementing count "after" returning
            if is_incrementing:
                self._count += 1
                return self._count - 1
            
            return self._count



