
import matplotlib
import artists_behaviour
import figure_widgets, axes_widgets
from collections import defaultdict

class ArtistManagerException(Exception):
    pass

class ArtistsManager(object):
    VALID_EVENT_NAMES = ['button_press_event', 'button_release_event', 'motion_notify_event'] + ['slider_on_change'] + ['on_change']
    def __init__(self, animation_manager, stage_events):
        self.axes = animation_manager.axes
        self.figure = self.axes.figure
        self.animation_manager = animation_manager
        self.stage_events = stage_events
        self.references = []
        self.registered_callbacks = defaultdict(lambda: defaultdict(list))


    def add_figure_widget(self, widget_type, *args, **kwargs):
        if widget_type == 'Slider':
            widget = figure_widgets.Slider(self, *args, **kwargs)
        elif widget_type == 'Text':
            widget = figure_widgets.Text(self, *args, **kwargs)
        else:
            raise ArtistManagerException('%s widget not known' % widget_type)
        self.references.append(widget)
        return widget

    def add_axes_widget(self, widget_type, *args, **kwargs):
        if widget_type == 'Point':
            widget = axes_widgets.Point(self, *args, **kwargs)
        elif widget_type == 'PathPatch':
            widget = axes_widgets.PathPatch(self, *args, **kwargs)
        else:
            raise ArtistManagerException('%s widget not known' % widget_type)
        self.references.append(widget)
        return widget

    def add_artists_to_figure(self, artists):
        if not isinstance(artists, list):
            artists = [artists]
        for artist in artists:
            artist.set_figure(self.figure)
            artist.set_transform(None)
            # artist.set_clip_box(self.axes.bbox)
            # artist.set_clip_on(False)
            if isinstance(artist, matplotlib.lines.Line2D):
                self.figure.lines.append(artist)
            elif isinstance(artist, matplotlib.patches.Patch):
                self.figure.patches.append(artist)
            elif isinstance(artist, matplotlib.text.Text):
                self.figure.texts.append(artist)
            else:
                raise ArtistManagerException('%s not allowed' % artist)

    def add_artists_to_axes(self, artists):
        if not isinstance(artists, list):
            artists = [artists]
        for artist in artists:
            artist.set_figure(self.figure)
            artist.set_transform(self.axes.transData)
            if isinstance(artist, matplotlib.lines.Line2D):
                self.axes.add_line(artist)
            elif isinstance(artist, matplotlib.patches.Patch):
                self.axes.add_patch(artist)
            elif isinstance(artist, matplotlib.text.Text):
                self.axes.add_artist(artist)
            else:
                raise ArtistManagerException('%s not allowed' % artist)
    @property
    def figure_artists(self):
        return self.figure.patches + self.figure.lines

    @property
    def axes_artists(self):
        return self.axes.patches + self.axes.lines

    @property
    def all_artists(self):
        return self.figure_artists + self.axes_artists

    def make_clickable(self, artists):
        self.references.append(artists_behaviour.ClickableArtists(artists, self))
        self.make_animated(artists)

    def make_draggable(self, artists):
        self.references.append(artists_behaviour.DraggableArtists(artists, self))
        self.make_animated(artists)

    def make_animated(self, artists):
        if not isinstance(artists, list):
            artists = [artists]
        self.animation_manager.make_animated(artists)

    def plot(self, *args, **kwargs):
        artists = self.axes.plot(*args, **kwargs)
        self.make_animated(artists)
        return artists

    def __getitem__(self, artist):
        def register_artist_event_callback(event_names, callback):
            if event_names == '*':
                event_names = self.VALID_EVENT_NAMES
            elif not isinstance(event_names, list):
                event_names = [event_names]

            for event_name in event_names:
                if event_name in self.VALID_EVENT_NAMES:
                    self.registered_callbacks[id(artist)][event_name].append(callback)
        return register_artist_event_callback

    def register_stage_event_callback(self, event_names, callback):
        self.stage_events.register_callback(event_names, callback)

    def register_animation_callback(self, callback):
        self.animation_manager.register_animation_callback(callback)

    def artist_event_notify(self, artist, mname, data=None):
        event = {'artist': artist, 'name': mname, 'data': data}
        for callback in self.registered_callbacks[id(artist)][mname]: callback(event)



artists_manager = None
def get_artists_manager(animation_manager, stage_events):
    global artists_manager
    if artists_manager is None:
        artists_manager = ArtistsManager(animation_manager, stage_events)
    return artists_manager
