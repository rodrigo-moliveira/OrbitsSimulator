from numpy import sin, cos, arctan2, pi, sqrt

from constants import Earth

class Orbit2D:
    """used for 2D simulations of the two-body problem and central-force problem
    """
    def __init__(self,a,e,ν0=0,central=Earth):
        if e >= 1 or e < 0 :
            raise Exception("The eccentricity (e) should be in the range [0,1) (elliptical orbits only)")
        if (a*(1-e)) < central.r :
            raise Exception("The semi-major axis at periaxis is smaller than the central body's radius (Collision!).")
        self.a = a                                   #semi-major axis [m]
        self.e = e                                   #eccentricity []
        self.M = self._νtoM(ν0 % (2*pi))             #true anomaly (ν) [rad]
        self.t = 0                                   #time [s]
        self.n = sqrt(central.mu / self.a**3)        #mean motion [rad/s]


    def propagate(self,dt):
        """propagate current state by dt
        """
        self.M += self.n * dt

    def getXYcoordinates(self):
        # get polar coordinates
        ν = self._M2ν(self.M)
        r = (self.a * (1 - self.e**2)) / (1 + self.e * cos(ν))

        # get x,y coordinates
        x = r * cos(ν)
        y = r * sin(ν)
        return (x,y)



    def _M2ν(self,M):
        """convert mean anomaly M to true anomaly ν
        """

        #1. Conversion from Mean Anomaly (M) to Eccentric anomaly (E)
        #from Vallado
        tol = 1e-8

        # Ellipse
        if -pi < M < 0 or M > pi:
            E = M - self.e
        else:
            E = M + self.e

        def next_E(E, e, M):
            return E + (M - E + e * sin(E)) / (1 - e * cos(E))

        E1 = next_E(E, self.e, M)
        while abs(E1 - E) >= tol:
            E = E1
            E1 = next_E(E, self.e, M)


        #2. Conversion from Eccentric anomaly E to true anomaly ν
        cos_ν = (cos(E1) - self.e) / (1 - self.e * cos(E1))
        sin_ν = (sin(E1) * sqrt(1 - self.e ** 2)) / (1 - self.e * cos(E1))
        ν = arctan2(sin_ν, cos_ν) % (pi * 2)

        return ν



    def _νtoM(self,ν):
        """convert true anomaly ν to mean anomaly M
        """
        #1. ν to E
        cos_E = (self.e + cos(ν)) / (1 + self.e * cos(ν))
        sin_E = (sin(ν) * sqrt(1 - self.e ** 2)) / (1 + self.e * cos(ν))
        E = arctan2(sin_E, cos_E) % (2 * pi)

        # 2. E to M
        M = E - self.e * sin(E)

        return M % (2*pi)
