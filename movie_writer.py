import matplotlib.pyplot as plt
import matplotlib
from matplotlib.animation import FuncAnimation
from queue import Queue
from threading import Thread
import time

class AnimatedPoint:
    def __init__(self):
        # Set up the figure and axis
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(-30, 30)
        self.ax.set_ylim(0, 260)
        self.ax.grid(True)

        # Initialize the point
        self.scat = self.ax.scatter([], [], color='blue', animated=True)
        self.texts = []

        # Initialize points list
        self.points = []

        # Create animation
        self.animation = FuncAnimation(
            self.fig,
            self.update,
            interval=15,  # Update every 100 ms
            blit=True
        )

    def update(self, frame):
        # Check if there's new data in the queue
        if not self.points:
            self.scat = self.ax.scatter([], [], color='blue', animated=True)
            self.texts = []
            return self.scat, *self.texts

        # Unpack points
        x, y, vrels = zip(*self.points)

        # Update scatter plot
        self.scat.set_offsets(list(zip(x, y)))

        # Remove old text labels
        for text in self.texts:
            text.remove()
        self.texts.clear()

        # Add new text labels
        for (xi, yi, vrel) in zip(x, y, vrels):
            text = self.ax.text(xi, yi, f'{vrel}',
                                fontsize=12,
                                ha='right',
                                va='bottom')
            self.texts.append(text)
        return self.scat, *self.texts

    def add_point(self, x, y, text=''):
        """Add a new point to the queue"""
        self.points.append((x, y, text))

    def show(self):
        plt.show()

    def close(self):
        """Clean up resources"""
        self.running = False
        plt.close()
