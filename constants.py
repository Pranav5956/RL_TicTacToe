from pygame.color import Color
from pygame.font import Font, init as initialize_fonts

initialize_fonts()

# Display settings
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 360
FPS = 30

# Colors
BLACK = Color(0, 0, 0)
WHITE = Color(255, 255, 255)

# Debug Settings
DEBUG_FONT = Font(None, 22)
DEBUG_HORIZONTAL_MARGIN = 5
DEBUG_VERTICAL_MARGIN = 5
DEBUG_HORIZONTAL_PADDING = 5
DEBUG_VERTICAL_PADDING = 5
DEBUG_VERTICAL_SPACING = 3
