
from matplotlib import patches
from matplotlib import text
import numpy as np

class Point(object):
    def __init__(self, artists_manager, x, y, radius, facecolor='black'):
        self.artists_manager, self.x, self.y, self.radius = artists_manager, x, y, radius
        self.gap = self.radius / 5.0

        self.text_data = None
        self.info_x, self.info_y = None, None
        self._update_state()

        self.circle = patches.Circle((self.x, self.y), self.radius, facecolor=facecolor, alpha=0.5)
        self.info = text.Text(self.info_x, self.info_y, self.text_data, alpha=0.7)

        artists_manager.add_artists_to_axes([self.circle, self.info])
        artists_manager.make_animated([self.info])
        artists_manager.make_draggable([self.circle])
        artists_manager[self.circle](['motion_notify_event'], self.on_drag)

    def on_drag(self, event):
        self.x, self.y = event['data']['x'], event['data']['y']
        self.circle.center = self.x, self.y

        self._update_state()

        self.info.set_text(self.text_data)
        self.info.set_position((self.info_x, self.info_y))

        self.on_change({'x': self.x, 'y': self.y, 'instance': self})

    def on_change(self, event):
        self.artists_manager.artist_event_notify(self, 'on_change', event)

    def _update_state(self):
        self.text_data = '%.2f, %.2f' % (self.x, self.y)
        self.info_x, self.info_y = self.x - self.radius, self.y + self.radius + self.gap

    def set_position(self, x, y):

        fake_event = {'data': {'x': x, 'y': y}}
        self.on_drag(fake_event)

    def set_visible(self, bool):
        self.circle.set_visible(bool)
        self.info.set_visible(bool)

    def set_color(self, color):
        self.circle.set_color(color)

class PathPatch(object):
    def __init__(self, artists_manager, path, show_handlers=None, **kwargs):
        self.artists_manager = artists_manager
        self.path = path
        self.show_handlers = show_handlers
        self.kwargs = kwargs
        self.path_patch = patches.PathPatch(self.path, **self.kwargs)

        self.points = None
        self.dragging = False
        self._init_state()

        artists_manager.add_artists_to_axes([self.path_patch])
        artists_manager.make_draggable([self.path_patch])
        artists_manager[self.path_patch](['motion_notify_event'], self.motion_notify_event)
        artists_manager[self.path_patch](['button_press_event'], self.button_press_event)
        artists_manager[self.path_patch](['button_release_event'], self.button_release_event)

    def _init_state(self):
        if self.show_handlers:
            radius = self.show_handlers
        else:
            radius = 0.0001
        self.points = {}
        for i, vertex in enumerate(self.path.vertices):
            point = Point(self.artists_manager, vertex[0], vertex[1], radius)
            point.on_change = self._on_handler_changed  # delegate to self
            self.points[point] = i

    def button_press_event(self, event):
        if event['artist'] == self.path_patch:
            self.dragging = True

    def button_release_event(self, event):
        self.dragging = False

    def motion_notify_event(self, event):
        self._update_handlers_position()
        self.on_change('drag')

    def _on_handler_changed(self, event):
        point_idx = self.points[event['instance']]
        old_value = self.path.vertices[point_idx].copy()
        cur_value = [event['x'], event['y']]
        self.path.vertices[point_idx][0] = cur_value[0]
        self.path.vertices[point_idx][1] = cur_value[1]
        if not self.dragging:
            self.on_change('handler_changed', handler_changed={point_idx: {'old_value': old_value, 'cur_value': cur_value}})

    def on_change(self, action, handler_changed=None):
        event = {'action': action, 'handler_changed': handler_changed, 'vertices_copy': self.vertices_copy}
        self.artists_manager.artist_event_notify(self, 'on_change', event)

    def _update_handlers_position(self):
        for point, i in self.points.items():
                x, y = self.path.vertices[i]
                point.set_position(x, y)

    @property
    def vertices_copy(self):
        return self.path.vertices.copy()

    def get_points(self):
        points = [None] * len(self.points)
        for point, i in self.points.items():
            points[i] = point
        return points

    def set_vertices(self, vertices):  # vertices: nd.array
        self.path.vertices = vertices
        self._update_handlers_position()