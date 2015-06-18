

# ===================== import stage objects here =========================
from ntkmplutils.stage import artists_manager, run, info_axes_events
from matplotlib.path import Path
from ntkunivutils.algorithms import Point, line_contains_point


# ===================== define objects ========================================

line_1 = artists_manager.add_axes_widget('PathPatch', Path([(-7, -2), (-7, 8)], [Path.MOVETO, Path.LINETO]), facecolor='yellow', alpha=0.5, fill=False, ls='solid', show_handlers=0.15)  # line_1 vertical
line_2 = artists_manager.add_axes_widget('PathPatch', Path([(-9, 7), (1, 7)], [Path.MOVETO, Path.LINETO]), facecolor='yellow', alpha=0.5, fill=False, ls='solid', show_handlers=0.15)  # line_1 horizontal

point = artists_manager.add_axes_widget('Point', 0, 0, 0.15, facecolor='black')


# =========================== assign objects to callbacks ============================

artists_manager[point]('on_change', lambda event: point_on_move(event))

# ===================== define callbacks ========================================

margin = 0.02
segment = True
def point_on_move(event):
    px, py = event['data']['x'], event['data']['y']
    line1_p1, line1_p2 = line_1.get_points()
    line2_p1, line2_p2 = line_2.get_points()

    online1 = line_contains_point(Point(line1_p1.x, line1_p1.y), Point(line1_p2.x, line1_p2.y), Point(px, py), segment=segment, margin=margin)
    online2 = line_contains_point(Point(line2_p1.x, line2_p1.y), Point(line2_p2.x, line2_p2.y), Point(px, py), segment=segment, margin=margin)

    if online1:
        point.set_color('r')
    elif online2:
        point.set_color('g')
    else:
        point.set_color('black')
# ==============================================================================================================================



# ==============================================================================================================================



__name__ == '__main__' and run()


