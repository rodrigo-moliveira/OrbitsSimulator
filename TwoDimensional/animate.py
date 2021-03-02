import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np


class AnimatedSimulation2D(object):
    def __init__(self, time_vector, particlesList,speed = 1,forever = True,dim = 1,show_trajectory = True):
        """
        time_vector - list with time steps of simulation
        particlesList - list with particles to plot
            particle.motion = "moving" or "static"
            particle.trajectory = [(x0,y0),(x1,y1),...,(xn,yn)] - list with coordinates of particle
        speed - Delay between frames in milliseconds.
        forever - whether or not to repeat simulation forever
        dim - dimension of plot (square) in meters
        """
        self.forever = forever
        self.particlesList = particlesList
        self.time_vector = time_vector
        self.stream = self.data_stream()
        self.dim = dim
        self.show_trajectory = show_trajectory

        # Setup the figure and axes...
        self.fig, self.ax = plt.subplots()
        plt.axis('scaled')

        # Then setup FuncAnimation.
        self.ani = animation.FuncAnimation(self.fig, self.update, interval=speed,
                                          init_func=self.setup_plot, blit=True)

    def setup_plot(self):
        """Initial drawing of the scatter plot."""
        point = next(self.stream)

        # moving particles
        for particle in point[1:]:
            xy = particle[0]
            c = particle[2]
            self.scat = self.ax.scatter(xy[0], xy[1] ,c=c)

        # static particles
        for particle in self.particlesList:
            if particle.motion == "static":
                circle = plt.Circle((particle.trajectory[0], particle.trajectory[1]),
                                    radius = particle.r, color=particle.color)
                center = self.ax.scatter(particle.trajectory[0], particle.trajectory[1] ,c='k')
                self.ax.add_patch(circle)

            # show dashed trajectories
            elif self.show_trajectory:
                traj = particle.trajectory
                x = [j[0] for j in traj]
                y = [j[1] for j in traj]
                plt.plot(x,y,linestyle='dashed',color="grey")

        self.ax.axis([-self.dim, self.dim, -self.dim, self.dim])

        return self.scat,

    def data_stream(self):
        """Generate trajectories data streams."""
        repeat = 0
        data = [[t] for t in self.time_vector]

        while (repeat == 0):
            for particle in self.particlesList:
                # do not process(update) static objects
                if particle.motion == 'static':
                    continue

                for data_point,point in zip(data,particle.trajectory):
                    data_point.append([point,particle.r,particle.color])

            for point in data:
                yield point

            if not self.forever:
                repeat = 1





    def update(self, i):
        """Update the scatter plot."""
        point = next(self.stream)

        for particle in point[1:]:
            xy = particle[0]
            c = particle[2]
            self.scat = self.ax.scatter(xy[0], xy[1] ,c=c)


        return self.scat,

    def show(self):
        plt.show()
