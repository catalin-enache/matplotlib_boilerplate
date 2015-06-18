import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

fig, axes = plt.subplots(ncols=2)

axes[0].imshow(np.random.random((10,10)), interpolation='none')
axes[1].imshow(np.random.random((10,10)))

def motion_capture(event):
    print event.xdata
    print event.ydata

fig.canvas.mpl_connect('motion_notify_event', motion_capture)

plt.show()