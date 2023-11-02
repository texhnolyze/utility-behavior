from __future__ import annotations
from typing import Optional
from random import random


class Pose:
    x: float
    y: float
    z: float
    theta: float

    def __init__(
        self, x: float = 0.0, y: float = 0.0, z: float = 0.0, theta: float = 0.0
    ):
        self.x = x
        self.y = y
        self.z = z
        self.theta = theta

    def __str__(self):
        return f"Pose(x: {self.x}, y: {self.y}, z: {self.z}, θ: {self.theta})"

    def __repr__(self):
        return str(self)


class State:
    pose: Pose
    cmd_vel: float

    def __init__(self, cmd_vel: float = 0.0, pose: Optional[Pose] = None):
        self.pose = pose or Pose()
        self.cmd_vel = cmd_vel

    @classmethod
    def random(cls) -> State:
        return State(random(), Pose(random(), random(), random(), random()))

    def __str__(self):
        return f"State(cmd_vel: {self.cmd_vel}, pose: {str(self.pose)})"

    def __repr__(self):
        return str(self)
