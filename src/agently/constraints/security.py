"""Security constraints - Security and resource isolation"""

import os
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set


@dataclass
class SecurityPolicy:
    """Security policy configuration"""
    allow_file_write: bool = True
    allow_network: bool = False
    allow_shell: bool = True
    allowed_paths: List[str] = None
    blocked_commands: List[str] = None

    def __post_init__(self):
        if self.allowed_paths is None:
            self.allowed_paths = []
        if self.blocked_commands is None:
            self.blocked_commands = []


class SecurityManager:
    """
    Security Manager - 安全管理器

    管理工具执行的安全隔离和资源限制。
    """

    # Dangerous commands that should be blocked
    DANGEROUS_COMMANDS: Set[str] = {
        "rm -rf /",
        "rm -rf /*",
        "> /dev/sda",
        "mkfs",
        "dd if=/dev/zero",
        ":(){ :|:& };:",  # Fork bomb
        "chmod -R 777 /",
        "mv / /dev/null",
        "reboot",
        "shutdown",
        "poweroff",
        "halt",
    }

    # Suspicious patterns
    SUSPICIOUS_PATTERNS: List[str] = [
        r"rm\s+-rf\s+/",
        r">\s*/dev/sd",
        r"mkfs\.",
        r"dd\s+if=/dev/zero",
        r":\(\)\s*\{\s*:\s*\|:\s*&\s*\};:",
    ]

    def __init__(self, policy: Optional[SecurityPolicy] = None):
        self.policy = policy or SecurityPolicy()
        self.execution_log: List[Dict[str, Any]] = []

    def validate_command(self, command: str) -> Dict[str, Any]:
        """
        Validate a shell command for security

        Args:
            command: Command to validate

        Returns:
            Validation result
        """
        # Check against dangerous commands
        for dangerous in self.DANGEROUS_COMMANDS:
            if dangerous in command:
                return {
                    "allowed": False,
                    "reason": f"Dangerous command detected: {dangerous}",
                    "risk_level": "critical",
                }

        # Check suspicious patterns
        for pattern in self.SUSPICIOUS_PATTERNS:
            if re.search(pattern, command):
                return {
                    "allowed": False,
                    "reason": f"Suspicious pattern detected: {pattern}",
                    "risk_level": "high",
                }

        # Check if shell execution is allowed
        if not self.policy.allow_shell:
            return {
                "allowed": False,
                "reason": "Shell execution is disabled by policy",
                "risk_level": "medium",
            }

        return {
            "allowed": True,
            "reason": "Command passed security checks",
            "risk_level": "low",
        }

    def validate_file_access(self, path: str, mode: str = "read") -> Dict[str, Any]:
        """
        Validate file access

        Args:
            path: File path
            mode: Access mode (read/write)

        Returns:
            Validation result
        """
        # Resolve to absolute path
        abs_path = os.path.abspath(os.path.expanduser(path))

        # Check write permissions
        if mode == "write" and not self.policy.allow_file_write:
            return {
                "allowed": False,
                "reason": "File write is disabled by policy",
            }

        # Check allowed paths
        if self.policy.allowed_paths:
            allowed = any(
                abs_path.startswith(os.path.abspath(allowed_path))
                for allowed_path in self.policy.allowed_paths
            )
            if not allowed:
                return {
                    "allowed": False,
                    "reason": f"Path {abs_path} is not in allowed paths",
                }

        # Check for sensitive paths
        sensitive_paths = [
            "/etc/passwd",
            "/etc/shadow",
            "/etc/ssh",
            "/root",
        ]
        for sensitive in sensitive_paths:
            if abs_path.startswith(sensitive):
                return {
                    "allowed": False,
                    "reason": f"Access to sensitive path {sensitive} is not allowed",
                }

        return {
            "allowed": True,
            "resolved_path": abs_path,
        }

    def validate_network_access(self, url: str) -> Dict[str, Any]:
        """Validate network access"""
        if not self.policy.allow_network:
            return {
                "allowed": False,
                "reason": "Network access is disabled by policy",
            }

        # Check for internal/private IPs
        blocked_patterns = [
            r"^http://127\.",
            r"^http://10\.",
            r"^http://192\.168\.",
            r"^http://localhost",
            r"^http://0\.0\.0\.0",
        ]

        for pattern in blocked_patterns:
            if re.match(pattern, url):
                return {
                    "allowed": False,
                    "reason": f"Access to internal address {url} is not allowed",
                }

        return {
            "allowed": True,
            "url": url,
        }

    def log_execution(self, action: str, details: Dict[str, Any]) -> None:
        """Log security-related execution"""
        import time
        self.execution_log.append({
            "timestamp": time.time(),
            "action": action,
            "details": details,
        })

    def get_execution_log(self) -> List[Dict[str, Any]]:
        """Get execution log"""
        return self.execution_log.copy()

    def clear_log(self) -> None:
        """Clear execution log"""
        self.execution_log.clear()


class ResourceLimiter:
    """
    Resource Limiter - 资源限制器

    限制CPU、内存、磁盘等资源使用。
    """

    def __init__(self):
        self.limits: Dict[str, float] = {
            "cpu_percent": 80.0,
            "memory_mb": 2048.0,
            "disk_mb": 1024.0,
            "file_descriptors": 100,
        }
        self.current_usage: Dict[str, float] = {}

    def set_limit(self, resource: str, limit: float) -> None:
        """Set resource limit"""
        self.limits[resource] = limit

    def get_limit(self, resource: str) -> Optional[float]:
        """Get resource limit"""
        return self.limits.get(resource)

    def check_resource(self, resource: str, usage: float) -> Dict[str, Any]:
        """Check if resource usage is within limit"""
        limit = self.limits.get(resource)
        if limit is None:
            return {
                "within_limit": True,
                "resource": resource,
                "usage": usage,
                "limit": None,
            }

        within_limit = usage < limit
        usage_percent = (usage / limit * 100) if limit > 0 else 0

        status = "ok"
        if usage_percent > 95:
            status = "critical"
        elif usage_percent > 80:
            status = "warning"

        return {
            "within_limit": within_limit,
            "resource": resource,
            "usage": usage,
            "limit": limit,
            "usage_percent": usage_percent,
            "status": status,
        }

    def get_all_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all resources"""
        return {
            resource: self.check_resource(resource, self.current_usage.get(resource, 0))
            for resource in self.limits.keys()
        }

    def update_usage(self, resource: str, usage: float) -> None:
        """Update current resource usage"""
        self.current_usage[resource] = usage

    def enforce_limits(self) -> Dict[str, Any]:
        """Enforce all resource limits"""
        violations = []

        for resource, limit in self.limits.items():
            usage = self.current_usage.get(resource, 0)
            if usage >= limit:
                violations.append({
                    "resource": resource,
                    "usage": usage,
                    "limit": limit,
                })

        return {
            "compliant": len(violations) == 0,
            "violations": violations,
        }
