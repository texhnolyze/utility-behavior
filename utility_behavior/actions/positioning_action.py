import math
from random import random

from utility_behavior.state import State
from utility_behavior.state.needs import Needs

from .action import Action


class PositioningAction(Action):
    def __init__(self):
        self.needs: list[Needs] = [Needs.ABLE_TO_MOVE, Needs.CURRENTLY_STANDING]

    def evaluate(self, state: State, newState: State) -> float:
        total = 0
        highest = 0
        for x in range(1, 3001):
            result = math.sin(x / 1000) ** (x / 1000)
            total += result
            highest = max(result, highest)

        return total / highest

    def next_states_to_evaluate(self, state: State) -> list[State]:
        return [State.random() for _ in range(1000)]
