from random import random

from utility_behavior.state import State
from utility_behavior.state.needs import Needs

from .action import Action


class DribbleAction(Action):
    def __init__(self):
        self.needs: list[Needs] = [Needs.ABLE_TO_MOVE, Needs.CURRENTLY_STANDING]

    def evaluate(self, state: State, newState: State) -> float:
        return random()

    def next_states_to_evaluate(self, state: State) -> list[State]:
        return [State.random() for _ in range(100)]
