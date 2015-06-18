
# http://matplotlib.1069221.n5.nabble.com/Matplotlib-drag-overlapping-points-interactively-td42847.html

import matplotlib
matplotlib.use('Qt4Agg')  # Qt4Agg TkAgg
print matplotlib.get_backend()

import matplotlib.pyplot as plt
import matplotlib.patches as patches


class DraggablePoints(object):
    def __init__(self, artists):
        for artist in artists:
            artist.set_picker(True)
        self.artists = artists
        self.currently_dragging = False
        self.current_artist = None
        self.offset = (0, 0)

        for canvas in set(artist.figure.canvas for artist in self.artists):
            canvas.mpl_connect('button_press_event', self.on_press)
            canvas.mpl_connect('button_release_event', self.on_release)
            canvas.mpl_connect('pick_event', self.on_pick)
            canvas.mpl_connect('motion_notify_event', self.on_motion)


    def on_press(self, event):
        self.currently_dragging = True

    def on_release(self, event):
        self.currently_dragging = False
        self.current_artist = None

    def on_pick(self, event):
        if self.current_artist is None:
            self.current_artist = event.artist
            x0, y0 = event.artist.center
            x1, y1 = event.mouseevent.xdata, event.mouseevent.ydata
            self.offset = (x0 - x1), (y0 - y1)

    def on_motion(self, event):
        if not self.currently_dragging:
            return
        if self.current_artist is None:
            return
        dx, dy = self.offset
        self.current_artist.center = event.xdata + dx, event.ydata + dy
        text.set_text('x: %.3f | y: %.3f' % (self.current_artist.center[0], self.current_artist.center[1]))
        self.current_artist.figure.canvas.draw()

if __name__ == '__main__':

    fig, ax = plt.subplots()
    plt.axis('equal')
    ax.set(xlim=[-5, 5], ylim=[-5, 5])

    text = plt.text(-4, 4, "Some text")

    circles = [patches.Circle((0.0, 0.0), 0.1, facecolor='g', alpha=0.5),
               patches.Circle((1.0, 1.0), 0.1, facecolor='y', alpha=0.5)]
    
    for circ in circles:
        ax.add_patch(circ)

    dr = DraggablePoints(circles)
    plt.show()


