import threading
from time import sleep
from bangbang import bangbang
from PID import PID
import random
from PIDTunerGui import PIDTunerGui
from bangbangGUI import bangbangGUI


def update_tank_level(pid:bangbang) -> None:
    tank_level = 0
    MEASUREMENT_PERIOD = 0.1 # Seconds
    print("Producing Simulated Tank Values...")
    while(True):
        input_flow = random.random() * 8 # 0-8 cm^3/sec
        output_flow = pid.update_control_value(tank_level, MEASUREMENT_PERIOD)
        tank_level += (input_flow - output_flow) * MEASUREMENT_PERIOD
        print(f"Flow In: {input_flow:.2f} |   Flow Out: {output_flow:.2f} | Tank level: {tank_level:.2f}")
        sleep(MEASUREMENT_PERIOD)



if __name__ == '__main__':
    tank_pid1 = PID(setpoint=25, P=1.5, I=1.2, D=0.0)
    tank_pid2 = bangbang(setpoint=25, P=0, I=1, D=0.0)
    gui = bangbangGUI(PID=tank_pid1, bangbang=tank_pid2)
    IS_RUNNING = [True]
    
    # Thread is daemon to exit when the gui exits
    simulator_thread1 = threading.Thread(target=update_tank_level, args=[tank_pid1], daemon=True)
    simulator_thread2 = threading.Thread(target=update_tank_level, args=[tank_pid2], daemon=True)

    simulator_thread1.start()
    simulator_thread2.start()
    gui.start_gui()

