
import config as cfg
from matplotlib.animation import FuncAnimation

class AnimationManager(object):
    def __init__(self, axes):
        self.animated_artists = []
        self.animation = None
        self.animation_callbacks = []
        self.fig = axes.figure
        self.axes = axes
        self.frame = 0

    def animation_init(self):
        return self.animated_artists

    def animate(self, i):
        if cfg.ANIMATION and i is not None:
            [callback(i) for callback in self.animation_callbacks]
        return self.animated_artists

    def start_animation(self):
        if not cfg.ANIMATION: return
        [artist.set_animated(True) for artist in self.animated_artists]
        self.animation = FuncAnimation(self.fig, self.animate, init_func=self.animation_init, interval=cfg.ANIMATION_INTERVAL, frames=self.frames(), blit=True)  # interval=10 allow other friends (ex: sliders) to draw_idle()

    def stop_animation(self):
        if not cfg.ANIMATION: return
        [artist.set_animated(False) for artist in self.animated_artists]
        self.animation = None



    def frames(self):
        while True:
            if not self.animation:
                raise StopIteration  # stop old animation from inside itself
            self.frame = self.get_next_frame(self.frame)
            yield self.frame

    def make_animated(self, artists):
        if not cfg.ANIMATION: return
        if not isinstance(artists, list): artists = [artists]
        [artist.set_animated(True) for artist in artists]
        [self.animated_artists.append(artist) for artist in artists if artist not in self.animated_artists]
        return self

    def unmake_animated(self, artists):
        if not cfg.ANIMATION: return
        if not isinstance(artists, list): artists = [artists]
        [artist.set_animated(False) for artist in artists]
        self.animated_artists = [artist for artist in self.animated_artists if artist not in artists]

    @staticmethod
    def get_next_frame(frame):
        if frame >= cfg.ANIMATION_FRAMES:
            frame = 0
        else:
            frame += 1
        return frame

    def register_animation_callback(self, callback):
        self.animation_callbacks.append(callback)


animation_manager = None
def get_animation_manager(axes):
    global animation_manager
    if animation_manager is None:
        animation_manager = AnimationManager(axes)
        animation_manager.start_animation()
    return animation_manager

