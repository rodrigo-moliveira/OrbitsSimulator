import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np


class AnimatedSimulation2D(object):
    def __init__(self, time_vector, particles_lst, speed=10, forever=True, dim=1, show_trajectory=True):
        """
        time_vector - list with time steps of simulation
        particles_lst - list with particles to plot
            particle.motion = "moving" or "static"
            particle.traj = trajectory list in xy coordinates
        speed - Delay between frames in milliseconds.
        forever - whether to repeat simulation forever
        dim - dimension of plot (square) in meters
        """
        self.forever = forever
        self.particles_lst = particles_lst
        self.time_vector = time_vector
        self.stream = self.data_stream()
        self.show_trajectory = show_trajectory
        self.dim = dim

        # Set up the figure and axes...
        self.fig, self.ax = plt.subplots()
        plt.axis('scaled')

        # Then setup FuncAnimation.
        self.ani = animation.FuncAnimation(self.fig, self.update, interval=speed,
                                           init_func=self.setup_plot, blit=True)

    def setup_plot(self):
        """Initial drawing of the scatter plot."""
        point = next(self.stream)
        self.scats = []

        # moving particles
        for particle in point[1:]:
            state = particle[0]
            color = particle[2]
            # radius = particle[1]
            self.scats.append(self.ax.scatter(state.x, state.y, c=color))

        # static particles
        for particle in self.particles_lst:
            if particle.motion == "static":
                # circle = plt.Circle((particle.traj[0], particle.traj[1]),
                #                    radius=1, color='blue')
                # self.ax.add_patch(circle)
                self.ax.scatter(particle.traj[0], particle.traj[1], c='yellow')

            # show dashed trajectories
            elif self.show_trajectory:
                traj = particle.traj
                x = [j.x for j in traj]
                y = [j.y for j in traj]
                plt.plot(x, y, linestyle='dashed', color="grey", linewidth=1)

        self.ax.axis([-10000000, 10000000, -10000000, 10000000])

        return self.scats

    def data_stream(self):
        """Generate trajectories data streams."""
        repeat = 0
        data = [[t] for t in self.time_vector]

        while repeat == 0:
            for particle in self.particles_lst:
                # do not process(update) static objects
                if particle.motion == 'static':
                    continue

                for data_point, point in zip(data, particle.traj):
                    # data_point.append([point, particle.r, particle.color])
                    data_point.append([point, 2, 'red'])

            for point in data:
                yield point

            if not self.forever:
                repeat = 1

    def update(self, i):
        """Update the scatter plot."""
        point = next(self.stream)

        i = 0
        for particle in point[1:]:
            xy = particle[0]
            c = particle[2]
            self.scats[i] = self.ax.scatter(xy.x, xy.y, c=c)
            i += 1

        return self.scats


    def show(self):
        plt.show()
