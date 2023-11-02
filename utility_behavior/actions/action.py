from utility_behavior.state import State
from utility_behavior.state.needs import Needs


class Action:
    def __init__(self):
        self.needs: list[Needs] = []

    def execute(self, new_state: State):
        raise NotImplementedError

    def evaluate(self, state: State, new_state: State) -> float:
        raise NotImplementedError

    def next_states_to_evaluate(self, state: State) -> list[State]:
        raise NotImplementedError

    def __repr__(self):
        return self.__class__.__name__
