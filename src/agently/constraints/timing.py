"""Timing constraint management"""

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TimingMeasurement:
    """Timing measurement record"""
    task: str
    duration_seconds: float
    timestamp: float = field(default_factory=time.time)


class ResponseTimeMonitor:
    """Monitors response times"""

    def __init__(self):
        self.measurements: List[TimingMeasurement] = []
        self.timers: Dict[str, float] = {}

    def start_timer(self, task: str) -> None:
        """Start a timer for a task

        Args:
            task: Task identifier
        """
        self.timers[task] = time.time()

    def stop_timer(self, task: str) -> float:
        """Stop timer and record measurement

        Args:
            task: Task identifier

        Returns:
            Duration in seconds
        """
        if task not in self.timers:
            return 0.0

        duration = time.time() - self.timers[task]
        measurement = TimingMeasurement(task=task, duration_seconds=duration)
        self.measurements.append(measurement)
        del self.timers[task]
        return duration

    def get_average_response_time(self) -> float:
        """Get average response time

        Returns:
            Average duration in seconds
        """
        if not self.measurements:
            return 0.0

        total = sum(m.duration_seconds for m in self.measurements)
        return total / len(self.measurements)


class TimeoutManager:
    """Manages timeouts for different task types"""

    def __init__(self):
        self.timeouts: Dict[str, int] = {
            "simple": 30,
            "medium": 60,
            "complex": 120,
        }

    def set_timeout(self, task_type: str, seconds: int) -> None:
        """Set timeout for a task type

        Args:
            task_type: Type of task
            seconds: Timeout in seconds
        """
        self.timeouts[task_type] = seconds

    def get_timeout_for_task(self, task: str) -> int:
        """Get appropriate timeout for a task

        Args:
            task: Task description

        Returns:
            Timeout in seconds
        """
        word_count = len(task.split())
        if word_count < 10:
            return self.timeouts["simple"]
        elif word_count < 50:
            return self.timeouts["medium"]
        else:
            return self.timeouts["complex"]
