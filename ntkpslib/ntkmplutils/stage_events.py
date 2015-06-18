
import math
from collections import defaultdict

class StageEvents(object):
    VALID_EVENT_NAMES = ['pick_event', 'button_press_event', 'motion_notify_event', 'button_release_event', 'draw_event', 'key_press_event', 'key_release_event', 'resize_event', 'scroll_event', 'figure_enter_event', 'figure_leave_event', 'axes_enter_event', 'axes_leave_event']
    def __init__(self, axes):
        self.axes = axes
        self.figure = self.axes.figure
        self.button_press = None
        self.pressed_inaxes = None
        self.last_xdata, self.last_ydata = 0, 0
        self.event_dx, self.event_dy = 0, 0
        self.registered_callbacks = defaultdict(list)
        for event_name in self.VALID_EVENT_NAMES:
            self.figure.canvas.mpl_connect(event_name, getattr(self, event_name))

    def register_callback(self, event_names, callback):
            if event_names == '*':
                event_names = self.VALID_EVENT_NAMES
            elif not isinstance(event_names, list):
                event_names = [event_names]

            for event_name in event_names:
                if event_name in self.VALID_EVENT_NAMES:
                    self.registered_callbacks[event_name].append(callback)

    def pick_event(self, event):
        event_data = self._prepare_event_notify(event)
        self._stage_event_notify(event_data)

    def button_press_event(self, event):
        self.pressed_inaxes = event.inaxes
        self.event_dx, self.event_dy = 0, 0
        self.button_press = self._get_event_xy(event)

        event_data = self._prepare_event_notify(event)
        self._stage_event_notify(event_data)


    def motion_notify_event(self, event):
        if self.button_press is None: return
        self._get_event_distance_xy(event)

        event_data = self._prepare_event_notify(event)
        self._stage_event_notify(event_data)

    def button_release_event(self, event):
        event_data = self._prepare_event_notify(event)
        self._stage_event_notify(event_data)

        self.button_press = None


    def draw_event(self, event):
        pass

    def key_press_event(self, event):
        pass

    def key_release_event(self, event):
        pass

    def resize_event(self, event):
        pass

    def scroll_event(self, event):
        pass

    def figure_enter_event(self, event):
        pass

    def figure_leave_event(self, event):
        pass

    def axes_enter_event(self, event):
        pass

    def axes_leave_event(self, event):
        pass

    def _get_event_xy(self, event):
        _event = event if event.name != 'pick_event' else event.mouseevent
        ret = (_event.xdata or self.last_xdata, _event.ydata or self.last_ydata) if self.pressed_inaxes else (_event.x, _event.y)
        if _event.xdata is not None and _event.ydata is not None:
            self.last_xdata, self.last_ydata = _event.xdata, _event.ydata
        return ret

    def _get_event_distance_xy(self, event):
        eventx, eventy = self._get_event_xy(event)
        if not all([eventx is not None, eventy is not None]): return self.event_dx, self.event_dy
        self.event_dx = eventx - self.button_press[0]
        self.event_dy = eventy - self.button_press[1]
        return self.event_dx, self.event_dy

    def _prepare_event_notify(self, event):
        xy = self._get_event_xy(event)
        _event = event if event.name != 'pick_event' else event.mouseevent
        event_data = {
            'original': event,
            'source': event.__class__,
            'name': event.name,
            'key': None,
            'x': xy[0],
            'y': xy[1],
            'xmouse': _event.x,
            'ymouse': _event.y,
            'xdata': _event.xdata,
            'ydata': _event.ydata,
            'distance_x': self.event_dx,
            'distance_y': self.event_dy,
            'distance_length': math.sqrt(self.event_dx ** 2 + self.event_dy ** 2),
            'radians': math.atan2(self.event_dy, self.event_dx),
        }
        event_data['angle'] = math.degrees(event_data['radians'])
        return event_data

    def _stage_event_notify(self, event):
        for event_name, callbacks in self.registered_callbacks.items():
            if event_name == event['name']:
                for callback in callbacks:
                    callback(event)


stage_events = None
def get_stage_events(axes):
    global stage_events
    if stage_events is None:
        stage_events = StageEvents(axes)
    return stage_events