import tkinter as tk
from Controllers.PID import PID
from Controllers.BangBang import BangBang
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from Controllers.ControllerParameter import ControllerParameter

class ControllerGUI:
    """
    @brief    GUI for graphically viewing changes in process values affected by controller(s) 
              overtime. Allows changing the setpoint and tuning values for the controller. 
    """
    def __init__(self, controllers:list ):
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
        self.gui.after(int(self.PLOTTING_PERIOD * 1000), self.update_values_continuously)
        self.gui.mainloop()

    def set_gui_layout(self) -> None:
        """
        @brief   Formats the GUI (text and input) and the Process Value plot.
        """

        # GUI
        self.gui = tk.Tk()
        self.gui.geometry("1600x800")
        self.gui.title("Controller Tuner")
        tk.Label(self.gui, text ="Controller GUI").pack()

        self.process_texts = []
        for controller in self.controllers:
            tk.Label(self.gui, text=controller.controller_name).pack()
            self.process_texts.append(
                self.display_controller_parameter(controller.process, 
                                                  HAS_INPUT=False, HAS_BUTTONS=False))

            self.display_controller_parameter(controller.setpoint, HAS_BUTTONS=False)

            for tuning_parameters in controller.tuning_parameters:
                self.display_controller_parameter(tuning_parameters)

        # Plot
        self.fig = plt.figure(layout='tight')
        self.subplot = self.fig.add_subplot(1, 1, 1)
        self.fig.set_figwidth(15)
        self.canvas = FigureCanvasTkAgg(self.fig, master = self.gui) 



    def display_controller_parameter(self, controller_parameter:ControllerParameter, 
                                     HAS_INPUT: bool = True, HAS_BUTTONS: bool = True) -> None:
        """
        @brief   Formats a "widget" to display the controller parameter value. Updates parameter
                 values based on button/text input.
        @param controller_parameter    Either a process, setpoint, or tuning parameter.
        @param HAS_INPUT    Text input for changing the parameter value is added to the GUI 
                            when True.
        @param HAS_BUTTONS    + and - buttons for changing the parameter value are added to the 
                              GUI when True.
        """
        frame = tk.Frame(self.gui)
        frame.pack()

        name = tk.Label(frame, text = controller_parameter.name)
        value = tk.Label(frame, text = controller_parameter.value, fg="black", bg="yellow")
        name.pack(side=tk.LEFT)
        value.pack(side=tk.LEFT)

        def update_value_text() -> None:
            """
            @brief   Sets the parameters text value based on the latest value in the Controller 
                     Class.
            """
            value['text'] = f"{controller_parameter.value:.1f}"
        
        if HAS_BUTTONS:
            increment_button = tk.Button(frame, text = f"+ {controller_parameter.adjust_amount}", 
                                        command=lambda:(controller_parameter.increment_value(), 
                                                        update_value_text()))
            decrement_button = tk.Button(frame, text = f"- {controller_parameter.adjust_amount}",
                                        command=lambda:(controller_parameter.decrement_value(), 
                                        update_value_text()))
            
            increment_button.pack(side=tk.LEFT)
            decrement_button.pack(side=tk.LEFT)

        if HAS_INPUT:
            input=tk.Entry(frame)

            def input_value(event):
                controller_parameter.value = input.get()
                update_value_text()
                input.delete(0, tk.END) # Clear input after pressing enter

            input.bind('<Return>', func=input_value)  # Update value on return
            input.pack()
        
        return value
        

    def update_values_continuously(self):
        """
        @brief    Updates plot and process value display every PLOTTING_PERIOD to be up to date
                  with the data in the controller classes.
        """
        
        """ Update gui text """
        for controller_process_text, controller in zip(self.process_texts, self.controllers):
            controller_process_text['text'] = f"{controller.process.value:.1f}"


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
        self.canvas.get_tk_widget().pack(padx=10, pady=10)

        # ask the mainloop to call this method again in the measurement period
        self.gui.after(int(self.PLOTTING_PERIOD * 1000), self.update_values_continuously)





