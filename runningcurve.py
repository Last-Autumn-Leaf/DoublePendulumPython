import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig, ax = plt.subplots()

x = np.arange(0, 2*np.pi, 0.01)
lineA, = ax.plot(x, np.sin(x))
lineB, = ax.plot(x, np.cos(x))


def animate(i):
    lineA.set_ydata(np.sin(x + i / 50))  # update the data.
    lineB.set_ydata(np.cos(x + i / 50))
    return lineA , lineB,


ani = animation.FuncAnimation(fig, animate, interval=20, blit=True, save_count=50)
plt.show()