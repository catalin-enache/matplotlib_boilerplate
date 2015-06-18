
"""
matplotlib==1.4.3
numpy==1.9.2
"""

import config as cfg
import matplotlib

if cfg.RENDERER == 'tk':
    matplotlib.use('TkAgg')  # Qt4Agg TkAgg
    # import matplotlib.backends.backend_tkagg as tkagg
    # from matplotlib.backend_bases import cursors
    # tkagg.cursord[cursors.POINTER] = 'hand1'  # hand1 hand2  # http://www.tcl.tk/man/tcl8.4/TkCmd/cursors.htm
else:
    matplotlib.use('Qt4Agg')
    # import matplotlib.backends.backend_qt4 as qt4
    # import PyQt4.QtCore as QtCore
    # from matplotlib.backend_bases import cursors
    # qt4.cursord[cursors.POINTER] = QtCore.Qt.OpenHandCursor  # QtCore.Qt.ArrowCursor QtCore.Qt.ClosedHandCursor QtCore.Qt.OpenHandCursor

# print matplotlib.get_backend()

import mpl_patches
import matplotlib.pyplot as plt

import animation_manager as anim_manager
import artists_manager as art_manager
import stage_events as stg_events

figure = plt.figure(1, figsize=cfg.FIGSIZE)
axes = plt.axes(cfg.MAINAXE_POSITION, polar=cfg.MAINAXE_POLAR)

animation_manager = anim_manager.get_animation_manager(axes)
stage_events = stg_events.get_stage_events(axes)

artists_manager = art_manager.get_artists_manager(animation_manager, stage_events)
