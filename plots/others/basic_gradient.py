

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

a = np.linspace(0, 1, 250)
b = np.zeros((250, 250))
b[:] = a

plt.imshow(b, cmap=plt.cm.binary)
plt.show()


