import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from queue import Queue
from threading import Thread
import time


class AnimatedPoint:
    def __init__(self):
        # Set up the figure and axis
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        self.ax.grid(True)

        # Initialize the point
        self.point, = self.ax.plot([], [], 'ro', markersize=10)

        # Initialize text annotation
        self.text = self.ax.text(0, 0, '', fontsize=10,
                                 horizontalalignment='center',
                                 verticalalignment='bottom')

        # Create a queue for receiving coordinates
        self.coordinate_queue = Queue()

        # Initialize coordinates
        self.x = 0
        self.y = 0

        # Initialize text
        self.point_text = ''

        # Start animation
        self.ani = FuncAnimation(self.fig, self.update, interval=50,
                                 init_func=self.init, blit=True)

        # Flag to control the data reading thread
        self.running = True

    def init(self):
        self.point.set_data([], [])
        self.text.set_text('')
        return self.point, self.text

    def update(self, frame):
        # Check if there's new data in the queue
        if not self.coordinate_queue.empty():
            self.x, self.y, self.point_text = self.coordinate_queue.get()

        # Update point position
        self.point.set_data([self.x], [self.y])

        # Update text position and content
        self.text.set_position((self.x, self.y))
        self.text.set_text(str(self.point_text))

        return self.point, self.text

    def add_point(self, x, y, text=''):
        """Add a new point to the queue with optional text"""
        self.coordinate_queue.put((x, y, text))

    def show(self):
        plt.title('Animated Point Visualization')
        plt.show()

    def close(self):
        """Clean up resources"""
        self.running = False
        plt.close()


# Example usage
if __name__ == "__main__":
    # Create the animated point
    animated_point = AnimatedPoint()

    # Simulate data with text
    def simulate_data():
        while True:
            # Simulate some data with text
            t = time.time()
            x = 5 * np.cos(t)
            y = 5 * np.sin(t)

            # Add coordinates with text
            animated_point.add_point(x, y, f'({x:.2f}, {y:.2f})')
            time.sleep(0.05)

    # Start the simulation in a separate thread
    Thread(target=simulate_data, daemon=True).start()

    # Show the animation
    animated_point.show()
