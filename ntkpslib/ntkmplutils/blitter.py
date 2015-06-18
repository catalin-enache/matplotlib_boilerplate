

class Blitter(object):
    def __init__(self):
        self.background = None
        self.registered_callbacks = {}

    def on_start(self, artist):
        self.registered_callbacks.get('on_start', lambda *args: None)('on_start', artist)
        figure, axes, canvas = artist.figure, artist.axes, artist.figure.canvas
        figure_or_axes = axes if axes else figure
        # draw everything but the selected rectangle
        artist.set_animated(True)
        canvas.draw()
        # store the pixel buffer
        self.background = canvas.copy_from_bbox(figure_or_axes.bbox)
        # now redraw just the rectangle
        figure_or_axes.draw_artist(artist)
        # and blit just the redrawn area
        canvas.blit(figure_or_axes.bbox)

    def on_animate(self, artist):
        self.registered_callbacks.get('on_animate', lambda *args: None)('on_animate', artist)
        figure, axes, canvas = artist.figure, artist.axes, artist.figure.canvas
        figure_or_axes = axes if axes else figure
        # restore the background region
        canvas.restore_region(self.background)
        # redraw just the current rectangle
        figure_or_axes.draw_artist(artist)
        # blit just the redrawn area
        canvas.blit(figure_or_axes.bbox)

    def on_end(self, artist):
        self.registered_callbacks.get('on_end', lambda *args: None)('on_end', artist)
        # turn off the rect animation property
        artist.set_animated(False)
        # reset the background
        self.background = None
        # redraw the full figure
        artist.figure.canvas.draw()

    def register_callback(self, name, callback):
        self.registered_callbacks[name] = callback