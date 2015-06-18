
import matplotlib as mpl
# mpl.use('TkAgg')
# print mpl.get_backend()

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib import animation


def motion_capture(event):
    try:
        x = int(event.xdata)
        y = int(event.ydata)
        pixels[y][x] = 1.0
        im.set_data(pixels)
        # plt.draw() # comment this if using FuncAnimation
        # print x, y
    except:
        pass

pixels = np.zeros((600, 800))
pixels[0][0] = 1  # hack ?

fig, axe = plt.subplots()
im = axe.imshow(pixels, interpolation='none', cmap=plt.cm.binary)
fig.canvas.mpl_connect('motion_notify_event', motion_capture)

# =========== FuncAnimation section ============


def init():
    return im,   # if blit=True in FuncAnimation, what we return here hints that function what artist changed - for performance reason


def animate(i):
    # print i # i are frames param in FuncAnimation | when frames reach their value they reset to 0 and start again
    return im,  # if blit=True in FuncAnimation, what we return here hints that function what artist changed - for performance reason


anim = animation.FuncAnimation(fig, animate, init_func=init, frames=10, interval=100, blit=True)

# =========== END FuncAnimation section ============

plt.show()