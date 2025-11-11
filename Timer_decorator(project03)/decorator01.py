import time
import numpy as np

class TimerDecorator:
    """
        A decorator class for measuring execution time statistics of functions.

        This decorator records how long a function takes to execute each time 
        it is called, while maintaining running statistics such as average 
        time, standard deviation, minimum, and maximum durations.

        The implementation is memory-efficient, it does not store each time 
        seperatly.

        Parameters
        ----------
        func : callable
            The function to be wrapped and timed.

        Attributes
        ----------
        func : callable
            The wrapped function being monitored.
        counter : int
            Number of times the decorated function has been called.
        total_time : float
            Cumulative sum of all recorded execution times (in seconds).
        total_squared_time : float
            Cumulative sum of squared execution times (used for variance computation).
        min_time : float
            Minimum recorded execution time.
        max_time : float
            Maximum recorded execution time.

        Examples
        --------
        >>> @TimerDecorator
        ... def slow_function():
        ...     time.sleep(0.2)
        ...
        >>> for _ in range(5):
        ...     slow_function()
        ...
        >>> slow_function.print_stats()
        runs: 5
        average (s): 0.2001
        std (s): 0.0005
        min (s): 0.1993
        max (s): 0.2010
    """
    def __init__(self, func):
        self.func = func
        self.counter = 0
        self.total_time = 0.0
        self.total_squared_time = 0.0
        self.min_time = float('inf')
        self.max_time = float('-inf')

    def __call__(self, *args, **kwargs):
        start = time.time()
        result = self.func(*args, **kwargs)
        elapsed = time.time() - start

        # Update stats incrementally
        self.counter += 1
        self.total_time += elapsed
        self.total_squared_time += elapsed ** 2
        self.min_time = min(self.min_time, elapsed)
        self.max_time = max(self.max_time, elapsed)

        return result

    def print_stats(self):
        if self.counter == 0:
            print("No runs yet.")
            return

        avg = self.total_time / self.counter
        variance = (self.total_squared_time / self.counter) - (avg ** 2)
        std = np.sqrt(variance) if variance > 0 else 0.0

        print(f"runs: {self.counter}")
        print(f"average (s): {avg:.6f}")
        print(f"std (s): {std:.6f}")
        print(f"min (s): {self.min_time:.6f}")
        print(f"max (s): {self.max_time:.6f}")

    
@TimerDecorator
def singularValueDecomposition(matrixsize = 1000):
    A = np.random.rand(matrixsize, matrixsize)
    np.linalg.svd(A)

for _ in range(5):
    singularValueDecomposition(2000)

singularValueDecomposition.print_stats()