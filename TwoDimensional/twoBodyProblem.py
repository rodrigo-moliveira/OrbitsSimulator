import numpy as np

from .orbits import Orbit2D
import constants
from .animate import AnimatedSimulation2D

# to simplify the problem (in terms of the order of magnitude of the axes), I make G = 1, m1 = 1
norm = np.linalg.norm
m1 = 1


def twoBodyProblem(a,e,mass_ratio,t_end,dt):

    m2 = mass_ratio * m1
    CM_particle = constants.Body(
        name="CM",
        mass=m1 + m2,
        equatorial_radius = -1,
    )
    particle1 = constants.Body(
        name="P1",
        mass=m1,
        equatorial_radius = -1,
    )
    particle2 = constants.Body(
        name="P2",
        mass=m2,
        equatorial_radius = -1,
    )

    r_relative = Orbit2D(a, e,CM_particle)


    t = 0
    particle1traj = []
    particle2traj = []
    time_vector = []

    while(t < t_end):
        r_relative.propagate(dt)
        (x,y) = r_relative.getXYcoordinates()

        particle1traj.append([-m2/(m1+m2) * x,-m2/(m1+m2) * y])
        particle2traj.append([m1/(m1+m2) * x,m1/(m1+m2) * y])

        t += dt
        time_vector.append(t)

    particle1.trajectory = particle1traj
    particle1.color = 'blue'
    particle1.motion = "moving"
    particle2.trajectory = particle2traj
    particle2.motion = "moving"
    particle2.color = 'orange'

    _all = np.array([particle1traj,particle2traj]).flatten()
    dim = abs(max(_all.min(), _all.max(), key=abs)) * 1.5

    animation = AnimatedSimulation2D(time_vector,(particle1,particle2,),dim=dim)
    animation.show()
