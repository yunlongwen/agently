"""Memory constraints - Memory usage limiting and tracking"""

import os
import sys
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class MemorySnapshot:
    """Memory usage snapshot"""
    label: str
    rss_mb: float
    vms_mb: float
    timestamp: float = field(default_factory=lambda: __import__('time').time())


class MemoryLimiter:
    """
    Memory Limiter - 内存限制器

    限制内存使用，防止超过设定的内存上限（默认4GB）。
    """

    def __init__(self, max_mb: int = 4096):
        """
        Initialize memory limiter

        Args:
            max_mb: Maximum memory limit in MB (default: 4096 MB = 4GB)
        """
        self.max_mb = max_mb
        self.warning_threshold = 0.8  # 80% warning
        self.critical_threshold = 0.95  # 95% critical

    def get_current_memory_mb(self) -> float:
        """Get current memory usage in MB"""
        try:
            import psutil
            process = psutil.Process(os.getpid())
            return process.memory_info().rss / (1024 * 1024)
        except ImportError:
            # Fallback: try reading from /proc on Linux
            try:
                with open(f'/proc/{os.getpid()}/status', 'r') as f:
                    for line in f:
                        if line.startswith('VmRSS:'):
                            # Parse value like "VmRSS:   12345 kB"
                            parts = line.split()
                            if len(parts) >= 2:
                                kb = int(parts[1])
                                return kb / 1024
            except (FileNotFoundError, ValueError):
                pass
            return 0.0

    def check_memory(self) -> Dict[str, Any]:
        """Check current memory status"""
        current_mb = self.get_current_memory_mb()
        usage_percent = current_mb / self.max_mb

        status = "normal"
        if usage_percent >= self.critical_threshold:
            status = "critical"
        elif usage_percent >= self.warning_threshold:
            status = "warning"

        return {
            "current_mb": current_mb,
            "max_mb": self.max_mb,
            "usage_percent": usage_percent * 100,
            "status": status,
            "available_mb": self.max_mb - current_mb,
        }

    def is_within_limit(self) -> bool:
        """Check if memory usage is within limit"""
        status = self.check_memory()
        return status["current_mb"] < self.max_mb

    def enforce_limit(self) -> bool:
        """
        Enforce memory limit

        Returns:
            True if within limit, False if exceeded
        """
        if not self.is_within_limit():
            # Try garbage collection
            import gc
            gc.collect()

            # Check again
            if not self.is_within_limit():
                return False

        return True

    def get_memory_info(self) -> Dict[str, Any]:
        """Get detailed memory information"""
        try:
            import psutil
            process = psutil.Process(os.getpid())
            mem_info = process.memory_info()

            return {
                "rss_mb": mem_info.rss / (1024 * 1024),
                "vms_mb": mem_info.vms / (1024 * 1024),
                "shared_mb": getattr(mem_info, 'shared', 0) / (1024 * 1024),
                "text_mb": getattr(mem_info, 'text', 0) / (1024 * 1024),
                "lib_mb": getattr(mem_info, 'lib', 0) / (1024 * 1024),
                "data_mb": getattr(mem_info, 'data', 0) / (1024 * 1024),
                "dirty_mb": getattr(mem_info, 'dirty', 0) / (1024 * 1024),
            }
        except ImportError:
            current = self.get_current_memory_mb()
            return {
                "rss_mb": current,
                "vms_mb": current,
            }


class MemoryTracker:
    """
    Memory Tracker - 内存追踪器

    追踪内存使用变化，分析内存趋势。
    """

    def __init__(self):
        self.snapshots: List[MemorySnapshot] = []
        self.limiter = MemoryLimiter()

    def take_snapshot(self, label: str) -> MemorySnapshot:
        """Take a memory snapshot"""
        info = self.limiter.get_memory_info()
        snapshot = MemorySnapshot(
            label=label,
            rss_mb=info.get("rss_mb", 0),
            vms_mb=info.get("vms_mb", 0),
        )
        self.snapshots.append(snapshot)
        return snapshot

    def get_usage_trend(self) -> Dict[str, Any]:
        """Get memory usage trend"""
        if len(self.snapshots) < 2:
            return {"trend": "insufficient_data"}

        first = self.snapshots[0]
        last = self.snapshots[-1]

        rss_diff = last.rss_mb - first.rss_mb
        vms_diff = last.vms_mb - first.vms_mb
        time_diff = last.timestamp - first.timestamp

        trend = "stable"
        if rss_diff > 10:  # More than 10MB increase
            trend = "increasing"
        elif rss_diff < -10:  # More than 10MB decrease
            trend = "decreasing"

        return {
            "trend": trend,
            "rss_diff_mb": rss_diff,
            "vms_diff_mb": vms_diff,
            "time_diff_seconds": time_diff,
            "snapshots_count": len(self.snapshots),
        }

    def get_peak_memory(self) -> Dict[str, float]:
        """Get peak memory usage"""
        if not self.snapshots:
            return {"rss_mb": 0, "vms_mb": 0}

        peak_rss = max(s.rss_mb for s in self.snapshots)
        peak_vms = max(s.vms_mb for s in self.snapshots)

        return {
            "rss_mb": peak_rss,
            "vms_mb": peak_vms,
        }

    def clear_history(self) -> None:
        """Clear snapshot history"""
        self.snapshots.clear()
