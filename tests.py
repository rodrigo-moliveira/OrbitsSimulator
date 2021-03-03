from constants import Body,Earth
from TwoDimensional.centralForceProblem import centralForceProblem
from TwoDimensional.twoBodyProblem import twoBodyProblem

# central force (satellite around Earth)
# height = 1000 * 10**4 #height [km]
# t_end = 24 * 60 * 60 #simulation time [seconds]
# dt = 30             #simulation step [seconds]
# sat = Body(
#     name="Satellite",
#     mass=1000,
#     equatorial_radius=10,
# )
# centralForceProblem(Earth.r + height,0.0,t_end,dt,sat,Earth)




# two body problem, analytic solution (general particle)
t_end = 10000                           #simulation time [seconds]
dt = 1                                  #simulation step [seconds]
mass_ratio = 100                          #mass_ratio = m2 / m1, where m1 is defined as Earth
                                            #(only the ratio matters for the overall geometry configuration)
e = 0.9
a = 100                                  #relative distance between two bodies. Default value is 10,
                                            #if you change it, you might have to
                                            # adjust simulation default time variables and animation speed.
twoBodyProblem(a,e,mass_ratio,t_end,dt)
