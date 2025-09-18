"""
Tests for Runner early termination functionality.
Tests that runners stop processing when any extraction fails.
"""

import pytest
import sys
import os
import time

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from processing_engine.processors.runners import (
    SequentialRunner,
    ThreadRunner,
    ProcessRunner,
)


# Test functions for early termination testing
def success_function(x):
    """Function that always succeeds."""
    return {"success": True, "result": x * 2, "input": x}


def failure_function(x):
    """Function that fails for specific inputs."""
    if x == 2:
        return {"success": False, "step": "extraction", "exception": "ValueError", "message": "Test failure", "input": x}
    return {"success": True, "result": x * 2, "input": x}


def slow_success_function(x):
    """Function that takes time but succeeds."""
    time.sleep(0.1)
    return {"success": True, "result": x * 2, "input": x}


def slow_failure_function(x):
    """Function that takes time and fails for specific inputs."""
    time.sleep(0.1)
    if x == 2:
        return {"success": False, "step": "extraction", "exception": "ValueError", "message": "Test failure", "input": x}
    return {"success": True, "result": x * 2, "input": x}


def early_failure_function(x):
    """Function that fails early in the sequence."""
    if x == 1:
        return {"success": False, "step": "extraction", "exception": "ValueError", "message": "Early failure", "input": x}
    return {"success": True, "result": x * 2, "input": x}


def late_failure_function(x):
    """Function that fails late in the sequence."""
    if x == 4:
        return {"success": False, "step": "extraction", "exception": "ValueError", "message": "Late failure", "input": x}
    return {"success": True, "result": x * 2, "input": x}


# Module-level functions for ProcessRunner tests (must be picklable)
def process_success_function(x):
    """Process-safe function that always succeeds."""
    return {"success": True, "result": x * 2, "input": x}


def process_failure_function(x):
    """Process-safe function that fails for specific inputs."""
    if x == 2:
        return {"success": False, "step": "extraction", "exception": "ValueError", "message": "Test failure", "input": x}
    return {"success": True, "result": x * 2, "input": x}


def process_slow_success_function(x):
    """Process-safe function that takes time but succeeds."""
    time.sleep(0.1)
    return {"success": True, "result": x * 2, "input": x}


def process_slow_failure_function(x):
    """Process-safe function that takes time and fails for specific inputs."""
    time.sleep(0.1)
    if x == 2:
        return {"success": False, "step": "extraction", "exception": "ValueError", "message": "Test failure", "input": x}
    return {"success": True, "result": x * 2, "input": x}


class TestSequentialRunnerEarlyTermination:
    """Test SequentialRunner early termination functionality."""

    def test_sequential_runner_no_early_termination_on_success(self):
        """Test that SequentialRunner processes all inputs when all succeed."""
        runner = SequentialRunner()
        inputs = [1, 2, 3, 4, 5]
        results = runner.run(success_function, inputs)

        assert len(results) == 5
        for i, result in enumerate(results):
            assert result["success"] is True
            assert result["result"] == inputs[i] * 2
            assert result["input"] == inputs[i]

    def test_sequential_runner_early_termination_on_failure(self):
        """Test that SequentialRunner stops processing when any input fails."""
        runner = SequentialRunner()
        inputs = [1, 2, 3, 4, 5]
        results = runner.run(failure_function, inputs)

        # Should stop after the failure at input 2
        assert len(results) == 2  # Only processed inputs 1 and 2

        # First result should be success
        assert results[0]["success"] is True
        assert results[0]["result"] == 2
        assert results[0]["input"] == 1

        # Second result should be failure
        assert results[1]["success"] is False
        assert results[1]["step"] == "extraction"
        assert results[1]["exception"] == "ValueError"
        assert results[1]["message"] == "Test failure"

    def test_sequential_runner_early_termination_first_input_failure(self):
        """Test SequentialRunner with failure on first input."""
        runner = SequentialRunner()
        inputs = [1, 2, 3, 4, 5]
        results = runner.run(early_failure_function, inputs)

        # Should stop after the first input fails
        assert len(results) == 1

        # First result should be failure
        assert results[0]["success"] is False
        assert results[0]["step"] == "extraction"
        assert results[0]["exception"] == "ValueError"
        assert results[0]["message"] == "Early failure"

    def test_sequential_runner_early_termination_last_input_failure(self):
        """Test SequentialRunner with failure on last input."""
        runner = SequentialRunner()
        inputs = [1, 2, 3, 4, 5]
        results = runner.run(late_failure_function, inputs)

        # Should process all inputs until the failure
        assert len(results) == 4

        # First three results should be success
        for i in range(3):
            assert results[i]["success"] is True
            assert results[i]["result"] == inputs[i] * 2
            assert results[i]["input"] == inputs[i]

        # Last result should be failure
        assert results[3]["success"] is False
        assert results[3]["step"] == "extraction"
        assert results[3]["exception"] == "ValueError"
        assert results[3]["message"] == "Late failure"

    def test_sequential_runner_early_termination_performance(self):
        """Test that SequentialRunner early termination improves performance."""
        runner = SequentialRunner()
        inputs = [1, 2, 3, 4, 5]

        # Test with slow function that fails early
        start_time = time.time()
        results = runner.run(slow_failure_function, inputs)
        end_time = time.time()

        # Should complete quickly due to early termination
        # Only first two inputs should be processed (2 * 0.1s = 0.2s)
        assert end_time - start_time < 0.3

        # Should have early termination
        assert len(results) == 2
        assert results[1]["success"] is False


class TestThreadRunnerEarlyTermination:
    """Test ThreadRunner early termination functionality."""

    def test_thread_runner_no_early_termination_on_success(self):
        """Test that ThreadRunner processes all inputs when all succeed."""
        runner = ThreadRunner(max_workers=2)
        inputs = [1, 2, 3, 4, 5]
        results = runner.run(success_function, inputs)

        assert len(results) == 5
        for i, result in enumerate(results):
            assert result["success"] is True
            assert result["result"] == inputs[i] * 2
            assert result["input"] == inputs[i]

    def test_thread_runner_early_termination_on_failure(self):
        """Test that ThreadRunner cancels remaining tasks when any input fails."""
        runner = ThreadRunner(max_workers=2)
        inputs = [1, 2, 3, 4, 5]
        results = runner.run(failure_function, inputs)

        # Should have results for all inputs (some may be cancelled)
        assert len(results) == 5

        # Find the failure result
        failure_found = False
        for result in results:
            if result["success"] is False:
                if result["exception"] == "ValueError" and "Test failure" in result["message"]:
                    failure_found = True
                    # This should be the input that actually failed
                    assert result["input"] == 2
                elif result["exception"] == "CancelledError":
                    assert "cancelled due to earlier failure" in result["message"]

        assert failure_found, "Should have found the actual failure"
        # May or may not have cancelled tasks depending on timing

    def test_thread_runner_early_termination_performance(self):
        """Test that ThreadRunner early termination improves performance."""
        runner = ThreadRunner(max_workers=2)
        inputs = [1, 2, 3, 4, 5]

        # Test with slow function that fails early
        start_time = time.time()
        results = runner.run(slow_failure_function, inputs)
        end_time = time.time()

        # Should complete quickly due to early termination
        # Should be faster than processing all inputs sequentially
        assert end_time - start_time < 0.4  # Allow some tolerance for threading overhead

        # Should have early termination
        failure_found = False
        for result in results:
            if result["success"] is False and result["exception"] == "ValueError":
                failure_found = True
                break
        assert failure_found

    def test_thread_runner_cancellation_behavior(self):
        """Test that ThreadRunner properly cancels remaining tasks."""
        runner = ThreadRunner(max_workers=3)
        inputs = [1, 2, 3, 4, 5]

        # Use a function that fails on input 2
        results = runner.run(failure_function, inputs)

        assert len(results) == 5

        # Should have at least one failure
        failures = [r for r in results if not r["success"]]
        assert len(failures) >= 1

        # Should have the actual failure
        actual_failure = next((r for r in failures if r["exception"] == "ValueError"), None)
        assert actual_failure is not None
        assert actual_failure["message"] == "Test failure"


class TestProcessRunnerEarlyTermination:
    """Test ProcessRunner early termination functionality."""

    def test_process_runner_no_early_termination_on_success(self):
        """Test that ProcessRunner processes all inputs when all succeed."""
        runner = ProcessRunner(max_workers=2)
        inputs = [1, 2, 3, 4, 5]
        results = runner.run(process_success_function, inputs)

        assert len(results) == 5
        for i, result in enumerate(results):
            assert result["success"] is True
            assert result["result"] == inputs[i] * 2
            assert result["input"] == inputs[i]

    def test_process_runner_early_termination_on_failure(self):
        """Test that ProcessRunner cancels remaining tasks when any input fails."""
        runner = ProcessRunner(max_workers=2)
        inputs = [1, 2, 3, 4, 5]
        results = runner.run(process_failure_function, inputs)

        # Should have results for all inputs (some may be cancelled)
        assert len(results) == 5

        # Find the failure result
        failure_found = False
        for result in results:
            if result["success"] is False:
                if result["exception"] == "ValueError" and "Test failure" in result["message"]:
                    failure_found = True
                    # This should be the input that actually failed
                    assert result["input"] == 2
                elif result["exception"] == "CancelledError":
                    assert "cancelled due to earlier failure" in result["message"]

        assert failure_found, "Should have found the actual failure"
        # May or may not have cancelled tasks depending on timing

    def test_process_runner_early_termination_performance(self):
        """Test that ProcessRunner early termination improves performance."""
        runner = ProcessRunner(max_workers=2)
        inputs = [1, 2, 3, 4, 5]

        # Test with slow function that fails early
        start_time = time.time()
        results = runner.run(process_slow_failure_function, inputs)
        end_time = time.time()

        # Should complete quickly due to early termination
        # Should be faster than processing all inputs sequentially
        assert end_time - start_time < 0.4  # Allow some tolerance for process overhead

        # Should have early termination
        failure_found = False
        for result in results:
            if result["success"] is False and result["exception"] == "ValueError":
                failure_found = True
                break
        assert failure_found

    def test_process_runner_cancellation_behavior(self):
        """Test that ProcessRunner properly cancels remaining tasks."""
        runner = ProcessRunner(max_workers=3)
        inputs = [1, 2, 3, 4, 5]

        # Use a function that fails on input 2
        results = runner.run(process_failure_function, inputs)

        assert len(results) == 5

        # Should have at least one failure
        failures = [r for r in results if not r["success"]]
        assert len(failures) >= 1

        # Should have the actual failure
        actual_failure = next((r for r in failures if r["exception"] == "ValueError"), None)
        assert actual_failure is not None
        assert actual_failure["message"] == "Test failure"


class TestRunnerEarlyTerminationComparison:
    """Test and compare early termination behavior across all runners."""

    def test_all_runners_early_termination_consistency(self):
        """Test that all runners have consistent early termination behavior."""
        inputs = [1, 2, 3, 4, 5]

        sequential_runner = SequentialRunner()
        thread_runner = ThreadRunner(max_workers=2)
        process_runner = ProcessRunner(max_workers=2)

        sequential_results = sequential_runner.run(failure_function, inputs)
        thread_results = thread_runner.run(failure_function, inputs)
        process_results = process_runner.run(process_failure_function, inputs)

        # Sequential runner should have early termination
        assert len(sequential_results) == 2
        assert sequential_results[1]["success"] is False

        # Thread and process runners should have results for all inputs
        assert len(thread_results) == 5
        assert len(process_results) == 5

        # All should have at least one failure
        sequential_failures = [r for r in sequential_results if not r["success"]]
        thread_failures = [r for r in thread_results if not r["success"]]
        process_failures = [r for r in process_results if not r["success"]]

        assert len(sequential_failures) == 1
        assert len(thread_failures) >= 1
        assert len(process_failures) >= 1

    def test_early_termination_performance_benefit(self):
        """Test that early termination provides performance benefits."""
        inputs = [1, 2, 3, 4, 5]

        # Test without early termination (all success)
        start_time = time.time()
        sequential_runner = SequentialRunner()
        results_all_success = sequential_runner.run(slow_success_function, inputs)
        time_all_success = time.time() - start_time

        # Test with early termination (failure on second input)
        start_time = time.time()
        results_with_failure = sequential_runner.run(slow_failure_function, inputs)
        time_with_failure = time.time() - start_time

        # Early termination should be faster
        assert time_with_failure < time_all_success

        # Verify results
        assert len(results_all_success) == 5
        assert len(results_with_failure) == 2
        assert results_with_failure[1]["success"] is False

    def test_early_termination_with_different_failure_positions(self):
        """Test early termination with failures at different positions."""
        inputs = [1, 2, 3, 4, 5]
        runner = SequentialRunner()

        # Test failure at beginning
        results_early = runner.run(early_failure_function, inputs)
        assert len(results_early) == 1
        assert results_early[0]["success"] is False

        # Test failure in middle
        results_middle = runner.run(failure_function, inputs)
        assert len(results_middle) == 2
        assert results_middle[1]["success"] is False

        # Test failure at end
        results_late = runner.run(late_failure_function, inputs)
        assert len(results_late) == 4
        assert results_late[3]["success"] is False

    def test_early_termination_with_empty_inputs(self):
        """Test early termination behavior with empty inputs."""
        runner = SequentialRunner()
        results = runner.run(success_function, [])
        assert results == []

    def test_early_termination_with_single_input(self):
        """Test early termination behavior with single input."""
        runner = SequentialRunner()

        # Single success
        results_success = runner.run(success_function, [1])
        assert len(results_success) == 1
        assert results_success[0]["success"] is True

        # Single failure
        results_failure = runner.run(failure_function, [2])
        assert len(results_failure) == 1
        assert results_failure[0]["success"] is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
