"""
Simple tests for Runner implementations focusing on core functionality.
"""

import pytest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from processing_engine.processors.runners import (
    Runner,
    SequentialRunner,
    ThreadRunner,
    ProcessRunner,
)


def simple_square(x):
    """Simple function for testing."""
    return {"result": x * x, "input": x}


def simple_identity(x):
    """Simple identity function for testing."""
    return {"value": x}


class TestRunnerBasics:
    """Test basic Runner functionality."""

    def test_runner_interface(self):
        """Test that Runner is abstract."""
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            Runner()

    def test_sequential_runner_basic(self):
        """Test SequentialRunner basic functionality."""
        runner = SequentialRunner()
        inputs = [1, 2, 3]
        results = runner.run(simple_square, inputs)

        assert len(results) == 3
        assert results[0]["result"] == 1
        assert results[1]["result"] == 4
        assert results[2]["result"] == 9

    def test_thread_runner_basic(self):
        """Test ThreadRunner basic functionality."""
        runner = ThreadRunner(max_workers=2)
        inputs = [1, 2, 3]
        results = runner.run(simple_square, inputs)

        assert len(results) == 3
        assert results[0]["result"] == 1
        assert results[1]["result"] == 4
        assert results[2]["result"] == 9

    def test_process_runner_basic(self):
        """Test ProcessRunner basic functionality."""
        runner = ProcessRunner(max_workers=2)
        inputs = [1, 2, 3]
        results = runner.run(simple_square, inputs)

        assert len(results) == 3
        assert results[0]["result"] == 1
        assert results[1]["result"] == 4
        assert results[2]["result"] == 9

    def test_all_runners_same_results(self):
        """Test that all runners produce the same results."""
        inputs = [1, 2, 3, 4, 5]

        sequential_runner = SequentialRunner()
        thread_runner = ThreadRunner(max_workers=2)
        process_runner = ProcessRunner(max_workers=2)

        sequential_results = sequential_runner.run(simple_square, inputs)
        thread_results = thread_runner.run(simple_square, inputs)
        process_results = process_runner.run(simple_square, inputs)

        # All should produce identical results
        assert sequential_results == thread_results == process_results

    def test_empty_inputs(self):
        """Test all runners with empty inputs."""
        sequential_runner = SequentialRunner()
        thread_runner = ThreadRunner(max_workers=2)
        process_runner = ProcessRunner(max_workers=2)

        sequential_results = sequential_runner.run(simple_square, [])
        thread_results = thread_runner.run(simple_square, [])
        process_results = process_runner.run(simple_square, [])

        assert sequential_results == []
        assert thread_results == []
        assert process_results == []

    def test_single_input(self):
        """Test all runners with single input."""
        sequential_runner = SequentialRunner()
        thread_runner = ThreadRunner(max_workers=2)
        process_runner = ProcessRunner(max_workers=2)

        sequential_results = sequential_runner.run(simple_identity, [42])
        thread_results = thread_runner.run(simple_identity, [42])
        process_results = process_runner.run(simple_identity, [42])

        expected = [{"value": 42}]
        assert sequential_results == expected
        assert thread_results == expected
        assert process_results == expected


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
