from .orbits import Orbit2D
from constants import Earth
from .animate import AnimatedSimulation2D


def centralForceProblem(a,e,t_end,dt,orbiter,central,ν0=0):
    orbit = Orbit2D(a,e,ν0,Earth)

    t = 0
    trajectory = []

    while(t < t_end):
        orbit.propagate(dt)
        (x,y) = orbit.getXYcoordinates()
        trajectory.append([x,y])

        t += dt

    animation = AnimatedSimulation2D(orbiter.r,trajectory)
    animation.show()
