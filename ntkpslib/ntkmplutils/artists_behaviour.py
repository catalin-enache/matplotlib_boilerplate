
# inspired from http://matplotlib.org/users/event_handling.html#draggable-rectangle-exercise
# and http://matplotlib.1069221.n5.nabble.com/Matplotlib-drag-overlapping-points-interactively-td42847.html

import matplotlib
import config as cfg
from blitter import Blitter

class DraggableException(Exception):
    pass

# ======================== ABSTRACT CLASSES =================================

class EventsArtists(object):
    def __init__(self, artists, artist_manager):
        for artist in artists:
            artist.set_picker(5) if isinstance(artist, matplotlib.lines.Line2D) else artist.set_picker(True)
        self.artist_manager = artist_manager
        self.artists = artists
        self.current_artist = None
        self.mouse_pressed = False
        self.subscribe_on_events(['pick_event'])
        self.startx, self.starty, self.event_dx, self.event_dy = None, None, 0, 0

    # we subscribe for stage events via artist manager
    # we will react to them and send them back to artist manager where others can subscribe for our events | we act like a proxy
    def subscribe_on_events(self, event_names):
        for event_name in event_names:
            self.artist_manager.register_stage_event_callback(event_name, getattr(self, event_name))

    def pick_event(self, event):
        _event = event['original']
        if self.current_artist is None and _event.artist in self.artists:
            self.current_artist = _event.artist
            return True
        return False

    # we send our events to artist manager which will take care to dispatch them to other subscribers
    def event_notify(self, event):
        self.artist_manager.artist_event_notify(self.current_artist, event['name'], event)

    def set_event_start_xy(self, startx, starty):
        self.startx, self.starty = startx, starty

    def reset_event_tracking(self):
        self.startx, self.starty, self.event_dx, self.event_dy = None, None, 0, 0

# ======================== CONCRETE CLASSES =================================

class ClickableArtists(EventsArtists):
    def __init__(self, artists, artist_manager):
        super(ClickableArtists, self).__init__(artists, artist_manager)
        self.subscribe_on_events(['button_press_event', 'button_release_event'])
        self.remembered_state = None
        self.background = None
        self.blitter = None if cfg.ANIMATION else Blitter()

    def button_press_event(self, event):
        if self.current_artist is None: return False
        self.event_notify(event)
        self.set_event_start_xy(*(event['x'], event['y']))
        self.remembered_state = self.save_state()
        self.blitter and self.blitter.on_start(self.current_artist)
        self.mouse_pressed = True
        return True

    def button_release_event(self, event):
        if self.current_artist is None: return False
        self.event_notify(event)
        self.reset_event_tracking()
        self.remembered_state = None
        self.blitter and self.blitter.on_end(self.current_artist)
        self.mouse_pressed = False
        self.current_artist = None
        return True

    def save_state(self):
        pass  # yet DraggableArtists must return artist state on button_press_event


class DraggableArtists(ClickableArtists):
    def __init__(self, artists, artist_manager):
        super(DraggableArtists, self).__init__(artists, artist_manager)
        self.subscribe_on_events(['motion_notify_event'])
        self.drag_handlers = {
            matplotlib.patches.Polygon: PolygonDragHandler,
            matplotlib.patches.Circle: EllipseDragHandler,
            matplotlib.patches.Ellipse: EllipseDragHandler,
            matplotlib.patches.PathPatch: PathPatchHandler,
            matplotlib.lines.Line2D: Line2DHandler,
            matplotlib.text.Text: TextHandler
        }

    def motion_notify_event(self, event):
        if self.current_artist is None or not self.mouse_pressed: return
        self.event_dx, self.event_dy = event['distance_x'], event['distance_y']
        all([self.event_dx is not None, self.event_dy is not None]) and self.get_next_position()
        self.blitter and self.blitter.on_animate(self.current_artist)
        self.event_notify(event)

    def save_state(self):
        return self.drag_handlers[self.current_artist.__class__].save_state(self)

    def get_next_position(self):
        self.drag_handlers[self.current_artist.__class__].get_next_position(self)



class PolygonDragHandler(object):
    @staticmethod
    def save_state(self):
        return self.current_artist.xy[:, 0].copy(), self.current_artist.xy[:, 1].copy()

    @staticmethod
    def get_next_position(self):
        artistx, artisty = self.remembered_state
        self.current_artist.xy[:, 0] = (artistx + self.event_dx)
        self.current_artist.xy[:, 1] = (artisty + self.event_dy)

class EllipseDragHandler(object):
    @staticmethod
    def save_state(self):
        return self.current_artist.center

    @staticmethod
    def get_next_position(self):
        center = self.remembered_state
        self.current_artist.center = center[0] + self.event_dx, center[1] + self.event_dy

class PathPatchHandler(object):
    @staticmethod
    def save_state(self):
        verticesx, verticesy = self.current_artist.get_path().vertices[:, 0].copy(), self.current_artist.get_path().vertices[:, 1].copy()
        return verticesx, verticesy

    @staticmethod
    def get_next_position(self):
        verticesx, verticesy = self.remembered_state
        self.current_artist.get_path().vertices[:, 0] = (verticesx + self.event_dx)
        self.current_artist.get_path().vertices[:, 1] = (verticesy + self.event_dy)

class Line2DHandler(object):
    @staticmethod
    def save_state(self):
        return self.current_artist.get_data()

    @staticmethod
    def get_next_position(self):
        artistx, artisty = self.remembered_state
        self.current_artist.set_data([artistx + self.event_dx, artisty + self.event_dy])

class TextHandler(object):
    @staticmethod
    def save_state(self):
        return self.current_artist.get_position()

    @staticmethod
    def get_next_position(self):
        artistx, artisty = self.remembered_state
        self.current_artist.set_position([artistx + self.event_dx, artisty + self.event_dy])





