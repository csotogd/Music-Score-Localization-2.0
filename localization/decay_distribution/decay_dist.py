import numpy as np
import matplotlib.pyplot as plt


class Decay_Dist:
    """
    A probability distribution f such that:
        - f is piecewise exponential
        - f(0) = 1

    Initialize with the future decay factor (i.e.
    the factor that determines how much faster the
    distribution decays for future times compared to
    past times).
    """

    def __init__(self, future_decay):
        self.a = np.exp(
            0.5 * (np.sqrt(np.log(future_decay) ** 2 + 4) - np.log(future_decay) + 2)
        )
        self.b = future_decay * self.a

    def __call__(self, x):
        return self.a**x if x < 0 else self.b ** (-x)

    def plot(self):
        x = np.linspace(-10, 10, 1000)
        y = [self(i) for i in x]
        plt.plot(x, y)
        plt.show()
