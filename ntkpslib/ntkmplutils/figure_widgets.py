
import numpy as np
from matplotlib.patches import Polygon
from matplotlib.lines import Line2D
from matplotlib import text

class SliderError(Exception):
    pass

class Slider(object):
    def __init__(self, artists_manager, position, length, range, step=None):
        self.artists_manager, self.length, self.range, self.position, self.step = artists_manager, length, range, position, step
        self.size = 10

        self.p1 = position[0], position[1]
        self.p2 = position[0] + length, position[1]
        self.line = Line2D([self.p1[0], self.p2[0]], [self.p1[1], self.p2[1]], color='b')

        self.pol_p1 = [self.p1[0] + self.length / 2 + self.size / 2, self.p1[1] - self.size / 2]  # bottom right
        self.pol_p2 = [self.p1[0] + self.length / 2 + self.size / 2, self.p1[1] + self.size / 2]  # top right
        self.pol_p3 = [self.p1[0] + self.length / 2 - self.size / 2, self.p1[1] + self.size / 2]  # top left
        self.pol_p4 = [self.p1[0] + self.length / 2 - self.size / 2, self.p1[1] - self.size / 2]  # bottom left

        self.button = Polygon(np.array([self.pol_p1, self.pol_p2, self.pol_p3, self.pol_p4]), alpha=0.5, fc='b')

        self.pol_yconstrain = self.button.xy[:, 1].copy()
        self.offset_x = 0
        self.available_px_units = self.length - self.size
        self.range_units = float(range[1] - range[0])
        self.last_data_value = None
        self.steps = []
        if self.step:
            self._define_steps()

        artists_manager.add_artists_to_figure([self.line, self.button])
        artists_manager.make_draggable([self.button])
        artists_manager[self.button](['button_press_event', 'button_release_event', 'motion_notify_event'], self.on_drag)

    def on_drag(self, event):
        event_x = event['data']['x']
        if event['name'] == 'button_press_event':
            self.offset_x = event_x - self.button.xy[2][0]
        elif event['name'] == 'button_release_event':
            self.offset_x = 0
        elif event['name'] == 'motion_notify_event':
            event_x_normalized = event_x - self.offset_x
            limit_left = self.p1[0]
            limit_right = self.p2[0] - self.size
            button_x = self.button.xy[2][0]  # top left point
            # constrain y line
            self.button.xy[:, 1] = self.pol_yconstrain
            # constrain x limits if event_x_normalized outside range
            if event_x_normalized < limit_left or event_x_normalized > limit_right:
                if button_x >= limit_right:
                    self._bt_push_left(event_x_normalized, limit_right)
                elif button_x <= limit_left:
                    self._bt_push_right(event_x_normalized, limit_left)
            # if event_x_normalized inside range check if snapping should be implemented
            elif self.step:
                closest_xstep = self._find_closest_xstep(event_x_normalized)
                if closest_xstep:
                    if event_x_normalized > closest_xstep:
                        self._bt_push_left(event_x_normalized, closest_xstep)
                    else:
                        self._bt_push_right(event_x_normalized, closest_xstep)

        button_x_now = self.button.xy[2][0]
        data_value = ((button_x_now - self.p1[0]) / self.available_px_units) * self.range_units + self.range[0]
        if data_value != self.last_data_value:
            self.slider_on_change(data_value)
        self.last_data_value = data_value

    def _find_closest_xstep(self, event_x):
        for i, step in enumerate(self.steps):
            if event_x <= step:
                right_step = step
                left_step = self.steps[i - 1] if i > 0 else self.steps[0]
                break
        else:
            # if event was somewhere close to right side: between p2 and p2 - self.size
            left_step = self.steps[-2]
            right_step = self.steps[-1]

        offset_left = event_x - left_step
        offset_right = right_step - event_x
        min_offset = min(offset_left, offset_right)

        closest_xstep = left_step if min_offset == offset_left else right_step

        return closest_xstep

    def _define_steps(self):
        """
        if self.step is not None
        map steps in self range to abs x values on line between p1 and p2 - size
        """
        steps = []
        for value in range(self.range[0], self.range[1] + 1, self.step):
            steps.append(self._convert_value_to_x(value))
        self.steps = steps
        return self.steps

    def _bt_push_left(self, event_x, toward_x):
        self.button.xy[:, 0] -= event_x - toward_x # - self.offset_x

    def _bt_push_right(self, event_x, toward_x):
        self.button.xy[:, 0] += toward_x - event_x # + self.offset_x


    def _convert_value_to_x(self, value):
        """ convert slider value to its abs x position on line (available space for x values (which is available_px_units) exclude btn size)"""
        if value < self.range[0] or value > self.range[1]:
            raise SliderError('%s not in range %s ... %s' % (value, self.range[0], self.range[1]))
        x = (value - self.range[0]) / self.range_units * self.available_px_units + self.p1[0]
        return x

    def _convert_value_to_fake_event(self, value):
        event = {'name': 'motion_notify_event', 'data': {'x': self._convert_value_to_x(value)}}
        return event

    def set_value(self, data_value):
        fake_event = self._convert_value_to_fake_event(data_value)
        self.offset_x = 0
        # set the button where it should be for fake_event['x']
        self.button.xy[:, 0] = np.array([self.position[0] + self.size, self.position[0] + self.size, self.position[0], self.position[0], self.size]) + (fake_event['data']['x'] - self.position[0])
        self.on_drag(fake_event)

    def slider_on_change(self, event):
        self.artists_manager.artist_event_notify(self, 'slider_on_change', event)

class Text():
    def __init__(self, artists_manager, x, y, data='info'):
        self.artists_manager = artists_manager
        self.text = text.Text(x, y, data)
        artists_manager.add_artists_to_figure(self.text)
        artists_manager.make_animated(self.text)


    def set_text(self, text):
        self.text.set_text(text)

    def get_text(self):
        return self.text.get_text()

    def set_position(self, xy):
        self.text.set_position(xy)