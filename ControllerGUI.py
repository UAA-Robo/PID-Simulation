import tkinter as tk
from PID import PID
from BangBang import BangBang
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from ControllerValue import ControllerValue

class ControllerGUI:
    def __init__(self, pid: PID, bang_bang: BangBang):
        self.pid = pid
        self.bang_bang = bang_bang

        self.x_time, self.y_process_value1, self.y_process_value2 = [], [], []
        self.MEASUREMENT_PERIOD = 0.2  # Time between "measurements" (seconds)
        self.set_gui_layout()

    def start_gui(self):
        self.gui.after(int(self.MEASUREMENT_PERIOD * 1000), self.update_values_continuously)
        self.gui.mainloop()

    def set_gui_layout(self):
        # GUI
        self.gui = tk.Tk()
        self.gui.geometry("1600x800")
        self.gui.title("Controller Tuner")
        tk.Label(self.gui, text ="Controller GUI").pack()

        self.process_text = self.display_controller_parameter(self.pid.process, HAS_INPUT=False, HAS_BUTTONS=False)
        self.display_controller_parameter(self.pid.setpoint, HAS_BUTTONS=False)
        self.display_controller_parameter(self.pid.P)
        self.display_controller_parameter(self.pid.I)
        self.display_controller_parameter(self.pid.D)

        # Plot
        #self.fig = plt.figure(layout='tight')
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2)
        self.fig.set_figwidth(15)
        self.canvas = FigureCanvasTkAgg(self.fig, master = self.gui) 



    def display_controller_parameter(self, controller_parameter:ControllerValue, HAS_INPUT: bool = True, HAS_BUTTONS: bool = True):
        frame = tk.Frame(self.gui)
        frame.pack()

        name = tk.Label(frame, text = controller_parameter.name)
        value = tk.Label(frame, text = controller_parameter.value, fg="black", bg="yellow")
        name.pack(side=tk.LEFT)
        value.pack(side=tk.LEFT)

        def update_value_text():
            value['text'] = f"{controller_parameter.value:.1f}"
        
        if HAS_BUTTONS:
            increment_button = tk.Button(frame, text = f"+ {controller_parameter.adjust_amount}", 
                                command=lambda:(controller_parameter.increment_value(), update_value_text()))
            decrement_button = tk.Button(frame, text = f"- {controller_parameter.adjust_amount}",
                                command=lambda:(controller_parameter.decrement_value(), update_value_text()))
            
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
        
        """ Update gui text """
        self.process_text['text'] = f"{self.pid.process.value:.1f}"

        """ Get recent process value """
        self.x_time.append(datetime.now()) 
        self.y_process_value1.append(self.pid.process.value)
        self.y_process_value2.append(self.bang_bang.process.value)
        # Limit x and y lists to 200 items
        self.x_time = self.x_time[-200:]
        self.y_process_value1 = self.y_process_value1[-200:]
        self.y_process_value2 = self.y_process_value2[-200:]

        """ Plot data """
        # Draw x and y lists
        self.ax1.clear()
        self.ax1.plot(self.x_time, self.y_process_value1)
        self.ax1.xaxis_date()
        self.ax2.clear()
        self.ax2.plot(self.x_time, self.y_process_value2)
        self.ax2.xaxis_date()
        plt.xticks(rotation=45, ha='right')
        plt.rc('font', **{'size': 6})
        plt.title(self.pid.process.name)
        plt.xlabel('Time')
        plt.ylabel(self.pid.process.name + ' (%)')

        self.canvas.draw()
        self.canvas.get_tk_widget().pack(padx=10, pady=10)

        # ask the mainloop to call this method again in the measurement period
        self.gui.after(int(self.MEASUREMENT_PERIOD * 1000), self.update_values_continuously)




