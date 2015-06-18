from matplotlib.animation import Animation
from matplotlib.patches import PathPatch

# The rest of the code in this class is to facilitate easy blitting
def _blit_draw(self, artists, bg_cache):
    # Handles blitted drawing, which renders only the artists given instead
    # of the entire figure.
    updated_axes_or_figs = []
    for a in artists:
        # If we haven't cached the background for this axes object, do
        # so now. This might not always be reliable, but it's an attempt
        # to automate the process.
        axe_or_fig = a.axes or a.figure
        if axe_or_fig not in bg_cache:
            bg_cache[axe_or_fig] = a.figure.canvas.copy_from_bbox(axe_or_fig.bbox)
        axe_or_fig.draw_artist(a)
        updated_axes_or_figs.append(axe_or_fig)

    # After rendering all the needed artists, blit each axes individually.
    for axe_or_fig in set(updated_axes_or_figs):
        (axe_or_fig.figure or axe_or_fig).canvas.blit(axe_or_fig.bbox)

def _blit_clear(self, artists, bg_cache):
    # Get a list of the axes that need clearing from the artists that
    # have been drawn. Grab the appropriate saved background from the
    # cache and restore.
    axes_or_figs = set(a.axes or a.figure for a in artists)
    for ax_or_fig in axes_or_figs:
        (ax_or_fig.figure or ax_or_fig).canvas.restore_region(bg_cache[ax_or_fig])


def path_patch_to_string(self):
    return "PathPatch ((%g, %g) ...)" % tuple(self._path.vertices[0])

Animation._blit_clear = _blit_clear
Animation._blit_draw = _blit_draw
PathPatch.__str__ = path_patch_to_string
