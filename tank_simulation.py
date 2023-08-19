import threading
from time import sleep
from PID import PID
import random
from PIDTunerGui import PIDTunerGui

# TODO: simulate tank level

def update_tank_level(pid:PID) -> None:
    tank_level = 0
    MEASUREMENT_PERIOD = 0.1 # Seconds
    print("Producing Simulated Tank Values...")
    while(True):
        input_flow = random.random() * 8 # 0-8 cm^3/sec
        output_flow = pid.update_control_value(tank_level, MEASUREMENT_PERIOD)
        tank_level += (input_flow - output_flow) * MEASUREMENT_PERIOD
        #print(f"Flow In: {input_flow:.2f} |   Flow Out: {output_flow:.2f} | Tank level: {tank_level:.2f}")
        sleep(MEASUREMENT_PERIOD)



if __name__ == '__main__':
    tank_pid = PID(setpoint=75, P=1.0, I=1.5, D=0.0)
    gui = PIDTunerGui(tank_pid)
    IS_RUNNING = [True]
    
    # Thread is daemon to exit when the gui exits
    simulator_thread = threading.Thread(target=update_tank_level, args=[tank_pid], daemon=True)

    simulator_thread.start()
    gui.start_gui()

# TEST comment