from numpy import sin, cos, arctan2, pi, sqrt

from TwoDimensional.state import State2D
from constants import Body


class Orbit2D:
    """used for 2D simulations of the two-body problem and central-force problem
    """

    def __init__(self, central_body: Body, initial_state: State2D):
        # get state in mean_keplerian form
        initial_state.convert_form('mean_keplerian')
        self.state = initial_state

        if self.state.e >= 1 or self.state.e < 0:
            raise Exception("The eccentricity (e) should be in the range [0,1) (elliptical orbits only)")

        self.t = 0  # time [s]
        self.n = sqrt(central_body.mu / self.state.a ** 3)  # mean motion [rad/s]

    def propagate(self, dt):
        """propagate current state by dt
        """
        self.state.M = (self.state.M + self.n * dt) % (2 * pi)
