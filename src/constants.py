
from pathlib import Path

# constants
FONT_FILEPATH = Path(__file__).parent.parent / "assets" / "fonts" / "BebasNeue-Regular.ttf"

STATE_GAME     = 0
STATE_GAMEOVER = 1
STATE_PAUSE    = 2
STATE_QUIT     = 3

MAX_FPS = 60

# types of blocks
# the shape that represent that definition is
# made with @s
BLOCK_NONE = 0
BLOCK1 = 1
# @@
# @@
BLOCK2 = 2
# @@@@
BLOCK3 = 3
# @
# @@@
BLOCK4 = 4
#   @
# @@@
BLOCK5 = 5
#  @
# @@@
BLOCK6 = 6
#  @@
# @@
BLOCK7 = 7
# @@
#  @@
BLOCKS = BLOCK1, BLOCK2, BLOCK3, BLOCK4, BLOCK5, BLOCK6, BLOCK7

# block heights and widths at first rotation postition
BLOCK_HEIGHTS = 0, 2, 1, 2, 2, 2, 2, 2
BLOCK_WIDTHS  = 0, 2, 4, 3, 3, 3, 3, 3

BLOCK1_ROTS = (
    ((0,0), (1,0), (0,1), (1,1)),
    ((0,0), (1,0), (0,1), (1,1)),
    ((0,0), (1,0), (0,1), (1,1)),
    ((0,0), (1,0), (0,1), (1,1))
                )

BLOCK2_ROTS = (
    ((0,0), (1,0), (2,0), (3,0)),
    ((1,-2), (1,-1), (1,0), (1,1)),
    ((0,-1), (1,-1), (2,-1), (3,-1)),
    ((2,-2), (2,-1), (2,0), (2,1)),
                )

BLOCK3_ROTS = (
    ((0,0), (0,1), (1,1), (2,1)),
    ((1,0), (2,0), (1,1), (1,2)),
    ((0,1), (1,1), (2,1), (2,2)),
    ((1,0), (1,1), (1,2), (0,2)),
                )
BLOCK4_ROTS = (
    ((0,1), (1,1), (2,1), (2,0)),
    ((1,0), (1,1), (1,2), (2,2)),
    ((0,1), (1,1), (2,1), (0,2)),
    ((1,0), (1,1), (1,2), (0,0)),
                )
BLOCK5_ROTS = (
    ((0,1), (1,1), (2,1), (1,0)),
    ((1,0), (1,1), (1,2), (2,1)),
    ((0,1), (1,1), (2,1), (1,2)),
    ((1,0), (1,1), (1,2), (0,1)),
                )
BLOCK6_ROTS = (
    ((0,1), (1,1), (1,0), (2,0)),
    ((1,0), (1,1), (2,1), (2,2)),
    ((0,2), (1,2), (1,1), (2,1)),
    ((0,0), (0,1), (1,1), (1,2)),
                )
BLOCK7_ROTS = (
    ((0,0), (1,0), (1,1), (2,1)),
    ((2,0), (2,1), (1,1), (1,2)),
    ((0,1), (1,1), (1,2), (2,2)),
    ((1,0), (1,1), (0,1), (0,2)),
                )

BLOCKS_ROTS = (((),), BLOCK1_ROTS, BLOCK2_ROTS, BLOCK3_ROTS,
    BLOCK4_ROTS, BLOCK5_ROTS, BLOCK6_ROTS, BLOCK7_ROTS)

# blocks' colors
'''
COLOR_BLOCK = (
    0x00141414,      # Empty block (kept as your default)
    (255, 104, 104), # Soft Red
    (133, 232, 157), # Mint Green
    (115, 157, 242), # Muted Blue
    (241, 230, 141), # Soft Yellow
    (198, 120, 221), # Lavender / Purple
    (100, 219, 237), # Soft Cyan
    (235, 162, 115)  # Pastel Orange
)

COLOR_FONT       = 248, 248, 242 # Off-white (softer on the eyes than pure 255,255,255)
COLOR_BACKGROUND =  30,  30,  40 # Very dark blue/charcoal
COLOR_PANEL      =  40,  42,  54 # Slightly lighter charcoal for the side panel
COLOR_GRID       =  55,  55,  70 # Subtle gray/blue for the grid lines
'''
COLOR_BLOCK = (
    0x00141414,
    (224, 108, 117),
    (152, 195, 121),
    (97, 175, 239),
    (229, 192, 123),
    (198, 120, 221),
    (86, 182, 194),
    (209, 154, 102)
)
COLOR_FONT       = 171, 178, 191
COLOR_BACKGROUND =  33,  37,  43
COLOR_PANEL      =  40,  44,  52
COLOR_GRID       =  59,  64,  72
