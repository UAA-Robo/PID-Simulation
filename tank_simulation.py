import random
import time
import datetime

import matplotlib.pyplot as plt
import matplotlib.animation as animation

from PID import PID
from PIDTunerGui import PIDTunerGui


tank_level = 50  # Measured in percentage
MEASUREMENT_PERIOD = 0.1  # Time between "measurements" (seconds)

tank_pid = PID(setpoint=75, P=1.0, I=1.5, D=0.0)


# PID GUI
pid_gui = PIDTunerGui(tank_pid)
pid_gui.start_gui()



