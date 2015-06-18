

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import numpy as np
import math


x = list(np.arange(-9.0, 9.0, 0.1))

# ============================= FIG 1 ========================================================

fig = plt.figure(1)  # make window instance, also mark this as current, return matplotlib.figure.Figure # http://matplotlib.org/api/figure_api.html#matplotlib.figure.Figure
ax = fig.add_subplot(111)  # add subplot in  window instance, return matplotlib.axes._subplots.AxesSubplot # http://matplotlib.org/api/axes_api.html#matplotlib.axes.Axes
# ax_ = plt.subplot(111) # ax is ax_ is plt.gca() => True

# fig2 = plt.figure(2) # another window instance, also mark this as current
# ax2 = fig2.add_subplot(111) # add subplot in second window instance
# ax2_ = plt.subplot(111) # # ax2 is ax2_ is plt.gca() => True

# plt.figure(1) # mark fig 1 as current, forward plt commands will refer to this # fig is plt.gcf() => True


def motion_notify_event(event):
	txt.set_text('%.2f %.2f' % (event.xdata or 0, event.ydata or 0))
	txt.set_position((event.xdata or 0, event.ydata or 0))
	
	# txt.figure is fig # True
	
	# txt.figure.canvas.draw() # slow
	
	# Better optimised alternative to t.figure.canvas.draw() but lower level than FuncAnimation use
	# txt.figure.canvas.restore_region(background) # fig.canvas.restore_region(background)  #  http://matplotlib.org/users/event_handling.html?highlight=restore_region  # http://stackoverflow.com/questions/11002338/how-do-i-re-draw-only-one-set-of-axes-on-a-figure-in-python    
	# txt.axes.draw_artist(t) # ax.draw_artist(txt)
	# txt.figure.canvas.blit(txt.axes.bbox) # fig.canvas.blit(ax.bbox)
	
	# Much better alternative to t.figure.canvas.draw() is to use FuncAnimation (see later)


# FuncAnimation
def animate(i):
	return txt,  # required by FuncAnimation to know what to blit


# FuncAnimation
def init():
	return txt,


ax.hold(True)  # old plots are kept (drown over previous) # all drown lines are kept in axes.lines
ax.grid(True)  # show grid
ax.axis([-10, 10, -10, 10])  # set plot dimensions # xlim(), ylim() also can be used


ax.set_aspect('equal', 'box')  # plt.axes().set_aspect('equal', 'box') # constrain aspect-ratio / proportion
ax.set_title('Simple plot')  # plt.title('Simple plot')
ax.set_xlabel('This is the X axis')  # plt.xlabel('This is the X axis') # passes the information on the Text instance of the XAxis. XAxis is a property of axes and is itself a container
ax.set_ylabel('This is the Y axis')  # plt.ylabel('This is the Y axis')
ax.set_xticks(range(-10,10))  # plt.xticks(range(-10,10)) # how many ticks to be
ax.set_yticks(range(-10,10))  # plt.yticks(range(-10,10))


line, = ax.plot(x, [math.sin(xi*1.0) for xi in x], '-r')  # opt: label='Label 1'   . : - --      . , o V ^ < > 1 2 3 4 s p  * h H + X D d _ |
# ax.fill(x, [math.sin(xi*1.0) for xi in x], '-ro')
# theta = np.arange(0., 2., 1./180.)*np.pi
# ax.polar(3*theta, theta/5);
txt = ax.text(1, 1, 'hello')
txt.set_animated(True)  # hint that this will be animated

# fig.canvas.draw() # !!!!!!!! important for figure.canvas.restore_region(background) to work
# background = fig.canvas.copy_from_bbox(ax.bbox) # copy current drawing => what will not change

cid = fig.canvas.mpl_connect('motion_notify_event', motion_notify_event)
# fig.canvas.mpl_disconnect(cid)
anim = FuncAnimation(fig, animate, init_func=init, interval=0, frames=100, blit=True) 

# print ax.lines[0] is line # True
# ax.lines.remove(line) # 


# ============================= FIG 2 ========================================================

fig2 = plt.figure(2, figsize=(10, 10), frameon=False)
# print matplotlib.artist.getp(fig2)
# print matplotlib.artist.getp(fig2.patch)
fig2.patch.set(facecolor=(0.75, 0.75, 0, 0.3))  # set_fc, set_facecolor, set(fc=), set(facecolor=)

# we can draw directly on fig (see below) but usually we prefer to draw on axes
l1 = matplotlib.lines.Line2D([0, 1], [0, 1], transform=fig2.transFigure, figure=fig2)
l2 = matplotlib.lines.Line2D([0, 1], [1, 0], transform=fig2.transFigure, figure=fig2)
fig2.lines.extend([l1, l2])
fig2.canvas.draw()	



ax2 = fig2.add_subplot(111)  # ax2 is also appended in fig2.axes
# ax3 = fig2.add_axes([0.1, 0.1, 0.7, 0.3])  # ax3 is also appended in fig2.axes
for a in fig2.axes: a.grid(True)
ax2.patch.set(fc=(0.75, 0, 0.75, 0.3))  # set color for axe background rect
# ax3.patch.set(fc=(0, 0.75, 0.75, 0.1))
ax2.axis([-10, 10, -10, 10])
ax2.set_aspect('equal', 'box')
l3, = ax2.plot([0, 1], [2, 4], '-ro', linewidth=2)


rect = matplotlib.patches.Rectangle((0, 0), width=5, height=5)
circ = matplotlib.patches.Circle((0.0, 0.0), 1, facecolor='g', alpha=0.5)
l4 = matplotlib.lines.Line2D(range(10), np.sin(range(10)), color='r')  # http://matplotlib.org/api/lines_api.html#matplotlib.lines.Line2D
l4.set_data(range(10), np.cos(range(10)))  # we change our mind and modify l4 data | think animation
ax2.add_patch(rect)  # add_artist, add_callback, add_collection, add_container, add_image, add_line, add_patch, add_table
ax2.add_patch(circ)
ax2.add_line(l4)
# ax2.figure.canvas.draw()
# print matplotlib.artist.getp(ax2)
# print ax2.xaxis.get_ticklocs()
# print matplotlib.artist.getp(ax2.xaxis)


# !!! draw stuff !!!
ax2.arrow(-5, 0, 5, 5)  # !plot(Line2D)!, !fill(Polygon)!, !imshow(imgdata)!   ?matshow? !text!, ?table?, ...      fill_between, fill_betweenx, arrow, pie, axhline, axhspan, axvline, axvspan, bar, angle_spectrum, plot_date, barbs, barh, boxplot, broken_barh, bxp, contour, contourf, csd, errorbar, eventplot, hexbin, hist, hist2d, hlines, magnitude_spectrum, pcolor, pcolorfast, pcolormesh, phase_spectrum, psd, quiver, scatter, semilogx, semilogy, specgram, spy, stackplot, stem, step, streamplot, tricontour, tricontourf, tripcolor, triplot, violin, violinplot, vlines, xcorr
ax2.fill([0, -1, -1, 0], [0, 0, -1, -1], fc='yellow', alpha=0.4)

# http://matplotlib.org/api/backend_bases_api.html#matplotlib.backend_bases.LocationEvent
# http://matplotlib.org/users/event_handling.html
def onclick(event):
	print 'circ.contains(event)', circ.contains(event)
	print 'l4.contains(event)', l4.contains(event)
	# print 'name=%s, canvas=%s, guiEvent=%s, button=%d, x=%d, y=%d, xdata=%f, ydata=%f, inaxes=%s' % (event.name, event.canvas, event.guiEvent, event.button, event.x or 0, event.y or 0, event.xdata or 0, event.ydata or 0, event.inaxes)

cid2 = fig2.canvas.mpl_connect('button_press_event', onclick)

axfreq = plt.axes([0.2, 0.05, 0.6, 0.01]) # [left, bottom, width, height] in normalized (0, 1) units
sl = matplotlib.widgets.Slider(axfreq, '1', -1, 1, 0.5)

ayfreq = plt.axes([0.2, 0.03, 0.6, 0.01]) # [left, bottom, width, height] in normalized (0, 1) units
s2 = matplotlib.widgets.Slider(ayfreq, '2', -1, 1, 0.5)



# ============================= Cheats ========================================================

# other Artist methods:
# bbox = artist.get_window_extent() # return bbox around artist
# highlight = matplotlib.patches.Rectangle(xy=bbox.min, width=bbox.width, height=bbox.height, alpha=0.3, color='yellow')

# other important axes methods:
# - add_artist(a) Use add_artist only for artists for which there is no dedicated add method
# - add_callback(f)
# - add_collection(collection, autolim=True)
# - add_container(container)
# - add_image(image)
# - add_line(line)
# - add_patch(p)
# - add_table(tab)

# - apply_aspect(position=None)
# - autoscale(enable=True, axis='both', tight=None)

# - axis(*v, **kwargs)

# - cla(): Clear the current axes.
# - clear(): clear the axes

# - contains(mouseevent)
# - contains_point(point)

# - start_pan(x, y, button): Called when a pan operation has started.
# - drag_pan(button, key, x, y): Called when the mouse moves during a pan operation.
# - end_pan(): Called when a pan operation completes (when the mouse button is up.)

# - draw(artist, renderer, *args, **kwargs): Draw everything (plot lines, axes, labels)
# - draw_artist(a): This method can only be used after an initial draw which caches the renderer. It is used to efficiently update Axes data (axis ticks, labels, etc are not updated)

# - get_figure(): Return the Figure instance the artist belongs to
# - get_axes(): Return the Axes instance the artist resides in, or None
# - get_children(): return a list of child artists
# - get_contains(): Return the _contains test used by the artist, or None for default.
# - get_images(): return a list of Axes images contained by the Axes
# - get_lines(): Return a list of lines contained by the Axes
# - get_picker(): Return the picker object used by this artist

# - grid(b=None, which=u'major', axis=u'both', **kwargs)

# - has_data(): Return True if any artists have been added to axes.


# - findobj(match=None, include_self=True): Find artist objects. Recursively find all Artist instances contained in self.
# - hitlist(event): List the children of the artist which contain the mouse event event.
# - hold(True) / ishold(): When hold is True, subsequent plot commands will be added to the current axes.
# - in_axes(mouseevent): Return True if the given mouseevent (in display coords) is in the Axes
# - pick(mouseevent): each child artist will fire a pick event if mouseevent is over the artist and the artist has picker set
# - pickable(): Return True if Artist is pickable.
# - properties()
# - redraw_in_frame():  It is used to efficiently update Axes data (axis ticks, labels, etc are not updated)
# - remove_callback(oid)
# - set_anchor(anchor)
# - set_picker(picker)
# - set_zorder(level)
# - twinx()
# - twiny()
# - update(props) | update_from(other)



# line, = ax.plot(...) # return Line2D
# print plt.setp(line) # see what Line2D props can be setup for lines
# plt.setp(line, ydata=[2,4,6,8], xdata=[0,1,2,3]) # setup Line2D props # http://matplotlib.org/api/lines_api.html#matplotlib.lines.Line2D
# line.set_data(xdata, ydata)
# see: set line props:  http://matplotlib.org/users/pyplot_tutorial.html#controlling-line-properties

# plt.gcf() # get current figure # can be changed with plt.figure(int)
# plt.gca() # get current axes
# plt.clf() # clear current figure
# plt.cla() # clear current axes

# plt.legend(['L1', 'L2', 'L3'], loc='lower left') # loc: (best, upper|lower|center/right|left|center)

# plt.savefig('plot123.svg') # opt: dpi=200, transparent=True,

# mpl.interactive(True)
# isinteractive(): Returns True or False, the value of interactive property
# ion(): Enables interactive mode
# ioff(): Disables interactive mode
# draw(): Forces a figure canvas redraw | is expensive

# ; suppress function output ex: plt.plot([2, 1]);

# matplotlib.rcParams # dict that shows configuration | mpl.rcParams['<param name>'] = <value>
# matplotlib.rcdefaults(): Restores Matplotlib's default configuration parameters values
# matplotlib.rc(): Sets multiple settings in a single command ex: mpl.rc(('figure', 'savefig'), facecolor='r')

# mpl.use (...) must be called right after importing matplotlib for the first time
# ex: mpl.use('Agg') # to render to file, or to not use a graphical display
# ex: mpl.use('GTKAgg') # to render to a GTK UI window

# f, ax = plt.subplots() # quick creating one fig with one subplot #  http://matplotlib.org/api/pyplot_api.html?highlight=subplots#matplotlib.pyplot.subplots


# artists tut: http://matplotlib.org/users/artists.html ! http://matplotlib.org/api/artist_api.html#matplotlib.artist.Artist


# Containers: Figure => Axes => Axis(xaxis,yaxis) => Tick

# fig props:  http://matplotlib.org/api/figure_api.html#matplotlib.figure.Figure
# fig.patch, ax.patch # surrounding Rectangle
# fig.axes # contains axes added by add_subplot

# axes props: http://matplotlib.org/api/axes_api.html#matplotlib.axes.Axes
# ax.patch.set(facecolor=(0,0.60,0), alpha=0.3)

# http://matplotlib.org/api/axis_api.html#matplotlib.axis.Axis
# http://matplotlib.org/api/axis_api.html#matplotlib.axis.Tick

# http://matplotlib.org/api/lines_api.html

# http://matplotlib.org/api/patches_api.html

# http://matplotlib.org/api/path_api.html#matplotlib.path.Path

# http://matplotlib.org/devel/transformations.html

# http://matplotlib.org/api/widgets_api.html

# http://matplotlib.org/api/markers_api.html

# http://matplotlib.org/api/animation_api.html

# http://matplotlib.org/api/index_backend_api.html

# http://matplotlib.org/api/cm_api.html

# http://matplotlib.org/api/colors_api.html

'''
multiple figs and subplots
import matplotlib.pyplot as plt
plt.figure(1)                # the first figure
plt.subplot(211)             # the first subplot in the first figure
plt.plot([1,2,3])
plt.subplot(212)             # the second subplot in the first figure
plt.plot([4,5,6])


plt.figure(2)                # a second figure
plt.plot([4,5,6])            # creates a subplot(111) by default

plt.figure(1)                # figure 1 current; subplot(212) still current
plt.subplot(211)             # make subplot(211) in figure1 current
plt.title('Easy as 1,2,3')   # subplot 211 title
'''

'''
matplotlib.Figure:
def get_children(self):
		'get a list of artists contained in the figure'
		children = [self.patch]
		children.extend(self.artists)
		children.extend(self.axes)
		children.extend(self.lines)
		children.extend(self.patches)
		children.extend(self.texts)
		children.extend(self.images)
		children.extend(self.legends)
		return children
'''

'''
matplotlib.axes._base
def get_children(self):
		"""return a list of child artists"""
		children = []
		children.append(self.xaxis)
		children.append(self.yaxis)
		children.extend(self.lines)
		children.extend(self.patches)
		children.extend(self.texts)
		children.extend(self.tables)
		children.extend(self.artists)
		children.extend(self.images)
		if self.legend_ is not None:
			children.append(self.legend_)
		children.extend(self.collections)
		children.append(self.title)
		children.append(self._left_title)
		children.append(self._right_title)
		children.append(self.patch)
		children.extend(six.itervalues(self.spines))
		return children
'''

'''
Events: http://matplotlib.org/api/backend_bases_api.html#matplotlib.backend_bases.LocationEvent

'button_press_event'	MouseEvent - mouse button is pressed
'button_release_event'	MouseEvent - mouse button is released
'draw_event'	DrawEvent - canvas draw
'key_press_event'	KeyEvent - key is pressed
'key_release_event'	KeyEvent - key is released
'motion_notify_event'	MouseEvent - mouse motion
'pick_event'	PickEvent - an object in the canvas is selected
'resize_event'	ResizeEvent - figure canvas is resized
'scroll_event'	MouseEvent - mouse scroll wheel is rolled
'figure_enter_event'	LocationEvent - mouse enters a new figure
'figure_leave_event'	LocationEvent - mouse leaves a figure
'axes_enter_event'	LocationEvent - mouse enters a new axes
'axes_leave_event'	LocationEvent - mouse leaves an axes
'''



# =============================================================================================

plt.show()



