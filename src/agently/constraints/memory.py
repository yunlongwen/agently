"""Memory constraint management"""

import os
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class MemorySnapshot:
    """Memory usage snapshot"""
    timestamp: float
    memory_mb: float
    label: str = ""


class MemoryLimiter:
    """Limits and monitors memory usage"""

    def __init__(self, max_mb: int = 4096):
        self.max_mb = max_mb

    def check_memory(self) -> Dict[str, Any]:
        """Check current memory usage

        Returns:
            Memory usage information
        """
        current_mb = self.get_current_memory_mb()
        return {
            "current_mb": current_mb,
            "max_mb": self.max_mb,
            "percent_used": (current_mb / self.max_mb) * 100,
        }

    def get_current_memory_mb(self) -> float:
        """Get current memory usage in MB

        Returns:
            Memory usage in MB
        """
        try:
            import psutil

            process = psutil.Process(os.getpid())
            return process.memory_info().rss / 1024 / 1024
        except ImportError:
            return 100.0

    def is_within_limit(self) -> bool:
        """Check if memory is within limit

        Returns:
            True if within limit
        """
        return self.get_current_memory_mb() <= self.max_mb


class MemoryTracker:
    """Tracks memory usage over time"""

    def __init__(self):
        self.snapshots: List[MemorySnapshot] = []

    def take_snapshot(self, label: str = "") -> None:
        """Take a memory snapshot

        Args:
            label: Label for the snapshot
        """
        import time

        limiter = MemoryLimiter()
        snapshot = MemorySnapshot(
            timestamp=time.time(),
            memory_mb=limiter.get_current_memory_mb(),
            label=label,
        )
        self.snapshots.append(snapshot)

    def get_usage_trend(self) -> Dict[str, Any]:
        """Get memory usage trend

        Returns:
            Trend information
        """
        if not self.snapshots:
            return {"trend": "unknown"}

        memory_values = [s.memory_mb for s in self.snapshots]
        return {
            "trend": "increasing" if memory_values[-1] > memory_values[0] else "decreasing",
            "min": min(memory_values),
            "max": max(memory_values),
            "current": memory_values[-1],
        }
