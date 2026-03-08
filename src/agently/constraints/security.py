"""Security constraint management"""

import re
from dataclasses import dataclass, field
from typing import Any


class SecurityManager:
    """Manages security constraints"""

    def __init__(self):
        self.blocked_commands = [
            r"rm\s+-rf\s+/",
            r"dd\s+if=",
            r"mkfs",
            r":(){ :|:& };:",
            r"chmod\s+777",
            r">\s*/dev/sd",
        ]

    def validate_command(self, command: str) -> dict[str, Any]:
        """Validate a shell command

        Args:
            command: Command to validate

        Returns:
            Validation result with 'allowed' flag
        """
        for pattern in self.blocked_commands:
            if re.search(pattern, command, re.IGNORECASE):
                return {
                    "allowed": False,
                    "reason": f"Blocked command pattern: {pattern}",
                }
        return {"allowed": True}

    def sanitize_input(self, input_str: str) -> str:
        """Sanitize user input

        Args:
            input_str: Input string

        Returns:
            Sanitized string
        """
        return input_str.strip()


@dataclass
class ResourceLimiter:
    """Limits resource usage"""

    limits: dict[str, Any] = field(
        default_factory=lambda: {
            "cpu_percent": 80.0,
            "memory_mb": 4096,
            "file_size_mb": 100,
            "execution_time_seconds": 300,
        }
    )

    def set_limit(self, resource: str, value: Any) -> None:
        """Set a resource limit

        Args:
            resource: Resource name
            value: Limit value
        """
        self.limits[resource] = value

    def check_resource(self, resource: str, current_value: Any) -> dict[str, Any]:
        """Check if resource usage is within limit

        Args:
            resource: Resource name
            current_value: Current usage value

        Returns:
            Check result with 'within_limit' flag
        """
        limit = self.limits.get(resource)
        if limit is None:
            return {"within_limit": True, "message": "No limit defined"}

        within_limit = current_value <= limit
        return {
            "within_limit": within_limit,
            "current": current_value,
            "limit": limit,
            "message": "Within limit" if within_limit else "Exceeds limit",
        }
