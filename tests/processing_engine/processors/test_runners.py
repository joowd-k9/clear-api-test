"""
Comprehensive tests for Runner implementations.
"""

import pytest
import sys
import os
import time
import threading
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from unittest.mock import patch, MagicMock

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from processing_engine.processors.runners import (
    Runner,
    SequentialRunner,
    ThreadRunner,
    ProcessRunner,
)


# Module-level functions for ProcessRunner tests (must be picklable)
def square_function(x):
    return {"result": x * x, "input": x}


def identity_function(x):
    return {"value": x, "order": x}


def get_process_info_function(x):
    import os

    time.sleep(0.1)  # Simulate work
    return {"result": x, "pid": os.getpid(), "ppid": os.getppid()}


def double_function(x):
    return {"result": x * 2}


def failing_function(x):
    if x == 3:
        raise ValueError("Test exception")
    return {"result": x}


def get_pid_function(x):
    import os

    time.sleep(0.1)
    return {"result": x, "pid": os.getpid()}


def handle_none_function(x):
    return {"result": x is None, "value": x}


def complex_function(x):
    return {
        "number": x,
        "string": f"value_{x}",
        "list": [x, x * 2, x * 3],
        "dict": {"nested": {"value": x}},
        "boolean": x % 2 == 0,
    }


def cpu_intensive_function(x):
    # Simulate CPU-intensive work
    result = 0
    for i in range(100000):
        result += i * x
    return {"result": result, "input": x}


def io_intensive_function(x):
    time.sleep(0.1)  # Simulate I/O wait
    return {"result": x * 2, "input": x}


class TestRunnerInterface:
    """Test the abstract Runner interface."""

    def test_runner_is_abstract(self):
        """Test that Runner cannot be instantiated directly."""
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            Runner()

    def test_runner_has_abstract_method(self):
        """Test that Runner has the required abstract method."""
        assert hasattr(Runner, "run")
        assert getattr(Runner.run, "__isabstractmethod__", False)


class TestSequentialRunner:
    """Test SequentialRunner implementation."""

    def test_sequential_runner_initialization(self):
        """Test SequentialRunner initialization."""
        runner = SequentialRunner()
        assert isinstance(runner, Runner)
        assert isinstance(runner, SequentialRunner)

    def test_sequential_runner_simple_function(self):
        """Test SequentialRunner with a simple function."""
        runner = SequentialRunner()

        def square(x):
            return {"result": x * x, "input": x}

        inputs = [1, 2, 3, 4, 5]
        results = runner.run(square, inputs)

        assert len(results) == 5
        assert results[0]["result"] == 1
        assert results[1]["result"] == 4
        assert results[2]["result"] == 9
        assert results[3]["result"] == 16
        assert results[4]["result"] == 25

    def test_sequential_runner_order_preservation(self):
        """Test that SequentialRunner preserves input order."""
        runner = SequentialRunner()

        def identity(x):
            return {"value": x, "order": x}

        inputs = [5, 1, 3, 2, 4]
        results = runner.run(identity, inputs)

        assert len(results) == 5
        for i, result in enumerate(results):
            assert result["value"] == inputs[i]
            assert result["order"] == inputs[i]

    def test_sequential_runner_empty_inputs(self):
        """Test SequentialRunner with empty inputs."""
        runner = SequentialRunner()

        def dummy_func(x):
            return {"result": x}

        results = runner.run(dummy_func, [])
        assert results == []

    def test_sequential_runner_single_input(self):
        """Test SequentialRunner with single input."""
        runner = SequentialRunner()

        def double(x):
            return {"result": x * 2}

        results = runner.run(double, [42])
        assert len(results) == 1
        assert results[0]["result"] == 84

    def test_sequential_runner_function_with_exception(self):
        """Test SequentialRunner handles exceptions properly."""
        runner = SequentialRunner()

        def failing_func(x):
            if x == 3:
                raise ValueError("Test exception")
            return {"result": x}

        inputs = [1, 2, 3, 4]

        with pytest.raises(ValueError, match="Test exception"):
            runner.run(failing_func, inputs)

    def test_sequential_runner_complex_data_types(self):
        """Test SequentialRunner with complex data types."""
        runner = SequentialRunner()

        def process_dict(d):
            return {
                "keys": list(d.keys()),
                "values": list(d.values()),
                "length": len(d),
            }

        inputs = [
            {"a": 1, "b": 2},
            {"x": "hello", "y": "world"},
            {"nested": {"inner": "value"}},
        ]

        results = runner.run(process_dict, inputs)

        assert len(results) == 3
        assert results[0]["keys"] == ["a", "b"]
        assert results[0]["values"] == [1, 2]
        assert results[0]["length"] == 2

        assert results[1]["keys"] == ["x", "y"]
        assert results[1]["values"] == ["hello", "world"]
        assert results[1]["length"] == 2

        assert results[2]["keys"] == ["nested"]
        assert results[2]["length"] == 1


class TestThreadRunner:
    """Test ThreadRunner implementation."""

    def test_thread_runner_initialization_default(self):
        """Test ThreadRunner initialization with default max_workers."""
        runner = ThreadRunner()
        assert isinstance(runner, Runner)
        assert isinstance(runner, ThreadRunner)
        assert runner.max_workers is None

    def test_thread_runner_initialization_custom_workers(self):
        """Test ThreadRunner initialization with custom max_workers."""
        runner = ThreadRunner(max_workers=4)
        assert runner.max_workers == 4

    def test_thread_runner_simple_function(self):
        """Test ThreadRunner with a simple function."""
        runner = ThreadRunner(max_workers=2)

        def square(x):
            return {"result": x * x, "input": x}

        inputs = [1, 2, 3, 4, 5]
        results = runner.run(square, inputs)

        assert len(results) == 5
        # Results should be in the same order as inputs
        for i, result in enumerate(results):
            assert result["result"] == inputs[i] * inputs[i]
            assert result["input"] == inputs[i]

    def test_thread_runner_order_preservation(self):
        """Test that ThreadRunner preserves input order despite concurrent execution."""
        runner = ThreadRunner(max_workers=3)

        def identity(x):
            return {"value": x, "order": x}

        inputs = [5, 1, 3, 2, 4]
        results = runner.run(identity, inputs)

        assert len(results) == 5
        for i, result in enumerate(results):
            assert result["value"] == inputs[i]
            assert result["order"] == inputs[i]

    def test_thread_runner_concurrent_execution(self):
        """Test that ThreadRunner actually executes functions concurrently."""
        runner = ThreadRunner(max_workers=2)

        execution_order = []
        execution_lock = threading.Lock()

        def slow_function(x):
            with execution_lock:
                execution_order.append(f"start_{x}")
            time.sleep(0.1)  # Simulate work
            with execution_lock:
                execution_order.append(f"end_{x}")
            return {"result": x, "thread": threading.current_thread().name}

        inputs = [1, 2, 3]
        start_time = time.time()
        results = runner.run(slow_function, inputs)
        end_time = time.time()

        # Should complete faster than sequential execution (3 * 0.1 = 0.3s)
        # but allow some tolerance for overhead
        assert end_time - start_time < 0.25

        # Should have results for all inputs
        assert len(results) == 3
        for i, result in enumerate(results):
            assert result["result"] == inputs[i]
            assert "ThreadPoolExecutor" in result["thread"]

        # Should show some interleaving of execution (concurrent behavior)
        assert len(execution_order) == 6  # 3 starts + 3 ends

    def test_thread_runner_empty_inputs(self):
        """Test ThreadRunner with empty inputs."""
        runner = ThreadRunner()

        def dummy_func(x):
            return {"result": x}

        results = runner.run(dummy_func, [])
        assert results == []

    def test_thread_runner_single_input(self):
        """Test ThreadRunner with single input."""
        runner = ThreadRunner()

        def double(x):
            return {"result": x * 2}

        results = runner.run(double, [42])
        assert len(results) == 1
        assert results[0]["result"] == 84

    def test_thread_runner_function_with_exception(self):
        """Test ThreadRunner handles exceptions properly."""
        runner = ThreadRunner(max_workers=2)

        def failing_func(x):
            if x == 3:
                raise ValueError("Test exception")
            return {"result": x}

        inputs = [1, 2, 3, 4]

        with pytest.raises(ValueError, match="Test exception"):
            runner.run(failing_func, inputs)

    def test_thread_runner_max_workers_limitation(self):
        """Test that ThreadRunner respects max_workers limit."""
        runner = ThreadRunner(max_workers=2)

        active_threads = []
        thread_lock = threading.Lock()

        def track_threads(x):
            with thread_lock:
                active_threads.append(threading.current_thread().name)
            time.sleep(0.1)
            return {"result": x, "thread": threading.current_thread().name}

        inputs = [1, 2, 3, 4, 5]
        results = runner.run(track_threads, inputs)

        # Should have results for all inputs
        assert len(results) == 5

        # Should not have more than max_workers unique thread names
        unique_threads = set(active_threads)
        assert len(unique_threads) <= 2  # max_workers


class TestProcessRunner:
    """Test ProcessRunner implementation."""

    def test_process_runner_initialization_default(self):
        """Test ProcessRunner initialization with default max_workers."""
        runner = ProcessRunner()
        assert isinstance(runner, Runner)
        assert isinstance(runner, ProcessRunner)
        assert runner.max_workers is None

    def test_process_runner_initialization_custom_workers(self):
        """Test ProcessRunner initialization with custom max_workers."""
        runner = ProcessRunner(max_workers=2)
        assert runner.max_workers == 2

    def test_process_runner_simple_function(self):
        """Test ProcessRunner with a simple function."""
        runner = ProcessRunner(max_workers=2)

        inputs = [1, 2, 3, 4, 5]
        results = runner.run(square_function, inputs)

        assert len(results) == 5
        # Results should be in the same order as inputs
        for i, result in enumerate(results):
            assert result["result"] == inputs[i] * inputs[i]
            assert result["input"] == inputs[i]

    def test_process_runner_order_preservation(self):
        """Test that ProcessRunner preserves input order despite concurrent execution."""
        runner = ProcessRunner(max_workers=2)

        inputs = [5, 1, 3, 2, 4]
        results = runner.run(identity_function, inputs)

        assert len(results) == 5
        for i, result in enumerate(results):
            assert result["value"] == inputs[i]
            assert result["order"] == inputs[i]

    def test_process_runner_concurrent_execution(self):
        """Test that ProcessRunner actually executes functions in separate processes."""
        runner = ProcessRunner(max_workers=2)

        inputs = [1, 2, 3]
        start_time = time.time()
        results = runner.run(get_process_info_function, inputs)
        end_time = time.time()

        # Should complete faster than sequential execution
        assert end_time - start_time < 0.25

        # Should have results for all inputs
        assert len(results) == 3
        for i, result in enumerate(results):
            assert result["result"] == inputs[i]
            assert isinstance(result["pid"], int)
            assert isinstance(result["ppid"], int)

        # Should have different PIDs (different processes)
        pids = [result["pid"] for result in results]
        unique_pids = set(pids)
        assert len(unique_pids) > 1  # Should use multiple processes

    def test_process_runner_empty_inputs(self):
        """Test ProcessRunner with empty inputs."""
        runner = ProcessRunner()

        def dummy_func(x):
            return {"result": x}

        results = runner.run(dummy_func, [])
        assert results == []

    def test_process_runner_single_input(self):
        """Test ProcessRunner with single input."""
        runner = ProcessRunner()

        results = runner.run(double_function, [42])
        assert len(results) == 1
        assert results[0]["result"] == 84

    def test_process_runner_function_with_exception(self):
        """Test ProcessRunner handles exceptions properly."""
        runner = ProcessRunner(max_workers=2)

        inputs = [1, 2, 3, 4]

        with pytest.raises(ValueError, match="Test exception"):
            runner.run(failing_function, inputs)

    def test_process_runner_max_workers_limitation(self):
        """Test that ProcessRunner respects max_workers limit."""
        runner = ProcessRunner(max_workers=2)

        inputs = [1, 2, 3, 4, 5]
        results = runner.run(get_pid_function, inputs)

        # Should have results for all inputs
        assert len(results) == 5

        # Should not have more than max_workers unique PIDs
        unique_pids = set(result["pid"] for result in results)
        assert len(unique_pids) <= 2  # max_workers


class TestRunnerComparison:
    """Test and compare different Runner implementations."""

    def test_all_runners_same_results(self):
        """Test that all runners produce the same results for the same function."""
        inputs = [1, 2, 3, 4, 5]

        sequential_runner = SequentialRunner()
        thread_runner = ThreadRunner(max_workers=2)
        process_runner = ProcessRunner(max_workers=2)

        sequential_results = sequential_runner.run(square_function, inputs)
        thread_results = thread_runner.run(square_function, inputs)
        process_results = process_runner.run(square_function, inputs)

        # All should produce identical results
        assert sequential_results == thread_results == process_results

    def test_runner_performance_comparison(self):
        """Test performance characteristics of different runners."""
        inputs = [1, 2, 3, 4, 5]

        # Test sequential runner
        start_time = time.time()
        sequential_runner = SequentialRunner()
        sequential_results = sequential_runner.run(cpu_intensive_function, inputs)
        sequential_time = time.time() - start_time

        # Test thread runner
        start_time = time.time()
        thread_runner = ThreadRunner(max_workers=2)
        thread_results = thread_runner.run(cpu_intensive_function, inputs)
        thread_time = time.time() - start_time

        # Test process runner
        start_time = time.time()
        process_runner = ProcessRunner(max_workers=2)
        process_results = process_runner.run(cpu_intensive_function, inputs)
        process_time = time.time() - start_time

        # All should produce the same results
        assert sequential_results == thread_results == process_results

        # For CPU-intensive tasks, process runner should be faster than sequential
        # Thread runner might be similar to sequential due to GIL
        print(f"Sequential time: {sequential_time:.3f}s")
        print(f"Thread time: {thread_time:.3f}s")
        print(f"Process time: {process_time:.3f}s")

    def test_runner_with_io_intensive_task(self):
        """Test runners with I/O intensive tasks."""
        inputs = [1, 2, 3, 4, 5]

        # Test sequential runner
        start_time = time.time()
        sequential_runner = SequentialRunner()
        sequential_results = sequential_runner.run(io_intensive_function, inputs)
        sequential_time = time.time() - start_time

        # Test thread runner
        start_time = time.time()
        thread_runner = ThreadRunner(max_workers=3)
        thread_results = thread_runner.run(io_intensive_function, inputs)
        thread_time = time.time() - start_time

        # Test process runner
        start_time = time.time()
        process_runner = ProcessRunner(max_workers=3)
        process_results = process_runner.run(io_intensive_function, inputs)
        process_time = time.time() - start_time

        # All should produce the same results
        assert sequential_results == thread_results == process_results

        # For I/O intensive tasks, both thread and process runners should be faster
        print(f"Sequential time: {sequential_time:.3f}s")
        print(f"Thread time: {thread_time:.3f}s")
        print(f"Process time: {process_time:.3f}s")

        # Thread and process runners should be significantly faster than sequential
        assert thread_time < sequential_time * 0.8
        assert process_time < sequential_time * 0.8


class TestRunnerEdgeCases:
    """Test edge cases and error conditions for all runners."""

    def test_runner_with_none_inputs(self):
        """Test runners with None inputs."""
        inputs = [None, 1, None, 2]

        sequential_runner = SequentialRunner()
        thread_runner = ThreadRunner(max_workers=2)
        process_runner = ProcessRunner(max_workers=2)

        sequential_results = sequential_runner.run(handle_none_function, inputs)
        thread_results = thread_runner.run(handle_none_function, inputs)
        process_results = process_runner.run(handle_none_function, inputs)

        expected = [
            {"result": True, "value": None},
            {"result": False, "value": 1},
            {"result": True, "value": None},
            {"result": False, "value": 2},
        ]

        assert sequential_results == expected
        assert thread_results == expected
        assert process_results == expected

    def test_runner_with_large_inputs(self):
        """Test runners with large number of inputs."""

        def identity(x):
            return {"value": x}

        # Create a large list of inputs
        inputs = list(range(100))

        sequential_runner = SequentialRunner()
        thread_runner = ThreadRunner(max_workers=4)
        process_runner = ProcessRunner(max_workers=4)

        sequential_results = sequential_runner.run(identity, inputs)
        thread_results = thread_runner.run(identity, inputs)
        process_results = process_runner.run(identity, inputs)

        assert len(sequential_results) == 100
        assert len(thread_results) == 100
        assert len(process_results) == 100

        # All should produce the same results
        assert sequential_results == thread_results == process_results

    def test_runner_with_complex_return_types(self):
        """Test runners with complex return types."""
        inputs = [1, 2, 3]

        sequential_runner = SequentialRunner()
        thread_runner = ThreadRunner(max_workers=2)
        process_runner = ProcessRunner(max_workers=2)

        sequential_results = sequential_runner.run(complex_function, inputs)
        thread_results = thread_runner.run(complex_function, inputs)
        process_results = process_runner.run(complex_function, inputs)

        # All should produce identical results
        assert sequential_results == thread_results == process_results

        # Verify the structure of results
        for result in sequential_results:
            assert "number" in result
            assert "string" in result
            assert "list" in result
            assert "dict" in result
            assert "boolean" in result
            assert isinstance(result["list"], list)
            assert isinstance(result["dict"], dict)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
