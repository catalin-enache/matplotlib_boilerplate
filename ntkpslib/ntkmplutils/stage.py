
import matplotlib.pyplot as plt
from ntkmplutils import artists_manager, cfg

artists_manager.axes.hold(cfg.MAINAXE_HOLD)
artists_manager.axes.grid(cfg.MAINAXE_GRID)
artists_manager.axes.set_aspect(*cfg.MAINAXE_ASPECT)

# ========================== CALLBACKS  ================================

def scale_slider_on_changed(value):
    value = int(round(value))
    step = 10 ** (value - 1)
    value = 10 ** value

    artists_manager.axes.axis([-value, value, -value, value])
    artists_manager.axes.set_xticks(range(-value, value)[::step])
    artists_manager.axes.set_yticks(range(-value, value)[::step])
    artists_manager.axes.set_xticklabels(['' for _ in range(-value, value)[::step]])
    artists_manager.axes.set_yticklabels(['' for _ in range(-value, value)[::step]])

def widgets_events(event):
    info_widgets_events.set_text(event)

def stage_events(event):
    data = 'x: %.2f, y: %.2f' % (float(event['x']), float(event['y']))
    info_stage_events.set_text(data)

artists_manager.register_stage_event_callback('*', stage_events)

# ========================== END CALLBACKS  ================================

# ========================== INFOS ================================

info_stage_events = artists_manager.add_figure_widget('Text', 1, 1)
info_widgets_events = artists_manager.add_figure_widget('Text', 1, 865)
info_axes_events = artists_manager.add_figure_widget('Text', 1, 850)

# ========================== END INFOS ================================

# ========================== SCALE SLIDER =============================

scale_slider = artists_manager.add_figure_widget('Slider', (130, 810), 30, (1, 3), 1)
artists_manager[scale_slider]('slider_on_change', lambda event: scale_slider_on_changed(event['data']))
artists_manager[scale_slider]('slider_on_change', lambda event: widgets_events('scale: %s' % 10 ** int(event['data'])))
scale_slider.set_value(cfg.MAINAXE_SCALE)

# ========================== END SCALE SLIDER =============================

def run():
    plt.show()  # blocking main loop



