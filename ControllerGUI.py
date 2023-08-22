import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Controllers.ControllerParameter import ControllerParameter

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
        self.gui.after(int(self.PLOTTING_PERIOD * 1000), self.update_values_continuously)
        self.gui.mainloop()

    def set_gui_layout(self) -> None:
        """
        @brief   Formats the GUI (text and input) and the Process Value plot.
        """

        # GUI
        self.gui = tk.Tk("1200x600")
        
        self.gui.title("Controller Tuner")
        left_frame = tk.Frame(self.gui, width=200)
        left_frame.grid(row=0, column=0, padx=10, pady=5, sticky=tk.NSEW)

        right_frame = tk.Frame(self.gui, width=300, height=300)
        right_frame.grid(row=0, column=1, padx=10, pady=5)

        left_frame_row = self.Counter()
        NUM_COLUMNS = 5
        tk.Label(left_frame, text ="Controller Visualization")\
            .grid(row=left_frame_row.count, column=0, columnspan=NUM_COLUMNS)

        self.process_texts = []
        for controller in self.controllers:
            tk.Label(left_frame, text=controller.controller_name)\
                .grid(row=left_frame_row.count, column=0, columnspan=NUM_COLUMNS, pady=(50, 10))
            self.process_texts.append(
                self.display_controller_parameter(left_frame, left_frame_row.count, 0, controller.process, 
                                                  HAS_INPUT=False, HAS_BUTTONS=False))

            self.display_controller_parameter(left_frame, left_frame_row.count, 0, controller.setpoint, HAS_BUTTONS=False)

            for tuning_parameters in controller.tuning_parameters:
                self.display_controller_parameter(left_frame, left_frame_row.count, 0, tuning_parameters)
 

        # Plot
        self.fig = plt.figure(layout='tight', figsize=(4, 2.5)) 
        self.subplot = self.fig.add_subplot(1, 1, 1)
        self.canvas = FigureCanvasTkAgg(self.fig, master = right_frame) 



    def display_controller_parameter(self, frame:tk.Frame, row:int, column:int, 
                                    controller_parameter:ControllerParameter, 
                                    HAS_INPUT: bool = True, HAS_BUTTONS: bool = True) -> None:
        """
        @brief   Formats a "widget" to display the controller parameter value. Updates parameter
                 values based on button/text input.
        @param frame    Frame to set widget in.
        @param row     Row in frame grid to place widget.
        @param column     Column in frame grid to place widget.
        @param controller_parameter    Either a process, setpoint, or tuning parameter.
        @param HAS_INPUT    Text input for changing the parameter value is added to the GUI 
                            when True.
        @param HAS_BUTTONS    + and - buttons for changing the parameter value are added to the 
                              GUI when True.
        """
        
        row = self.Counter(initial_count=row, is_incrementing=False)
        column = self.Counter()

        name = tk.Label(frame, text = controller_parameter.name, wraplength=200)
        name.grid(row=row.count, column=column.count, sticky=tk.E, padx=(0, 10))

        column_span = 1 if HAS_INPUT or HAS_BUTTONS else 5

        value = tk.Label(frame, text = controller_parameter.value, fg="black", bg="yellow", width=5)
        value.grid(row=row.count, column=column.count, padx=10, columnspan=column_span, sticky=tk.EW)


        def update_value_text() -> None:
            """
            @brief   Sets the parameters text value based on the latest value in the Controller 
                     Class.
            """
            value['text'] = f"{controller_parameter.value:.1f}"
    
        
        if HAS_INPUT:
            width = 5 if HAS_BUTTONS else 13
            if HAS_BUTTONS: width = 5   
            input=tk.Entry(frame, width=width)

            def input_value(event):
                controller_parameter.value = input.get()
                update_value_text()
                input.delete(0, tk.END) # Clear input after pressing enter

            input.bind('<Return>', func=input_value)  # Update value on return

            # Otherwise placed between buttons
            if not HAS_BUTTONS:
                input.grid(row=row.count, column=column.count, columnspan=3)
       
    
        if HAS_BUTTONS:
            increment_button = tk.Button(frame, 
                                         text="+",  # f"+ {controller_parameter.adjust_amount}"
                                        command=lambda:(controller_parameter.increment_value(), 
                                                        update_value_text()))
            decrement_button = tk.Button(frame,
                                         text="-", # f"- {controller_parameter.adjust_amount}",
                                        command=lambda:(controller_parameter.decrement_value(), 
                                        update_value_text()))
            
            increment_button.grid(row=row.count, column=column.count)
            if HAS_INPUT:
                input.grid(row=row.count, column=column.count)
            decrement_button.grid(row=row.count, column=column.count)

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
        self.canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10, sticky=tk.NSEW)

        # ask the mainloop to call this method again in the measurement period
        self.gui.after(int(self.PLOTTING_PERIOD * 1000), self.update_values_continuously)


    class  Counter:
        """
        @brief Keeps tracks of a counter and automatically increments them when they are 
               used. Used for tkinter grid rows/columns
        """
        def __init__(self, is_incrementing: bool = True, initial_count: int = 0):
            self._count = initial_count
            self._IS_INCREMENTING = is_incrementing

        @property
        def count(self):
            # Emulates incrementing count "after" returning
            if self._IS_INCREMENTING:
                self._count += 1
                return self._count - 1
            
            return self._count




