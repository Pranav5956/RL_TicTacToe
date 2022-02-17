import pygame
from pygame.sprite import *

from utils.constants import *
from utils.enums import Position, TileType


class Tile(Sprite):
    TRANSPARENT_TILES = [TileType.VISITED, TileType.CROSSED]

    def __init__(self, position: Position, tile_type: TileType = TileType.EMPTY, *groups: AbstractGroup) -> None:
        super().__init__(*groups)

        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=position)

        self._tile_type = tile_type
        self._tile_color = None

        self.__update_tile_color()

    def __update_tile_color(self) -> None:
        if self._tile_type is TileType.EMPTY:
            self._tile_color = WHITE
        elif self._tile_type is TileType.VISITED:
            self._tile_color = GREEN
        elif self._tile_type is TileType.CROSSED:
            self._tile_color = RED
        elif self._tile_type is TileType.START:
            self._tile_color = CYAN
        elif self._tile_type is TileType.END:
            self._tile_color = BLUE
        elif self._tile_type is TileType.COIN:
            self._tile_color = WHITE
        else:
            self._tile_color = BLACK

        self.image.fill(self._tile_color)
        self.image.set_alpha(
            90 if self._tile_type in Tile.TRANSPARENT_TILES else 255)

        if self.tile_type is TileType.COIN:
            pygame.draw.ellipse(
                self.image, RED, (TILE_SIZE // 4, TILE_SIZE // 6, TILE_SIZE // 2, (TILE_SIZE * 4) // 6))

    @property
    def tile_type(self) -> TileType:
        return self._tile_type

    @tile_type.setter
    def tile_type(self, tile_type: TileType = TileType.EMPTY):
        self._tile_type = tile_type
        self.__update_tile_color()

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)
