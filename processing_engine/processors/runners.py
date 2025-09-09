# runners.py

from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from typing import Callable, Any, Iterable


class Runner(ABC):
    """
    Abstract base class for execution run strategies.
    Defines a unified interface for sequential, threaded, or process-based execution.
    """

    @abstractmethod
    def run(
        self,
        func: Callable[[Any], Any],
        inputs: Iterable[Any],
    ) -> list[dict[str, Any]]:
        """
        Run a function against a list of inputs.

        Args:
            func: A callable to execute for each input.
            inputs: Iterable of input data.

        Returns:
            List of results in the same order as inputs.
        """


class SequentialRunner(Runner):
    """Runs tasks sequentially in the same thread strategy."""

    def run(
        self, func: Callable[[Any], Any], inputs: Iterable[Any]
    ) -> list[dict[str, Any]]:
        return [func(i) for i in inputs]


class ThreadRunner(Runner):
    """Runs tasks using a thread pool strategy."""

    def __init__(self, max_workers: int | None = None):
        self.max_workers = max_workers

    def run(
        self, func: Callable[[Any], Any], inputs: Iterable[Any]
    ) -> list[dict[str, Any]]:
        results: dict[int, dict[str, Any]] = {}
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_index = {
                executor.submit(func, i): idx for idx, i in enumerate(inputs)
            }
            for future in as_completed(future_to_index):
                idx = future_to_index[future]
                results[idx] = future.result()
        return [results[i] for i in sorted(results.keys())]


class ProcessRunner(Runner):
    """Runs tasks using a process pool (multiprocessing) strategy."""

    def __init__(self, max_workers: int | None = None):
        self.max_workers = max_workers

    def run(
        self, func: Callable[[Any], Any], inputs: Iterable[Any]
    ) -> list[dict[str, Any]]:
        results: dict[int, dict[str, Any]] = {}
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_index = {
                executor.submit(func, i): idx for idx, i in enumerate(inputs)
            }
            for future in as_completed(future_to_index):
                idx = future_to_index[future]
                results[idx] = future.result()
        return [results[i] for i in sorted(results.keys())]
