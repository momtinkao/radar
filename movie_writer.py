import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from queue import Queue
from threading import Thread
import time
from simradar.utils import Lane, Simulator


class AnimatedPoint:
    def __init__(self):
        # Set up the figure and axis
        self.fig, (self.ax, self.ax2) = plt.subplots(1, 2)
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(0, 200)
        self.ax.grid(True)

        self.ax2.set_xlim(-10, 10)
        self.ax2.set_ylim(0,  200)
        self.ax2.grid(True)

        # Initialize the point
        self.scat = self.ax.scatter([], [], color='blue', animated=True)
        self.scat2 = self.ax2.scatter([], [], color='blue', animated=True)
        self.texts = []
        self.texts2 = []

        # Initialize points list
        self.points = []

        # Create animation
        self.animation = FuncAnimation(
            self.fig,
            self.update,
            interval=70,  # Update every 100 ms
            blit=True
        )

    def update(self, frame):
        # Check if there's new data in the queue
        if not self.points:
            self.scat = self.ax.scatter([], [], color='blue', animated=True)
            self.texts = []
            self.scat2 = self.ax2.scatter([], [], color='blue', animated=True)
            self.texts2 = []
            return self.scat, self.scat2, *self.texts, *self.texts2

        # Unpack points
        x, y, vrels, _types = zip(*self.points)

        # Update scatter plot
        self.scat.set_offsets(list(zip(x, y)))
        self.scat2.set_offsets(list(zip(x, y)))

        self.texts.clear()
        self.texts2.clear()

        # Add new text labels
        for (xi, yi, vrel, _type) in zip(x, y, vrels, _types):
            text = self.ax.text(xi, yi, f'{vrel}',
                                fontsize=12,
                                ha='right',
                                va='bottom')
            text2 = self.ax2.text(xi, yi, f'{_type}',
                                  fontsize=12,
                                  ha='right',
                                  va='bottom')
            self.texts.append(text)
            self.texts2.append(text2)
        return self.scat, self.scat2, *self.texts, *self.texts2,

    def update_points(self, new_points):
        """Update the current points"""
        self.points = new_points

    def show(self):
        plt.show()

    def close(self):
        """Clean up resources"""
        self.running = False
        plt.close()
