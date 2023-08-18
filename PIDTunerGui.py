import tkinter as tk
from PID import PID
import matplotlib.pyplot as plt
import random
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.animation as animation

class PIDTunerGui:
    def __init__(self, PID: PID):
        self.PID = PID
        self.gui = tk.Tk()
        self.fig = plt.figure()
        self.subplot = self.fig.add_subplot(1, 1, 1)
        self.x_time, self.y_tank_level = [0,1], [30, 40]
        self.canvas = FigureCanvasTkAgg(self.fig, master = self.gui) 
        # Format plot

        self.tank_level = 0.0
        self.MEASUREMENT_PERIOD = 0.2  # Time between "measurements" (seconds)

    def display_PID_parameter(self, PID_parameter, HAS_INPUT: bool = True, HAS_BUTTONS: bool = True):
        frame = tk.Frame(self.gui)
        frame.pack()

        name = tk.Label(frame, text = PID_parameter.name)
        value = tk.Label(frame, text = PID_parameter.value, fg="black", bg="yellow")
        name.pack(side=tk.LEFT)
        value.pack(side=tk.LEFT)

        def update_value_text():
            value['text'] = f"{PID_parameter.value:.1f}"
        
        if HAS_BUTTONS:
            increment_button = tk.Button(frame, text = f"+ {PID_parameter.adjust_amount}", 
                                command=lambda:(PID_parameter.increment_value(), update_value_text()))
            decrement_button = tk.Button(frame, text = f"- {PID_parameter.adjust_amount}",
                                command=lambda:(PID_parameter.decrement_value(), update_value_text()))
            
            increment_button.pack(side=tk.LEFT)
            decrement_button.pack(side=tk.LEFT)

        if HAS_INPUT:
            input=tk.Entry(frame)

            def input_value(event):
                PID_parameter.set_value(input.get())
                update_value_text()
                input.delete(0, tk.END) # Clear input after pressing enter

            input.bind('<Return>', func=input_value)  # Update value on return
            input.pack()
        
        
        


    # This function is called periodically from FuncAnimation
    def animate(self):
        
        input_flow = random.random() * 8 # 0-8 cm^3/sec
        output_flow = self.PID.update_control_value(self.tank_level, self.MEASUREMENT_PERIOD)
        self.tank_level += (input_flow - output_flow) * self.MEASUREMENT_PERIOD

        
        self.x_time.append(datetime.now().strftime('%H:%M:%S.%f'))
        self.y_tank_level.append(self.tank_level)

        # Limit x and y lists to 20 items
        self.x_time = self.x_time[-200:]
        self.y_tank_level = self.y_tank_level[-200:]

        # Draw x and y lists
        self.subplot.clear()
        self.subplot.plot(self.x_time, self.y_tank_level)

        
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

        self.gui.after(int(self.MEASUREMENT_PERIOD * 1000), self.animate)
        #self.after( MEASUREMENT_PERIOD * 1000, self.animate) # ask the mainloop to call this method again in the measurement period



    def set_gui_layout(self):
        
        self.gui.geometry("600x600")

        self.gui.title("PID Tuner")
        tk.Label(self.gui, text ="PID GUI").pack()

        self.display_PID_parameter(self.PID.process, HAS_INPUT=False, HAS_BUTTONS=False)
        self.display_PID_parameter(self.PID.setpoint, HAS_BUTTONS=False)
        self.display_PID_parameter(self.PID.P)
        self.display_PID_parameter(self.PID.I)
        self.display_PID_parameter(self.PID.D)
        
        plt.xticks(rotation=45, ha='right')
        plt.subplots_adjust(bottom=0.30)
        plt.title('Tank Level')
        plt.ylabel('Tank Level (%)')




    def start_gui(self):
        self.set_gui_layout()
        self.gui.after(int(self.MEASUREMENT_PERIOD * 1000), self.animate)
        self.gui.mainloop()


