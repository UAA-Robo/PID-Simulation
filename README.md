# Controller-Simulation
Feedback Controllers are widespread in the world of tech. PIDs in specific are an important part of many robotics application but can be confusing to understand and work with.

This program is designed to help you learn how PIDs work, how to tune them, and how they compare to other Controllers like Bang-Bang. The program simulates a tank with a random flow input and an output (**control value**) controlled by the PID and Bang-Bang Controller to simulate valve opening and closing. The difference between the input and output flow affects the tank level (**Process Value**):
> Tank-Level = (Flow-Rate-In - Flow-Rate-Out) * Time-Since-Last-Measurement + Previous-Tank-Level-At-Last-Measurement

In the GUI, you can see the affects of the PID on the Process Value as you change the **Setpoint** and tune the PID. The GUI also shows you a Bang-Bang Controller alongside the PID so you can see why PID controllers instead of Bang-Bang Controllers. 


**STATUS.** This project is in progress. The tank simulator, PID, and Bang-bang Controller are finished. The tkinter GUI to show the graph is also functional, but badly needs beautification. A visual representation of the tank also needs to be made.

## Setup
In order to install all the dependencies needed for this application, run 
`pip install -r requirements.txt` (in this directory). This can be done with or without a virtual environment (venv).

## Usage
To run this program, run `python3 tank_simulation.py` in this directory. 
A popup window will popup that will let you visualize and change the Controller Parameters:
* The **Process Value** is the level (%) that the tank is at. 
* The **Setpoint** is the level (%) that you want to the tank to change.
* For the P, I, and D are values to tune the PID. They are usually between 0-2, but it varies per application. l . The  the Setpoint is the value 

If you need more guidance, [this](https://youtu.be/4Y7zG48uHRo) is a good resource for PID and Bang-Bang controllers.

<br>
This program can very easily be adapted for a different process simulation. All that would need to be changed in `update_tank_level(...)` in `tank_simulation.py` is the Control Value and Process Value are generated. 

The Controllers and GUI in this program can also very easily be adapted to be used with an actual process instead of this simulation. In `tank_simulation.py`, instead of generating the Process Value in `update_tank_level(...)`, you would just need to use a value from your actual process sensor. Then you would need to configure the Control Value control your process.