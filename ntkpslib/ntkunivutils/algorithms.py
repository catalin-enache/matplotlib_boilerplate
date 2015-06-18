
import math

INFINITY = float('inf')
#INFINITY = 999999999999999.0  # something very big close to infinity

# helper to normalize value as to not get false non positives
def n(val):
    return int(round(val * 1000000))

# helper to get margins for the value
def e(value, margin):
        return value - margin, value + margin


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def point_in_rect_of_two_points(p, p1, p2, margin=0):
    """
    we check if point inside rect defined by 2 points
    """
    left_x, right_x = sorted([n(p1.x), n(p2.x)])
    bottom_y, top_y = sorted([n(p1.y), n(p2.y)])
    xy = n(p.x), n(p.y)

    _margin = n(margin)

    left_x -= _margin
    right_x += _margin
    bottom_y -= _margin
    top_y += _margin

    if left_x <= xy[0] <= right_x and bottom_y <= xy[1] <= top_y:
        return True


def line_slope_from_2_points(p1, p2):
    """
    slope = raise / run
    @returns m (slope)
    """
    _raise = p1.y - p2.y
    _run = p1.x - p2.x
    if _run == 0 and _raise == 0:
        return None
    elif _run == 0:
        return INFINITY  # vertical
    elif _raise == 0:
        return 0  # horizontal
    return _raise / _run

def line_y_intercept(p, m):
    """
    y = mx + b || b = y - mx
    @returns b (y intercept)
    """
    b = p.y - m * p.x
    return b

def line_system_of_equations_of_slope_intercept_form(m1, x1, b1, m2, x2, b2):
    """
    b1 = y - m1 * x | from y = mx + b
    b2 = y - m2 * x | so, y = b2 + m2 * x in second equation
    b1 = b2 + m2 * x - m1 * x # substitute y in first eq
    b1 - b2 = m2 * x - m1 * x # put x terms on the same side
    b1 - b2 = x(m2 - m1) # factor out x
    (b1 - b2)/(m2 - m1) = x # this is x value in first equation
    we will find y later by putting x in any of these 2 equations - theoretically
    in practice we'll put x in both of them and y values will be almost the same
    @returns intersection point
    """
    if m1 == 0 and m2 == 0:  # if both lines are horizontal
        return None
    elif m1 == INFINITY and m2 == INFINITY:  # if both lines are vertical
        return None
    elif m1 == INFINITY:  # if line_1 is vertical
        x = x1  # any x from line_1
        y = m2 * x + b2  # y is equation of line_2 for x1
    elif m2 == INFINITY:  # if line_2 is vertical
        x = x2  # any x from line_2
        y = m1 * x + b1  # y is equation of line_1 for x2
    else:
        x = (b1 - b2) / (m2 - m1)
        y00 = m1 * x + b1
        y01 = m2 * x + b2
        # y00 and y01 are found by putting resulted x in both lines equations
        # Theoretically y00 and y01 should be identical.
        # In practice their value is almost equal but not exactly the same, so we get a mean for both
        y = (y00 + y01) / 2

    return x, y


def intersection_line_line(line1_p1, line1_p2, line2_p1, line2_p2, segment_intersection=True):
    x1 = line1_p1.x
    x2 = line2_p1.x
    m1 = line_slope_from_2_points(line1_p1, line1_p2)
    m2 = line_slope_from_2_points(line2_p1, line2_p2)
    b1 = line_y_intercept(line1_p1, m1)
    b2 = line_y_intercept(line2_p1, m2)
    xy = line_system_of_equations_of_slope_intercept_form(m1, x1, b1, m2, x2, b2)
    if not xy: return None
    if not segment_intersection:
        return xy
    else:  # return intersection_point only if inside segments
        if point_in_rect_of_two_points(Point(xy[0], xy[1]), line1_p1, line1_p2, margin=0) \
        and point_in_rect_of_two_points(Point(xy[0], xy[1]), line2_p1, line2_p2, margin=0):
            return xy

def line_contains_point(line_p1, line_p2, p, segment=True, margin=0):
    """
    find equation of line
    put p.x in this equation and check if y returned equals p.y
    """
    m = line_slope_from_2_points(line_p1, line_p2)
    b = line_y_intercept(line_p1, m)

    if m == INFINITY:  # if line is vertical
        x00, x01 = e(line_p1.x, margin)
        test = x00 <= p.x <= x01
    else:
        y_test = m * p.x + b
        _margin = margin
        if m > 1 or m < -1:
            _margin = margin * abs(m)  # m tends to infinity as line tends toward vertical. so, we have to increase the margin because very small x changes result in big y changes and a fixed margin would not fit.
        y00, y01 = e(y_test, _margin)
        test = y00 <= p.y <= y01

    if test:
        if not segment:
            return test
        else:  # check if point on segment
            if point_in_rect_of_two_points(p, line_p1, line_p2, margin):
                return test