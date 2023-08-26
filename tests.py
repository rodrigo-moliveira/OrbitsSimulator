from constants import Earth, Body
from TwoDimensional.centralForceProblem import centralForceProblem
from TwoDimensional.state import State2D
#from TwoDimensional.twoBodyProblem import twoBodyProblem

# central force (satellite around Earth)
initial_state = State2D("mean_keplerian", a=Earth.radius + 500*1000, e=0.1, M=2.3)
initial_state.convert_form("true_keplerian")
t_end = 24 * 60 * 60  # simulation time [seconds]
dt = 1  # simulation step [seconds]
sat = Body(
    name="Satellite",
    mass=1000,
    radius=1
)
sat.initial_state = initial_state
centralForceProblem(Earth, sat, t_end, dt)




# two body problem, analytic solution (general particle)
#t_end = 10000                           #simulation time [seconds]
#dt = 1                                  #simulation step [seconds]
#mass_ratio = 100                          #mass_ratio = m2 / m1, where m1 is defined as Earth
                                            #(only the ratio matters for the overall geometry configuration)
#e = 0.9
#a = 100                                  #relative distance between two bodies. Default value is 10,
                                            #if you change it, you might have to
                                            # adjust simulation default time variables and animation speed.
#twoBodyProblem(a,e,mass_ratio,t_end,dt)
