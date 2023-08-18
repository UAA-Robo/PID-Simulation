import tkinter as tk
from PID import PID
class PIDTunerGui:
    def __init__(self, PID: PID):
        self.PID = PID

    def display_PID_parameter(self, PID_parameter, HAS_INPUT: bool = True, HAS_BUTTONS: bool = True):
        frame = tk.Frame(self.gui)
        frame.pack()

        name = tk.Label(frame, text = PID_parameter.name)
        value = tk.Label(frame, text = PID_parameter.value, fg="black", bg="yellow")
        name.pack(side=tk.LEFT)
        value.pack(side=tk.LEFT)

        
        if HAS_BUTTONS:
            def update_value_text():
                value['text'] = f"{PID_parameter.value:.1f}"
            increment_button = tk.Button(frame, text = f"+ {PID_parameter.adjust_amount}", 
                                command=lambda:(PID_parameter.increment_value(), update_value_text()))
            decrement_button = tk.Button(frame, text = f"- {PID_parameter.adjust_amount}",
                                command=lambda:(PID_parameter.decrement_value(), update_value_text()))
            
            increment_button.pack(side=tk.LEFT)
            decrement_button.pack(side=tk.LEFT)

        if HAS_INPUT:
            input=tk.Entry(frame)
            input.pack()


    def set_gui_layout(self):
        self.gui = tk.Tk()
        self.gui.geometry("400x400")


        self.gui.title("PID Tuner")
        tk.Label(self.gui, text ="PID GUI").pack()

        # # Process
        # process_frame = tk.Frame(self.gui)
        # process_frame.pack()
        # tk.Label(process_frame, text = 'Process Value').pack(side=tk.LEFT)
        # tk.Label(process_frame, text = self.PID.process.value, fg="black", bg="yellow")\
        #     .pack(side=tk.LEFT)


        # # Setpoint
        # setpoint_frame = tk.Frame(self.gui)
        # setpoint_frame.pack()
        # tk.Label(setpoint_frame, text = self.PID.setpoint.name).pack(side=tk.LEFT)
        # tk.Label(setpoint_frame, text = self.PID.setpoint.value, fg="black", bg="yellow")\
        #     .pack(side=tk.LEFT)
        # setpoint_input =tk.Entry(setpoint_frame)
        # setpoint_input.pack()

        self.display_PID_parameter(self.PID.process, HAS_INPUT=False, HAS_BUTTONS=False)
        self.display_PID_parameter(self.PID.setpoint, HAS_BUTTONS=False)
        self.display_PID_parameter(self.PID.P)
        self.display_PID_parameter(self.PID.I)
        self.display_PID_parameter(self.PID.D)
        


        # redbutton = tk.Button(frame, text = 'Red', fg ='red')
        # redbutton.pack(side = tk.LEFT)
        # greenbutton = tk.Button(frame, text = 'Brown', fg='brown')
        # greenbutton.pack(side = tk.LEFT )


    def start_gui(self):
        self.set_gui_layout()
        self.gui.mainloop()


