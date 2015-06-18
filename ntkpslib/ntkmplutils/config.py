
RENDERER = 'qt'  # tk qt

FIGSIZE = (11, 11)
MAINAXE_POSITION = [0.1, 0.2, 0.8, 0.7]  # [left, bottom, width, height] in normalized (0, 1) units
MAINAXE_HOLD = True
MAINAXE_GRID = True
MAINAXE_ASPECT = ('equal', 'box')
MAINAXE_SCALE = 1  # 1 | 2 | 3 / for 10 100 1000
MAINAXE_POLAR = False


ANIMATION = True
ANIMATION_FRAMES = 100
ANIMATION_INTERVAL = 10  # interval=10 allow other friends (ex: matplotlib.sliders) to draw_idle()