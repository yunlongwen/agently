"""Logging configuration using structlog"""

import logging
import sys
from typing import Optional

import structlog

from agently.config import Settings, get_settings


def configure_logging(settings: Optional[Settings] = None) -> None:
    """Configure structured logging with structlog

    Args:
        settings: Application settings. If None, uses global settings.
    """
    if settings is None:
        settings = get_settings()

    # Configure standard logging to work with structlog
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.log_level.upper()),
    )

    # Configure structlog processors
    processors: list[object] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
    ]

    if settings.log_format == "json":
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer(colors=True))

    structlog.configure(
        processors=processors,  # type: ignore[arg-type]
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, settings.log_level.upper())
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: Optional[str] = None) -> structlog.BoundLogger:
    """Get a structured logger

    Args:
        name: Logger name. If None, uses caller's module name.

    Returns:
        Structured logger instance
    """
    logger = structlog.get_logger(name)
    return logger  # type: ignore[no-any-return]


class LoggingMixin:
    """Mixin class to add logging capability to any class"""

    @property
    def logger(self) -> structlog.BoundLogger:
        """Get logger for this class"""
        return get_logger(self.__class__.__name__)
