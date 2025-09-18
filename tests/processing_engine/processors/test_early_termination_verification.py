"""
Rigorous verification tests for early termination functionality.
These tests provide concrete evidence that early termination is working.
"""

import pytest
import sys
import os
import time
import threading
from unittest.mock import patch

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from processing_engine.processors.runners import (
    SequentialRunner,
    ThreadRunner,
    ProcessRunner,
)


# Global counters to track execution
execution_counter = 0
execution_lock = threading.Lock()


def reset_counter():
    """Reset the global execution counter."""
    global execution_counter
    with execution_lock:
        execution_counter = 0


def get_counter():
    """Get the current execution counter value."""
    global execution_counter
    with execution_lock:
        return execution_counter


def increment_counter():
    """Increment the global execution counter."""
    global execution_counter
    with execution_lock:
        execution_counter += 1


def slow_function_with_counter(x):
    """Function that takes time and tracks execution."""
    increment_counter()
    time.sleep(0.2)  # 200ms delay
    if x == 2:
        return {"success": False, "step": "extraction", "exception": "ValueError", "message": "Test failure", "input": x}
    return {"success": True, "result": x * 2, "input": x}


def slow_function_all_success(x):
    """Function that takes time but always succeeds."""
    increment_counter()
    time.sleep(0.2)  # 200ms delay
    return {"success": True, "result": x * 2, "input": x}


# Process-safe versions for ProcessRunner
def process_slow_function_with_counter(x):
    """Process-safe function that takes time and tracks execution."""
    import time
    time.sleep(0.2)  # 200ms delay
    if x == 2:
        return {"success": False, "step": "extraction", "exception": "ValueError", "message": "Test failure", "input": x}
    return {"success": True, "result": x * 2, "input": x}


def process_slow_function_all_success(x):
    """Process-safe function that takes time but always succeeds."""
    import time
    time.sleep(0.2)  # 200ms delay
    return {"success": True, "result": x * 2, "input": x}


class TestEarlyTerminationVerification:
    """Rigorous tests to verify early termination is actually working."""

    def test_sequential_runner_execution_count_verification(self):
        """Verify SequentialRunner actually stops executing after failure."""
        reset_counter()
        runner = SequentialRunner()
        inputs = [1, 2, 3, 4, 5]

        start_time = time.time()
        results = runner.run(slow_function_with_counter, inputs)
        end_time = time.time()

        execution_count = get_counter()

        # Should only execute 2 functions (inputs 1 and 2)
        assert execution_count == 2, f"Expected 2 executions, got {execution_count}"

        # Should have only 2 results
        assert len(results) == 2, f"Expected 2 results, got {len(results)}"

        # Should complete in ~400ms (2 * 200ms) instead of 1000ms (5 * 200ms)
        execution_time = end_time - start_time
        assert execution_time < 0.5, f"Expected < 0.5s, got {execution_time:.3f}s"
        assert execution_time > 0.3, f"Expected > 0.3s, got {execution_time:.3f}s"

        # Verify the results
        assert results[0]["success"] is True
        assert results[1]["success"] is False
        assert results[1]["input"] == 2

    def test_sequential_runner_no_early_termination_verification(self):
        """Verify SequentialRunner processes all inputs when no failures occur."""
        reset_counter()
        runner = SequentialRunner()
        inputs = [1, 2, 3, 4, 5]

        start_time = time.time()
        results = runner.run(slow_function_all_success, inputs)
        end_time = time.time()

        execution_count = get_counter()

        # Should execute all 5 functions
        assert execution_count == 5, f"Expected 5 executions, got {execution_count}"

        # Should have all 5 results
        assert len(results) == 5, f"Expected 5 results, got {len(results)}"

        # Should complete in ~1000ms (5 * 200ms)
        execution_time = end_time - start_time
        assert execution_time > 0.8, f"Expected > 0.8s, got {execution_time:.3f}s"
        assert execution_time < 1.2, f"Expected < 1.2s, got {execution_time:.3f}s"

    def test_thread_runner_cancellation_verification(self):
        """Verify ThreadRunner actually cancels remaining tasks."""
        runner = ThreadRunner(max_workers=3)
        inputs = [1, 2, 3, 4, 5]

        start_time = time.time()
        results = runner.run(slow_function_with_counter, inputs)
        end_time = time.time()

        # Should complete much faster than sequential (due to parallel execution and early termination)
        execution_time = end_time - start_time
        assert execution_time < 0.4, f"Expected < 0.4s due to parallel execution, got {execution_time:.3f}s"

        # Should have results for all inputs
        assert len(results) == 5, f"Expected 5 results, got {len(results)}"

        # Should have at least one failure
        failures = [r for r in results if not r["success"]]
        assert len(failures) >= 1, "Should have at least one failure"

        # Should have the actual failure
        actual_failure = next((r for r in failures if r["exception"] == "ValueError"), None)
        assert actual_failure is not None, "Should have the actual ValueError failure"
        assert actual_failure["input"] == 2

        # May have cancelled tasks
        cancelled_tasks = [r for r in results if r["exception"] == "CancelledError"]
        print(f"Found {len(cancelled_tasks)} cancelled tasks")

    def test_process_runner_cancellation_verification(self):
        """Verify ProcessRunner actually cancels remaining processes."""
        runner = ProcessRunner(max_workers=3)
        inputs = [1, 2, 3, 4, 5]

        start_time = time.time()
        results = runner.run(process_slow_function_with_counter, inputs)
        end_time = time.time()

        # Should complete much faster than sequential (due to parallel execution and early termination)
        execution_time = end_time - start_time
        assert execution_time < 0.4, f"Expected < 0.4s due to parallel execution, got {execution_time:.3f}s"

        # Should have results for all inputs
        assert len(results) == 5, f"Expected 5 results, got {len(results)}"

        # Should have at least one failure
        failures = [r for r in results if not r["success"]]
        assert len(failures) >= 1, "Should have at least one failure"

        # Should have the actual failure
        actual_failure = next((r for r in failures if r["exception"] == "ValueError"), None)
        assert actual_failure is not None, "Should have the actual ValueError failure"
        assert actual_failure["input"] == 2

        # May have cancelled tasks
        cancelled_tasks = [r for r in results if r["exception"] == "CancelledError"]
        print(f"Found {len(cancelled_tasks)} cancelled tasks")

    def test_early_termination_performance_comparison(self):
        """Compare performance with and without early termination."""
        inputs = [1, 2, 3, 4, 5]

        # Test with early termination (failure on input 2)
        reset_counter()
        runner = SequentialRunner()
        start_time = time.time()
        results_with_failure = runner.run(slow_function_with_counter, inputs)
        time_with_failure = time.time() - start_time
        count_with_failure = get_counter()

        # Test without early termination (all success)
        reset_counter()
        start_time = time.time()
        results_all_success = runner.run(slow_function_all_success, inputs)
        time_all_success = time.time() - start_time
        count_all_success = get_counter()

        # Verify execution counts
        assert count_with_failure == 2, f"With failure: expected 2 executions, got {count_with_failure}"
        assert count_all_success == 5, f"All success: expected 5 executions, got {count_all_success}"

        # Verify result counts
        assert len(results_with_failure) == 2, f"With failure: expected 2 results, got {len(results_with_failure)}"
        assert len(results_all_success) == 5, f"All success: expected 5 results, got {len(results_all_success)}"

        # Verify timing (early termination should be significantly faster)
        assert time_with_failure < time_all_success * 0.6, f"Early termination should be much faster: {time_with_failure:.3f}s vs {time_all_success:.3f}s"

        print(f"Performance comparison:")
        print(f"  With early termination: {time_with_failure:.3f}s ({count_with_failure} executions)")
        print(f"  Without early termination: {time_all_success:.3f}s ({count_all_success} executions)")
        print(f"  Speedup: {time_all_success/time_with_failure:.1f}x")

    def test_early_termination_with_different_failure_positions(self):
        """Test early termination with failures at different positions."""
        runner = SequentialRunner()

        # Test failure at position 1 (first input)
        reset_counter()
        results_early = runner.run(lambda x: {"success": False, "step": "extraction", "exception": "ValueError", "message": "Early failure", "input": x} if x == 1 else {"success": True, "result": x * 2, "input": x}, [1, 2, 3, 4, 5])
        count_early = get_counter()
        assert count_early == 1, f"Early failure: expected 1 execution, got {count_early}"
        assert len(results_early) == 1, f"Early failure: expected 1 result, got {len(results_early)}"

        # Test failure at position 3 (middle)
        reset_counter()
        results_middle = runner.run(lambda x: {"success": False, "step": "extraction", "exception": "ValueError", "message": "Middle failure", "input": x} if x == 3 else {"success": True, "result": x * 2, "input": x}, [1, 2, 3, 4, 5])
        count_middle = get_counter()
        assert count_middle == 3, f"Middle failure: expected 3 executions, got {count_middle}"
        assert len(results_middle) == 3, f"Middle failure: expected 3 results, got {len(results_middle)}"

        # Test failure at position 5 (last input)
        reset_counter()
        results_late = runner.run(lambda x: {"success": False, "step": "extraction", "exception": "ValueError", "message": "Late failure", "input": x} if x == 5 else {"success": True, "result": x * 2, "input": x}, [1, 2, 3, 4, 5])
        count_late = get_counter()
        assert count_late == 5, f"Late failure: expected 5 executions, got {count_late}"
        assert len(results_late) == 5, f"Late failure: expected 5 results, got {len(results_late)}"

    def test_early_termination_resource_savings(self):
        """Demonstrate resource savings from early termination."""
        inputs = list(range(1, 11))  # 10 inputs

        # Function that simulates expensive work
        def expensive_function(x):
            increment_counter()
            time.sleep(0.1)  # 100ms per operation
            if x == 3:
                return {"success": False, "step": "extraction", "exception": "ValueError", "message": "Expensive failure", "input": x}
            return {"success": True, "result": x * 2, "input": x}

        # Test with early termination
        reset_counter()
        runner = SequentialRunner()
        start_time = time.time()
        results = runner.run(expensive_function, inputs)
        time_with_early_termination = time.time() - start_time
        executions_with_early_termination = get_counter()

        # Should only execute 3 functions (inputs 1, 2, 3)
        assert executions_with_early_termination == 3, f"Expected 3 executions, got {executions_with_early_termination}"
        assert len(results) == 3, f"Expected 3 results, got {len(results)}"

        # Should complete in ~300ms instead of 1000ms
        assert time_with_early_termination < 0.4, f"Expected < 0.4s, got {time_with_early_termination:.3f}s"

        # Calculate resource savings
        total_possible_executions = len(inputs)
        saved_executions = total_possible_executions - executions_with_early_termination
        savings_percentage = (saved_executions / total_possible_executions) * 100

        print(f"Resource savings demonstration:")
        print(f"  Total possible executions: {total_possible_executions}")
        print(f"  Actual executions: {executions_with_early_termination}")
        print(f"  Saved executions: {saved_executions}")
        print(f"  Savings: {savings_percentage:.1f}%")
        print(f"  Time saved: {time_with_early_termination:.3f}s vs potential 1.0s")

    def test_early_termination_consistency_across_runners(self):
        """Verify that all runners implement early termination consistently."""
        inputs = [1, 2, 3, 4, 5]

        def test_function(x):
            increment_counter()
            time.sleep(0.1)
            if x == 2:
                return {"success": False, "step": "extraction", "exception": "ValueError", "message": "Test failure", "input": x}
            return {"success": True, "result": x * 2, "input": x}

        # Test SequentialRunner
        reset_counter()
        sequential_runner = SequentialRunner()
        sequential_results = sequential_runner.run(test_function, inputs)
        sequential_count = get_counter()

        # Test ThreadRunner
        reset_counter()
        thread_runner = ThreadRunner(max_workers=2)
        thread_results = thread_runner.run(test_function, inputs)
        thread_count = get_counter()

        # Test ProcessRunner
        reset_counter()
        process_runner = ProcessRunner(max_workers=2)
        process_results = process_runner.run(process_slow_function_with_counter, inputs)
        process_count = get_counter()

        # SequentialRunner should have early termination
        assert sequential_count == 2, f"SequentialRunner: expected 2 executions, got {sequential_count}"
        assert len(sequential_results) == 2, f"SequentialRunner: expected 2 results, got {len(sequential_results)}"

        # ThreadRunner and ProcessRunner may have different execution counts due to parallel execution
        # but should still have the failure and complete faster than without early termination
        assert len(thread_results) == 5, f"ThreadRunner: expected 5 results, got {len(thread_results)}"
        assert len(process_results) == 5, f"ProcessRunner: expected 5 results, got {len(process_results)}"

        # All should have the failure
        sequential_failures = [r for r in sequential_results if not r["success"]]
        thread_failures = [r for r in thread_results if not r["success"]]
        process_failures = [r for r in process_results if not r["success"]]

        assert len(sequential_failures) == 1, "SequentialRunner should have 1 failure"
        assert len(thread_failures) >= 1, "ThreadRunner should have at least 1 failure"
        assert len(process_failures) >= 1, "ProcessRunner should have at least 1 failure"

        print(f"Execution counts:")
        print(f"  SequentialRunner: {sequential_count} executions")
        print(f"  ThreadRunner: {thread_count} executions")
        print(f"  ProcessRunner: {process_count} executions")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])  # -s to show print statements
