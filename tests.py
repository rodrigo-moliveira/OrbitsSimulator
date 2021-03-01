from constants import Body,Earth
from TwoDimensional.centralForceProblem import centralForceProblem



height = 1000 * 10**3 #height [km]
t_end = 24 * 60 * 60 #simulation time [seconds]
dt = 60             #simulation step [seconds]
sat = Body(
    name="Satellite",
    mass=1000,
    equatorial_radius=10,
)
centralForceProblem(Earth.r + height,0.01,t_end,dt,sat,Earth)


# for t in range(100):
#     orbit.propagate(1)
#     print(orbit.getXYcoordinates())

# if __name__ == '__main__':
    # a = AnimatedScatter()
    # plt.show()
