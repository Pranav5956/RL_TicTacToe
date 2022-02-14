from typing import Any
import pygame
from constants import *

debug_messages = {}


def debug(key: str = "DEBUG", message: Any = "Debug Message"):
    if key not in debug_messages.keys():
        try:
            debug_messages[key] = key + " : " + str(message)
        except TypeError:
            debug_messages[key] = key + " : [UNDEFINED]"

    # Get dimensions of debug texts
    debug_displays = []
    debug_max_text_width = -1
    debug_text_height = 0
    for debug_message_key in sorted(debug_messages.keys()):
        debug_surf = DEBUG_FONT.render(
            debug_messages[debug_message_key], True, WHITE)
        debug_displays.append(debug_surf)

        width, height = debug_surf.get_size()
        debug_text_height += height
        if width > debug_max_text_width:
            debug_max_text_width = width

    # Draw the debug box
    display_surf = pygame.display.get_surface()
    debug_box_rect = pygame.Rect(
        DEBUG_HORIZONTAL_MARGIN,
        DEBUG_VERTICAL_MARGIN,
        debug_max_text_width + DEBUG_HORIZONTAL_PADDING * 2,
        debug_text_height + DEBUG_VERTICAL_SPACING *
        (len(debug_displays) - 1) + DEBUG_VERTICAL_PADDING * 2
    )
    pygame.draw.rect(display_surf, BLACK, debug_box_rect)

    # Draw the debug texts
    previous_y = DEBUG_VERTICAL_MARGIN + DEBUG_VERTICAL_PADDING
    for i in range(len(debug_displays)):
        debug_surf = debug_displays[i]
        debug_rect = debug_surf.get_rect(
            topleft=(
                DEBUG_HORIZONTAL_MARGIN + DEBUG_HORIZONTAL_PADDING,
                previous_y
            )
        )
        previous_y += debug_rect.height + DEBUG_VERTICAL_SPACING
        display_surf.blit(debug_surf, debug_rect)
