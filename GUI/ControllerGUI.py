import tkinter as tk
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Controllers.ControllerParameter import ControllerParameter
from GUI.ParameterSpinbox import ParameterSpinbox
from GUI.ParameterDisplay import ParameterDisplay

class ControllerGUI:
    """
    @brief    GUI for graphically viewing changes in process values affected by controller(s) 
              overtime. Allows changing the setpoint and tuning values for the controller. 
    """
    def __init__(self, controllers:list):
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
        self.app.after(int(self.PLOTTING_PERIOD * 1000), self.update_values_continuously)
        self.app.mainloop()

    def set_gui_layout(self) -> None:
        """
        @brief   Formats the GUI (text and input) and the Process Value plot.
        """

        # GUI
        self.app = ctk.CTk()  # "1200x600"
        
        self.app.title("Controller Tuner")
        left_frame = tk.Frame(self.app, width=200)
        left_frame.grid(row=0, column=0, padx=10, pady=5, sticky=tk.NSEW)

        right_frame = tk.Frame(self.app, width=300, height=300)
        right_frame.grid(row=0, column=1, padx=10, pady=5)

        left_frame_row = self.Counter()
        NUM_COLUMNS = 5
        tk.Label(left_frame, text ="Controller Visualization")\
            .grid(row=left_frame_row.count(), column=0, columnspan=NUM_COLUMNS)

        for controller in self.controllers:
            tk.Label(left_frame, text=controller.controller_name)\
                .grid(row=left_frame_row.count(), column=0, columnspan=NUM_COLUMNS, pady=(50, 10))
            
            
            ParameterDisplay(self.app, left_frame, controller.process)\
                .grid(row=left_frame_row.count(False), column=0)

            ParameterSpinbox(left_frame, controller.setpoint)\
                .grid(row=left_frame_row.count(), column=1)

            tuner_column = self.Counter()
            for tuning_parameter in controller.tuning_parameters:
                ParameterSpinbox(left_frame, tuning_parameter)\
                .grid(row=left_frame_row.count(False), column=tuner_column.count())

            left_frame_row.count()
 

        # Plot
        self.fig = plt.figure(layout='tight', figsize=(4, 2.5)) 
        self.subplot = self.fig.add_subplot(1, 1, 1)
        self.canvas = FigureCanvasTkAgg(self.fig, master = right_frame) 


    def update_values_continuously(self):
        """
        @brief    Updates plot and process value display every PLOTTING_PERIOD to be up to date
                  with the data in the controller classes.
        """

        """ Plot data """        
        self.subplot.clear()
        for controller in self.controllers:
            self.subplot.plot(controller.process.time_log, controller.process.value_log, 
                              label =controller.controller_name, linestyle="-")
        
        plt.legend()
        plt.xticks(rotation=45, ha='right')
        plt.rc('font', **{'size': 6})
        plt.title("Process")
        plt.xlabel('Time')
        plt.ylabel("Process Value")
        plt.ylim([0, 100])

        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10, sticky=tk.NSEW)

        # ask the mainloop to call this method again in the measurement period
        self.app.after(int(self.PLOTTING_PERIOD * 1000), self.update_values_continuously)


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


