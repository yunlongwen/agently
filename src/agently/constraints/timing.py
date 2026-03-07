"""Timing constraints - Response time monitoring and timeout management"""

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TimingMeasurement:
    """Timing measurement record"""
    task: str
    duration_seconds: float
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)


class ResponseTimeMonitor:
    """
    Response Time Monitor - 响应时间监控器

    监控任务响应时间，确保满足时间约束。
    """

    # Time constraints in seconds
    SIMPLE_TASK_TIMEOUT = 30
    MODERATE_TASK_TIMEOUT = 60
    COMPLEX_TASK_TIMEOUT = 120

    def __init__(self):
        self.measurements: List[TimingMeasurement] = []
        self.timers: Dict[str, float] = {}

    def start_timer(self, task_id: str) -> None:
        """Start a timer for a task"""
        self.timers[task_id] = time.time()

    def stop_timer(self, task_id: str) -> Optional[float]:
        """Stop a timer and record the measurement"""
        if task_id not in self.timers:
            return None

        start_time = self.timers.pop(task_id)
        duration = time.time() - start_time

        measurement = TimingMeasurement(
            task=task_id,
            duration_seconds=duration,
        )
        self.measurements.append(measurement)

        return duration

    def measure(self, task_id: str) -> Optional[TimingMeasurement]:
        """Get the last measurement for a task"""
        for m in reversed(self.measurements):
            if m.task == task_id:
                return m
        return None

    def get_average_response_time(self, task_pattern: Optional[str] = None) -> float:
        """Get average response time"""
        if not self.measurements:
            return 0.0

        if task_pattern:
            times = [m.duration_seconds for m in self.measurements
                     if task_pattern in m.task]
        else:
            times = [m.duration_seconds for m in self.measurements]

        if not times:
            return 0.0

        return sum(times) / len(times)

    def get_percentile(self, percentile: float) -> float:
        """Get response time at given percentile"""
        if not self.measurements:
            return 0.0

        times = sorted(m.duration_seconds for m in self.measurements)
        index = int(len(times) * percentile / 100)
        return times[min(index, len(times) - 1)]

    def check_response_time(self, task: str, actual_time: float) -> Dict[str, Any]:
        """Check if response time meets constraints"""
        expected_timeout = self.get_timeout_for_task(task)

        status = "ok"
        if actual_time > expected_timeout:
            status = "exceeded"
        elif actual_time > expected_timeout * 0.8:
            status = "warning"

        return {
            "task": task,
            "actual_seconds": actual_time,
            "expected_seconds": expected_timeout,
            "status": status,
        }

    def get_timeout_for_task(self, task: str) -> int:
        """Get appropriate timeout for task based on complexity"""
        task_lower = task.lower()
        words = len(task.split())

        # Simple tasks: short, single action
        simple_indicators = ["简单", "quick", "simple", "check", "show", "list"]
        if any(ind in task_lower for ind in simple_indicators) or words < 10:
            return self.SIMPLE_TASK_TIMEOUT

        # Complex tasks: long, multiple actions
        complex_indicators = ["复杂", "complex", "analyze", "refactor", "multiple", "entire"]
        if any(ind in task_lower for ind in complex_indicators) or words > 50:
            return self.COMPLEX_TASK_TIMEOUT

        # Moderate tasks: everything else
        return self.MODERATE_TASK_TIMEOUT

    def clear_measurements(self) -> None:
        """Clear all measurements"""
        self.measurements.clear()
        self.timers.clear()


class TimeoutManager:
    """
    Timeout Manager - 超时管理器

    管理不同任务类型的超时设置。
    """

    def __init__(self):
        self.timeouts: Dict[str, int] = {
            "simple": 30,
            "moderate": 60,
            "complex": 120,
        }
        self.custom_timeouts: Dict[str, int] = {}

    def set_timeout(self, task_type: str, seconds: int) -> None:
        """Set timeout for a task type"""
        self.timeouts[task_type] = seconds

    def set_custom_timeout(self, task_id: str, seconds: int) -> None:
        """Set custom timeout for a specific task"""
        self.custom_timeouts[task_id] = seconds

    def get_timeout(self, task_type: str = "moderate") -> int:
        """Get timeout for a task type"""
        return self.timeouts.get(task_type, 60)

    def get_timeout_for_task(self, task: str) -> int:
        """Determine timeout based on task description"""
        task_lower = task.lower()
        words = len(task.split())

        # Check for custom timeout first
        for task_id, timeout in self.custom_timeouts.items():
            if task_id in task:
                return timeout

        # Determine by complexity
        if words < 10:
            return self.timeouts["simple"]
        elif words > 50:
            return self.timeouts["complex"]
        else:
            return self.timeouts["moderate"]

    def with_timeout(self, func, timeout_seconds: int):
        """Execute function with timeout"""
        import signal
        from functools import wraps

        def timeout_handler(signum, frame):
            raise TimeoutError(f"Function execution exceeded {timeout_seconds} seconds")

        @wraps(func)
        def wrapper(*args, **kwargs):
            # Set the alarm
            old_handler = signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(timeout_seconds)

            try:
                result = func(*args, **kwargs)
                return result
            finally:
                signal.alarm(0)
                signal.signal(signal.SIGALRM, old_handler)

        return wrapper
