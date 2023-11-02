from pprint import pprint
from typing import Iterable, Tuple

import itertools
import functools

from .actions import ALL_ACTIONS, Action
from .state import Pose, State
from .state.needs import Needs

from .execution.thread_pool import ThreadPoolExecutor
from .execution.process_pool import ProcessPoolExecutor


Evaluation = Tuple[Action, list[State]]
EvaluationResult = Tuple[Action, State, float]


class Evaluator:
    def __init__(self, state: State):
        self.state = state

    def evaluate(self, evaluation: Evaluation) -> EvaluationResult:
        results = self.evaluate_new_states(evaluation)
        return max(results, key=lambda item: item[2])

    def evaluate_new_states(self, evaluation: Evaluation) -> Iterable[EvaluationResult]:
        action, new_states = evaluation
        return map(
            lambda state: (action, state, action.evaluate(self.state, state)),
            new_states,
        )


class ActionDecider:
    def __init__(self):
        self.actions = ALL_ACTIONS
        self.max_parallel_states = 4

        #  max_workers = int(len(ALL_ACTIONS) * self.max_parallel_states / 2)
        #  self.executor = ThreadPoolExecutor(4)
        #  self.executor = ProcessPoolExecutor(6)

        self.next_action: EvaluationResult = (None, None, 0)
        self.state = State(cmd_vel=1.0, pose=Pose(1, 1, 0))
        self.evaluator = Evaluator(self.state)
        self.fulfilled_needs: list[Needs] = [
            Needs.ABLE_TO_MOVE,
            Needs.CURRENTLY_STANDING,
        ]

    def decide(self):
        def flat_map(f, xs):
            return functools.reduce(lambda a, b: itertools.chain(a, b), map(f, xs))

        possible_actions = filter(
            lambda a: self.fulfilled_needs <= a.needs, self.actions
        )
        needed_evaluations = flat_map(
            self.split_into_evaluation_parts, possible_actions
        )

        #  async execution with thread or process pool
        #  split_results = self.async_evaluation(needed_evaluations)

        # sync execution
        split_results = self.sync_evaluation(needed_evaluations)

        ideal_action = max(split_results, key=lambda item: item[2])
        self.next_action = ideal_action

        #  pprint(
        #  f"Ideal action: {ideal_action[0]}, max_score: {ideal_action[2]}, {ideal_action[1]})"
        #  )

    def async_evaluation(
        self, evaluations: Iterable[Evaluation]
    ) -> list[EvaluationResult]:
        return self.executor.map(self.evaluator.evaluate, evaluations)

    def sync_evaluation(
        self, evaluations: Iterable[Evaluation]
    ) -> list[EvaluationResult]:
        split_results: list[EvaluationResult] = []

        for action, states in evaluations:
            split_results.append(self.evaluator.evaluate((action, states)))

        return split_results

    def split_into_evaluation_parts(self, action: Action) -> Iterable[Evaluation]:
        new_states = action.next_states_to_evaluate(self.state)
        parts = [
            new_states[i : i + self.max_parallel_states]
            for i in range(0, len(new_states), self.max_parallel_states)
        ]
        return map(lambda part: (action, part), parts)
