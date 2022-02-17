import time
import numpy as np
from utils.enums import Action, QTable, Rewards
from utils.constants import *
from objects.env import Environment


class Trainer:
    def __init__(
        self,
        env: Environment,
        learning_rate: float = LEARNING_RATE,
        gamma: float = GAMMA,
        exp_rate: float = EXP_RATE,
        exp_rate_decrease: float = EXP_RATE_DECREASE,
        min_exp_rate: float = EXP_RATE_MINIMUM,
        episodes: int = EPISODES,
        steps_per_episode: int = STEPS_PER_EPISODE
    ) -> None:
        self._env = env
        self._learning_rate = learning_rate
        self._gamma = gamma
        self._exp_rate = exp_rate
        self._exp_rate_decrease = exp_rate_decrease
        self._min_exp_rate = min_exp_rate
        self._episodes = episodes
        self._steps_per_episode = steps_per_episode

        self._current_episode = 0
        self._current_step = 0
        self._current_action = None
        self._current_reward = 0
        self._rewards = []

        self._q_table = {}

    @property
    def lr(self) -> float:
        return self._learning_rate

    @property
    def gamma(self) -> float:
        return self._gamma

    @property
    def exp_rate(self) -> float:
        return self._exp_rate

    @property
    def current_episode(self) -> int:
        return self._current_episode

    @property
    def current_step(self) -> int:
        return self._current_step

    @property
    def current_action(self) -> Action:
        return self._current_action

    @property
    def current_reward(self) -> float:
        return self._current_reward

    @property
    def q_table(self) -> QTable:
        return self._q_table

    @property
    def rewards(self) -> Rewards:
        return self._rewards

    @property
    def steps_per_episode(self) -> int:
        return self._steps_per_episode

    def train_loop(self) -> None:
        default_action_space = [0 for _ in self._env.actions]

        for self._current_episode in range(1, self._episodes + 1):
            state = self._env.reset()
            self._current_reward = 0

            for self._current_step in range(self._steps_per_episode):
                if np.random.uniform(0, 1) < self._exp_rate:
                    action_index = np.random.randint(len(self._env.actions))
                else:
                    action_index = np.argmax(self.q_table.get(
                        state, default_action_space))
                self._current_action = self._env.actions[action_index]

                next_state, reward, done = self._env.step(self._current_action)
                self._current_reward += reward

                # Q learning formula
                if state not in self._q_table.keys():
                    self._q_table[state] = default_action_space.copy()

                self._q_table[state][action_index] = (
                    1 - self._learning_rate) * self._q_table[state][action_index] + self._learning_rate * (
                        reward + self._gamma *
                    np.max(self._q_table.get(
                        next_state, default_action_space))
                )

                if done or self._current_step >= self._steps_per_episode:
                    break

                state = next_state
                yield time.sleep(STEP_TIME)

            self._exp_rate = max(self._min_exp_rate,
                                 np.exp(-self._exp_rate_decrease * self._current_episode))
            self._rewards.append(self._current_reward)
