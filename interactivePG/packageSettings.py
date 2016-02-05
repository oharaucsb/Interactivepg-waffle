import itertools as itt
from pyqtgraph import intColor


config_options = {
    "selectionThickness": 3,
    "axisFontSize": 10,
    "axisLabelFontSize": 50,
    "axisThickness": 5,
    "axisTickLength": -20,
    "legendFontSize": 50,
    "boundedAxes": True,
    "background": 'w',
    "foreground": 'k',
    "standardColors": [
        'b', 'g', 'r', 'c', 'k', 'm'
    ], # if int, will step through colors using pg.intColor
                         # if list, will step through the list of colors
    "standardLineshapes": 4, # ints are passed for Qt pen styles. How many linestyles
                        # should be cycled when no args are passed
    "linestyleChars": ['_', '-', '--', '.', '-.', '-..'], # characeter codes used for passing
                    #string to specify line style
    "linewidth": 3,
    "errorBarCapWidth": 0.0
}
