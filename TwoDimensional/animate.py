import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np


class AnimatedSimulation2D(object):
    def __init__(self, R_list,trajectories_list,speed = 30,forever = True):
        """
        R_list - list of radius of each object to plot
        trajectories_list - list of trajectories for each object
        speed - Delay between frames in milliseconds.
        forever - whether or not to repeat simulation forever
        """
        self.R_list = R_list
        self.trajectories_list = trajectories_list
        self.forever = forever
        self.stream = self.data_stream()

        all = np.array(self.trajectories_list).flatten()
        self.MAX_XY = abs(max(all.min(), all.max(), key=abs)) * 1.5

        # Setup the figure and axes...
        self.fig, self.ax = plt.subplots()
        plt.axis('scaled')
        # Then setup FuncAnimation.
        self.ani = animation.FuncAnimation(self.fig, self.update, interval=speed,
                                          init_func=self.setup_plot, blit=True)

    def setup_plot(self):
        """Initial drawing of the scatter plot."""
        x, y = next(self.stream)

        circle1 = plt.Circle((0, 0), 6378136, color='b')
        self.ax.add_patch(circle1)
        self.scat = self.ax.scatter(x, y,c='k')
        self.ax.axis([-self.MAX_XY, self.MAX_XY, -self.MAX_XY, self.MAX_XY])

        return self.scat,

    def data_stream(self):
        """Generate trajectories data streams."""
        trajectory = self.trajectories_list

        if self.forever:
            while(True):
                for point in trajectory:
                    yield point
        else:
            for point in trajectory:
                yield point



    def update(self, i):
        """Update the scatter plot."""
        x,y = next(self.stream)

        # Set x and y data...
        self.scat = self.ax.scatter(x, y,c='k')

        return self.scat,

    def show(self):
        plt.show()
