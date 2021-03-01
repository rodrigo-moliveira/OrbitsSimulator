"""Constants necessary to computations

All units are in `SI <https://en.wikipedia.org/wiki/International_System_of_Units>`__
"""

from numpy import sqrt


c = 299792458
"""Speed of light in m.s⁻¹"""

g0 = 9.80665
"""Standard Earth gravity in m.s⁻²"""

G = 6.6740831e-11
"""Gravitational constant in m³.kg⁻¹.s⁻² or N.m².kg⁻²"""


class Body:
    """Generic class for the description of physical characteristics of celestial body"""

    def __init__(self, name, mass, equatorial_radius, **kwargs):
        self.name = name
        """Name of the celestial body"""
        self.mass = mass
        """Mass of the celestial body"""
        self.equatorial_radius = equatorial_radius
        """Equatorial radius of the celestial body"""

        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        return "<Body '%s'>" % self.name

    def __getattr__(self, name):
        attrs = {
            "m": "mass",
            "r": "equatorial_radius",
            chr(956): "mu",
            "µ": "mu",
            "e": "eccentricity",
        }

        try:
            return getattr(self, attrs[name])
        except KeyError:
            raise AttributeError(name)

    @property
    def mu(self):
        """Standard gravitational parameter of the body"""
        return self.mass * G

    @property
    def eccentricity(self):
        """Eccentricity of the body"""
        return sqrt(self.f * 2 - self.f ** 2)

    def polar_radius(self):
        """Polar radius of the body"""
        return self.r * (1 - self.f)


Earth = Body(
    name="Earth",
    mass=5.97237e24,
    equatorial_radius=6378136.3,
)
