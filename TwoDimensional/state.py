from math import pi, sin, cos, atan2, sqrt


class State2D(object):
    """
    Store orbital state for 2D orbits (only in plane)
    """
    FORMS = {'true_keplerian', 'mean_keplerian', 'cartesian'}
    MEAN_KEPLERIAN = [
        'a',  # semi-major axis
        'e',  # eccentricity
        'M'  # mean anomaly
    ]
    TRUE_KEPLERIAN = [
        'a',  # semi-major axis
        'e',  # eccentricity
        'theta'  # true anomaly
    ]
    CARTESIAN = [
        'x',  # x coordinate
        'y',  # y coordinate
    ]
    FORM_MAP = {
        "true_keplerian": TRUE_KEPLERIAN,
        "mean_keplerian": MEAN_KEPLERIAN,
        "cartesian": CARTESIAN
    }

    def __init__(self, form, **kwargs):
        self._form = form
        self._state = []

        # validate input form
        if form not in State2D.FORMS:
            raise AttributeError(f"Unknown form in State initialization. Valid forms are "
                                 f"'true_keplerian', 'mean_keplerian' or 'cartesian'")
        # initialize state
        if 'state' in kwargs:
            self._state = kwargs['state']

        else:
            arr = State2D.FORM_MAP[form]
            for ele in arr:
                try:
                    self._state.append(kwargs[ele])
                except:
                    raise AttributeError(f"Error when initializing the State. Element {ele} is missing for {form} form")

    def __repr__(self):
        att = str()
        for key, val in zip(State2D.FORM_MAP[self._form], self._state):
            att += f"{key}={val},"
        return f"[State2D {self._form}: {att[0:-1]}]"

    def copy(self, form=None):
        copy_state = State2D(self._form, state=self._state.copy())
        if form is not None:
            copy_state.convert_form(form)
        return copy_state

    def __getattr__(self, item):
        form_map = State2D.FORM_MAP[self._form]
        try:
            i = form_map.index(item)
        except:
            raise AttributeError(f"Unknown element {item} for state in form {self._form}. "
                                 f"Available elements are {form_map}")
        return self._state[i]

    def __setattr__(self, key, value):
        if key in {'_form', '_state'}:
            super(State2D, self).__setattr__(key, value)
        else:
            self.set_state_element(key, value)

    def set_state_element(self, key, value):
        form_map = State2D.FORM_MAP[self._form]
        try:
            i = form_map.index(key)
            self._state[i] = value
        except:
            raise AttributeError(f"Unknown element {key} for state in form {self._form}. "
                                 f"Available elements are {form_map}")

    def convert_form(self, new_form):
        if new_form not in State2D.FORMS:
            raise AttributeError(f"Unknown form in State initialization. Valid forms are "
                                 f"'true_keplerian', 'mean_keplerian' or 'cartesian'")

        if self._form == new_form:
            return  # no action needed

        if self._form == 'mean_keplerian' and new_form == 'true_keplerian':
            # convert from mean to true keplerian
            a, e, M = self._state
            theta = self._mean2true(e, M)
            self._state = [a, e, theta]
        elif self._form == 'true_keplerian' and new_form == 'mean_keplerian':
            # convert from true to mean keplerian
            a, e, theta = self._state
            M = self._true2mean(e, theta)
            self._state = [a, e, M]
        elif self._form == 'mean_keplerian' and new_form == 'cartesian':
            # convert from mean_keplerian to true_keplerian first
            self.convert_form('true_keplerian')
            self.convert_form('cartesian')
        elif self._form == 'true_keplerian' and new_form == 'cartesian':
            a, e, theta = self._state
            x, y = self._true2cartesian(a, e, theta)
            self._state = [x, y]
        self._form = new_form

    @staticmethod
    def _true2cartesian(a, e, v):
        """convert true keplerian to cartesian
        """
        # get polar coordinates
        r = (a * (1 - e ** 2)) / (1 + e * cos(v))

        # get x,y coordinates
        x = r * cos(v)
        y = r * sin(v)
        return x, y

    @staticmethod
    def _mean2true(e, M):
        """convert mean anomaly M to true anomaly v
        """

        # 1. Conversion from Mean Anomaly (M) to Eccentric anomaly (E)
        # from Vallado
        tol = 1e-9

        # Ellipse
        if -pi < M < 0 or M > pi:
            E = M - e
        else:
            E = M + e

        def next_E(E, e, M):
            return E + (M - E + e * sin(E)) / (1 - e * cos(E))

        E1 = next_E(E, e, M)
        while abs(E1 - E) >= tol:
            E = E1
            E1 = next_E(E, e, M)

        # 2. Conversion from Eccentric anomaly E to true anomaly v
        cos_v = (cos(E1) - e) / (1 - e * cos(E1))
        sin_v = (sin(E1) * sqrt(1 - e ** 2)) / (1 - e * cos(E1))
        v = atan2(sin_v, cos_v) % (pi * 2)

        return v

    @staticmethod
    def _true2mean(e, v):
        """convert true anomaly v to mean anomaly M
        """
        # 1. v to E
        cos_E = (e + cos(v)) / (1 + e * cos(v))
        sin_E = (sin(v) * sqrt(1 - e ** 2)) / (1 + e * cos(v))
        E = atan2(sin_E, cos_E) % (2 * pi)

        # 2. E to M
        M = E - e * sin(E)

        return M % (2 * pi)
