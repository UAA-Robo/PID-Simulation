import customtkinter as ctk 
import tkinter as tk
from Controllers.Controller import Controller

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Plot(FigureCanvasTkAgg):
    def __init__(self,
                 app: ctk.CTk, # TODO: see if need this!
                 master:any,
                 controllers: list[Controller],
                 update_period: float = 0.2,  # second
                 ):
        
        self.fig = plt.figure(layout='constrained', figsize=(4,3))
        super().__init__(self.fig, master = master)
        
        
        self.app = app
        self.controllers = controllers
        self.UPDATE_PERIOD = update_period
        
        dark_color = "#323232"
        self.light_color = "white"

        
        self.fig.set_facecolor(dark_color)
        self.subplot = self.fig.add_subplot(1, 1, 1)
        self.subplot.set_facecolor(dark_color)
    
        for side in ["bottom", "top", "right", "left"]: 
            self.subplot.spines[side].set_color(self.light_color)
        for axis in ["x", "y"]:     
            self.subplot.tick_params(axis=axis, colors=self.light_color)
        plt.rc('font', **{'size': 6})
        plt.rcParams.update({'text.color': self.light_color,'axes.labelcolor': self.light_color})

        # Start continuos callback
        self.update_plot_callback()
    


    def update_plot_callback(self):
        """
        @brief    Updates plot and process value display every UPDATE_PERIOD to be up to date
                  with the data in the controller classes.
        """

        self.subplot.clear()
        for controller in self.controllers:
            self.subplot.plot(controller.process.time_log, controller.process.value_log, 
                              label =controller.controller_name, linestyle="-")
        
        plt.xticks(rotation=45, ha="right")
        plt.legend(facecolor="#323232", frameon=False)
        plt.title("Process")
        plt.xlabel('Time')
        plt.ylabel("Process Value")
        plt.ylim([0, 100])

        self.draw()
        self.get_tk_widget().grid(row=0, column=0,sticky=tk.NSEW)
        

        # ask the mainloop to call this method again in the measurement period
        self.app.after(int(self.UPDATE_PERIOD * 1000), self.update_plot_callback)