import pygame
from pygame.sprite import Sprite, AbstractGroup
from utils.constants import RED, TILE_SIZE

from utils.enums import Position


class Agent(Sprite):
    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__(*groups)

        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect()
        self.image.fill(RED)

    def update_position(self, position: Position) -> None:
        self.rect.topleft = (position[0] * TILE_SIZE, position[1] * TILE_SIZE)
