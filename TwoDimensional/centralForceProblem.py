import numpy as np

from .orbits import Orbit2D
from constants import Earth
from .animate import AnimatedSimulation2D


def centralForceProblem(a,e,t_end,dt,orbiter,central,ν0=0):
    orbit = Orbit2D(a,e,Earth,ν0)

    t = 0
    trajectory_orbiter = []
    trajectory_central = [0, 0] #xy coordinates of ellipse focus
    time_vector = []

    while(t < t_end):
        orbit.propagate(dt)
        (x,y) = orbit.getXYcoordinates()
        trajectory_orbiter.append([x,y])


        t += dt
        time_vector.append(t)

    central.trajectory = trajectory_central
    central.motion = "static"
    central.color = 'blue'
    orbiter.trajectory = trajectory_orbiter
    orbiter.motion = "moving"
    orbiter.color = 'black'

    _all = np.array(trajectory_orbiter).flatten()
    dim = abs(max(_all.min(), _all.max(), key=abs)) * 1.5

    animation = AnimatedSimulation2D(time_vector,(orbiter,central,),dim=dim)
    animation.show()
