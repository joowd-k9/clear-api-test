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


class DefaultRunner(Runner):
    """Runs tasks sequentially in the same thread strategy."""

    def run(
        self, func: Callable[[Any], Any], inputs: Iterable[Any]
    ) -> list[dict[str, Any]]:
        results = []
        for i in inputs:
            result = func(i)
            results.append(result)
            # Early termination: if any extraction fails, return only that error immediately
            if not result.get("success", True):
                return [result]  # Return only the error, stop immediately
        # If we get here, all inputs succeeded
        return results


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

            # Track completed futures to cancel remaining ones on failure
            completed_futures = set()

            for future in as_completed(future_to_index):
                idx = future_to_index[future]
                result = future.result()
                results[idx] = result
                completed_futures.add(future)

                # Early termination: if any extraction fails, cancel remaining futures and return only that error
                if not result.get("success", True):
                    # Cancel all remaining futures
                    for remaining_future in future_to_index:
                        if remaining_future not in completed_futures:
                            remaining_future.cancel()
                    return [result]  # Return only the error, stop immediately

        # Return results in order if all succeeded
        input_list = list(inputs)
        ordered_results = []
        for i in range(len(input_list)):
            if i in results:
                ordered_results.append(results[i])
        return ordered_results


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

            # Track completed futures to cancel remaining ones on failure
            completed_futures = set()

            for future in as_completed(future_to_index):
                idx = future_to_index[future]
                result = future.result()
                results[idx] = result
                completed_futures.add(future)

                # Early termination: if any extraction fails, cancel remaining futures and return only that error
                if not result.get("success", True):
                    # Cancel all remaining futures
                    for remaining_future in future_to_index:
                        if remaining_future not in completed_futures:
                            remaining_future.cancel()
                    return [result]  # Return only the error, stop immediately

        # Return results in order if all succeeded
        input_list = list(inputs)
        ordered_results = []
        for i in range(len(input_list)):
            if i in results:
                ordered_results.append(results[i])
        return ordered_results
