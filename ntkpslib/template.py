

# ===================== import stage objects here =========================
from ntkmplutils.stage import artists_manager, run
import numpy as np
from matplotlib.path import Path


artists_manager.register_animation_callback(lambda i: on_animation(i))

def on_animation(i):
    pass

# ===================== define objects ========================================

x1 = np.arange(-1000, 1000, 0.1)
y1, = artists_manager.plot(x1, x1 ** 2 + 0, '-')

o1 = artists_manager.add_axes_widget('PathPatch', Path([(-3, -7), (-3, -0), (7, -0), (7, -7)], [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]), facecolor='yellow', alpha=0.5, fill=True, ls='solid', show_handlers=0.15)
o2 = artists_manager.add_axes_widget('PathPatch', Path([(-6, 5), (-4, 4), (-2, 5)], [Path.MOVETO, Path.CURVE3, Path.CURVE3]), facecolor='green', alpha=0.5, fill=True, ls='dotted', show_handlers=0.15)
o3 = artists_manager.add_axes_widget('PathPatch', Path([(4, 5), (5, 6), (6, 5), (4, 5)], [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO]), facecolor='magenta', alpha=0.5, fill=True, ls='solid', show_handlers=0.15)
o4 = artists_manager.add_axes_widget('PathPatch', Path([(-8, 7), (-8, 2)], [Path.MOVETO, Path.LINETO]), facecolor='yellow', alpha=0.5, fill=False, ls='solid', show_handlers=0.15)

p1 = artists_manager.add_axes_widget('Point', -9, 9, 0.3, facecolor='cyan')

# =========================== assign objects to callbacks ============================

artists_manager[o1]('on_change', lambda event: o1_on_change(event))
artists_manager[p1]('on_change', lambda event: p1_on_change(event))

# ===================== define callbacks ========================================

def o1_on_change(event):
    if event['data']['action'] == 'handler_changed':
        o2.get_points()[0].set_position(*event['data']['handler_changed'].values()[0]['cur_value'])

def p1_on_change(event):
    pass
    # print event['data']['x'], event['data']['y']


# ==============================================================================================================================

__name__ == '__main__' and run()



'''
# polar example
r = np.arange(0, 3.0, 0.01)
theta = 2*np.pi*r
artists_manager.plot(theta, r, color='#ee8d18', lw=3)
artists_manager.axes.set_rmax(2.0)
'''
