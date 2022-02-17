import numpy as np
from objects.agent import Agent
from objects.env import Environment
import pygame
from objects.tile import Tile
from objects.trainer import Trainer

from utils.constants import *
from utils.debug import debug
from utils.enums import TileType


class Game:
    def __init__(self, caption: str = "Test") -> None:
        pygame.init()
        self._screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.SRCALPHA)
        self._clock = pygame.time.Clock()
        self._running = True

        self._tile_sprite_group = pygame.sprite.Group()
        self._entity_sprite_group = pygame.sprite.Group()

        self._maze_tiles = [
            [Tile((row * TILE_SIZE, col * TILE_SIZE), TileType.WALL, self._tile_sprite_group)
             for col in range(TILE_COL_COUNT)]
            for row in range(TILE_ROW_COUNT)
        ]
        self._agent = Agent(self._entity_sprite_group)
        self._env = Environment(self._maze_tiles, self._agent)
        self._trainer = Trainer(self._env)

        pygame.display.set_caption(caption)
        self._train_loop = self._trainer.train_loop()
        self._training_completed = False

    def __run_training_loop(self) -> None:
        try:
            self._train_loop.__next__()
        except StopIteration:
            self._training_completed = True
            print("Training completed!")

    def run(self) -> None:
        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False

            self._screen.fill(WHITE)

            ticks = self._clock.tick(MAX_FPS)
            fps = 1000 / ticks
            # delta_time = 1 / fps

            if not self._training_completed:
                self.__run_training_loop()

            # Draw the sprites
            self._tile_sprite_group.draw(self._screen)
            self._entity_sprite_group.draw(self._screen)

            # Debug messages
            debug("FPS", round(fps, 4))
            debug("Observations", self._env.observations)
            debug("Episode", self._trainer.current_episode)
            debug(
                "Step", f"{self._trainer.current_step}/{self._trainer.steps_per_episode}")
            debug("Learning Rate", round(self._trainer.lr, 4))
            debug("Discount Factor", round(self._trainer.gamma, 4))
            debug("Exploration Rate", round(self._trainer.exp_rate, 4))
            debug("Current Action", self._trainer.current_action.name)
            debug("Current Reward", round(self._trainer.current_reward, 4))
            debug("Mean Reward", round(
                np.mean(self._trainer.rewards or [0]), 4))

            pygame.display.update()

        pygame.quit()
