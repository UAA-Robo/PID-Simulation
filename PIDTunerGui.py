import tkinter as tk
from PID import PID
class PIDTunerGui:
    def __init__(self, PID: PID):
        self.PID = PID

    def constant_input(self, name, value):
        frame = tk.Frame(self.gui)
        frame.pack()

        tk.Label(frame, text = name).pack(side=tk.LEFT)
        tk.Label(frame, text = value, fg="black", bg="yellow").pack(side=tk.LEFT)
        
        increment_button = tk.Button(frame, text = "+ 0.1")
        increment_button.pack(side=tk.LEFT)

        decrement_button = tk.Button(frame, text = "- 0.1")
        decrement_button.pack(side=tk.LEFT)

        input=tk.Entry(frame)
        input.pack()


        return ""

    def set_gui_layout(self):
        self.gui = tk.Tk()
        self.gui.geometry("400x400")


        self.gui.title("PID Tuner")
        tk.Label(self.gui, text ="PID GUI").pack()

        # Process
        proccess_frame = tk.Frame(self.gui)
        proccess_frame.pack()
        tk.Label(proccess_frame, text = 'Process Value').pack(side=tk.LEFT)
        tk.Label(proccess_frame, text = self.PID.process_value, fg="black", bg="yellow").pack(side=tk.LEFT)


        # Setpoint
        setpoint_frame = tk.Frame(self.gui)
        setpoint_frame.pack()
        tk.Label(setpoint_frame, text = 'Setpoint Value').pack(side=tk.LEFT)
        tk.Label(setpoint_frame, text = self.PID.setpoint, fg="black", bg="yellow").pack(side=tk.LEFT)
        setpoint_input =tk.Entry(setpoint_frame)
        setpoint_input.pack()


        self.constant_input('P', self.PID.P)
        self.constant_input('I', self.PID.I)
        self.constant_input('D', self.PID.D)
        


        # redbutton = tk.Button(frame, text = 'Red', fg ='red')
        # redbutton.pack(side = tk.LEFT)
        # greenbutton = tk.Button(frame, text = 'Brown', fg='brown')
        # greenbutton.pack(side = tk.LEFT )


    def start_gui(self):
        self.set_gui_layout()
        self.gui.mainloop()


