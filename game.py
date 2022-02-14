import pygame

from constants import *
from debug import debug


class Game:
    def __init__(self, caption: str = "Test") -> None:
        pygame.init()
        self._screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.SRCALPHA)
        self._clock = pygame.time.Clock()
        self._running = True

        pygame.display.set_caption(caption)

    def run(self) -> None:
        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False

            self._screen.fill(WHITE)
            debug("Test Parameter", "Test value")
            pygame.display.update()
            self._clock.tick(FPS)

        pygame.quit()
