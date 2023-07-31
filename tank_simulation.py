import random
import time
import datetime

import matplotlib.pyplot as plt
import matplotlib.animation as animation

tank_level = 50  # Measured in percentage
MEASUREMENT_PERIOD = 0.1  # Time between "measurements" (seconds)
output_flow = 4  # 0-12 cm^3/sec 

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
x_time = []
y_tank_level = []

# This function is called periodically from FuncAnimation
def animate(i, x_time, y_tank_level):
    input_flow = random.random() * 8 # 0-8 cm^3/sec
    global tank_level  # TODO: change this to not be global
    tank_level += (input_flow - output_flow) * MEASUREMENT_PERIOD
    print(tank_level)
    
    x_time.append(datetime.datetime.now().strftime('%H:%M:%S.%f'))
    y_tank_level.append(tank_level)

    # Limit x and y lists to 20 items
    x_time = x_time[-200:]
    y_tank_level = y_tank_level[-200:]

        # Draw x and y lists
    ax.clear()
    ax.plot(x_time, y_tank_level)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Tank Level')
    plt.ylabel('Tank Level (%)')



# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(x_time, y_tank_level), interval= MEASUREMENT_PERIOD * 1000)
plt.show()



