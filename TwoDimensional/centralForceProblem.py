import numpy as np

from .orbits import Orbit2D
from constants import Earth, Body
from .animate import AnimatedSimulation2D
from .state import State2D


def centralForceProblem(central_body: Body, orbiter_body: Body, t_end, dt):
    orbit = Orbit2D(central_body, orbiter_body.initial_state)

    t = 0
    traj_body = []
    time_vec = []

    while t < t_end:
        orbit.propagate(dt)
        orb = orbit.state.copy(form='cartesian')
        traj_body.append(orb)
        time_vec.append(t)

        t += dt

    central_body.motion = 'static'
    central_body.traj = [0, 0]
    orbiter_body.motion = 'moving'
    orbiter_body.traj = traj_body

    animation = AnimatedSimulation2D(time_vec, [central_body, orbiter_body])
    animation.show()
