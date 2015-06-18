
import matplotlib
use = 'tk'  # qt tk

if use == 'tk':
    matplotlib.use('TkAgg')  # Qt4Agg TkAgg
    import matplotlib.backends.backend_tkagg as tkagg
    from matplotlib.backend_bases import cursors
    tkagg.cursord[cursors.POINTER] = 'hand1'  # hand1 hand2  # http://www.tcl.tk/man/tcl8.4/TkCmd/cursors.htm
else:
    matplotlib.use('Qt4Agg')
    import matplotlib.backends.backend_qt4 as qt4
    import PyQt4.QtCore as QtCore
    from matplotlib.backend_bases import cursors
    qt4.cursord[cursors.POINTER] = QtCore.Qt.OpenHandCursor  # QtCore.Qt.ArrowCursor QtCore.Qt.ClosedHandCursor QtCore.Qt.OpenHandCursor

print matplotlib.get_backend()

import matplotlib.pyplot as plt
import matplotlib.patches as patches


fig, ax = plt.subplots()
plt.axis('equal')
ax.set(xlim=[-5, 5], ylim=[-5, 5])
plt.show()


