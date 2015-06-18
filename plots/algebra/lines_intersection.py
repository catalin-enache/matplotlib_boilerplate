

# ===================== import stage objects here =========================
from ntkmplutils.stage import artists_manager, run, info_axes_events
from matplotlib.path import Path
from ntkunivutils.algorithms import Point, line_slope_from_2_points, intersection_line_line


# ===================== define objects ========================================

line_1 = artists_manager.add_axes_widget('PathPatch', Path([(-7, -2), (-7, 8)], [Path.MOVETO, Path.LINETO]), facecolor='yellow', alpha=0.5, fill=False, ls='solid', show_handlers=0.15)  # line_1 vertical
line_2 = artists_manager.add_axes_widget('PathPatch', Path([(-4, 8), (-4, -2)], [Path.MOVETO, Path.LINETO]), facecolor='yellow', alpha=0.5, fill=False, ls='solid', show_handlers=0.15)  # line_2 vertical
line_3 = artists_manager.add_axes_widget('PathPatch', Path([(-9, 7), (1, 7)], [Path.MOVETO, Path.LINETO]), facecolor='yellow', alpha=0.5, fill=False, ls='solid', show_handlers=0.15)  # line_1 horizontal
line_4 = artists_manager.add_axes_widget('PathPatch', Path([(-9, 4), (1, 4)], [Path.MOVETO, Path.LINETO]), facecolor='yellow', alpha=0.5, fill=False, ls='solid', show_handlers=0.15)  # line_2 horizontal


intersection_point_1_2 = artists_manager.add_axes_widget('Point', 0, 0, 0.15, facecolor='r')
intersection_point_1_3 = artists_manager.add_axes_widget('Point', 0, 1, 0.15, facecolor='b')
intersection_point_1_4 = artists_manager.add_axes_widget('Point', 0, 2, 0.15, facecolor='y')
intersection_point_2_3 = artists_manager.add_axes_widget('Point', 0, 3, 0.15, facecolor='c')
intersection_point_2_4 = artists_manager.add_axes_widget('Point', 0, 4, 0.15, facecolor='g')
intersection_point_3_4 = artists_manager.add_axes_widget('Point', 0, 5, 0.15, facecolor='m')

# =========================== assign objects to callbacks ============================

artists_manager[line_1]('on_change', lambda event: lines_on_change(event))
artists_manager[line_2]('on_change', lambda event: lines_on_change(event))
artists_manager[line_3]('on_change', lambda event: lines_on_change(event))
artists_manager[line_4]('on_change', lambda event: lines_on_change(event))

# ===================== define callbacks ========================================

def lines_on_change(event=None):

    line1_p1, line1_p2 = line_1.get_points()
    line2_p1, line2_p2 = line_2.get_points()
    line3_p1, line3_p2 = line_3.get_points()
    line4_p1, line4_p2 = line_4.get_points()

    intersection_1_2 = intersection_line_line(Point(line1_p1.x, line1_p1.y), Point(line1_p2.x, line1_p2.y), Point(line2_p1.x, line2_p1.y), Point(line2_p2.x, line2_p2.y), segment_intersection=True)
    intersection_1_3 = intersection_line_line(Point(line1_p1.x, line1_p1.y), Point(line1_p2.x, line1_p2.y), Point(line3_p1.x, line3_p1.y), Point(line3_p2.x, line3_p2.y), segment_intersection=True)
    intersection_1_4 = intersection_line_line(Point(line1_p1.x, line1_p1.y), Point(line1_p2.x, line1_p2.y), Point(line4_p1.x, line4_p1.y), Point(line4_p2.x, line4_p2.y), segment_intersection=True)
    intersection_2_3 = intersection_line_line(Point(line2_p1.x, line2_p1.y), Point(line2_p2.x, line2_p2.y), Point(line3_p1.x, line3_p1.y), Point(line3_p2.x, line3_p2.y), segment_intersection=True)
    intersection_2_4 = intersection_line_line(Point(line2_p1.x, line2_p1.y), Point(line2_p2.x, line2_p2.y), Point(line4_p1.x, line4_p1.y), Point(line4_p2.x, line4_p2.y), segment_intersection=True)
    intersection_3_4 = intersection_line_line(Point(line3_p1.x, line3_p1.y), Point(line3_p2.x, line3_p2.y), Point(line4_p1.x, line4_p1.y), Point(line4_p2.x, line4_p2.y), segment_intersection=True)

    intersection_points = [
        (intersection_1_2, intersection_point_1_2),
        (intersection_1_3, intersection_point_1_3),
        (intersection_1_4, intersection_point_1_4),
        (intersection_2_3, intersection_point_2_3),
        (intersection_2_4, intersection_point_2_4),
        (intersection_3_4, intersection_point_3_4),
    ]

    for intersection, intersection_point in intersection_points:
        if intersection:
            intersection_point.set_visible(True)
            intersection_point.set_position(*intersection)
        else:
            intersection_point.set_visible(False)



# ==============================================================================================================================

lines_on_change()

# ==============================================================================================================================



__name__ == '__main__' and run()


