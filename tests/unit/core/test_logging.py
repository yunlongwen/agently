"""Tests for logging configuration"""

from agently.config import Settings, reset_settings
from agently.logging import LoggingMixin, configure_logging, get_logger


class TestConfigureLogging:
    """Test configure_logging function"""

    def test_configure_with_default_settings(self):
        """Test configuration with default settings"""
        reset_settings()
        configure_logging()

        # Check that logging is configured
        logger = get_logger("test")
        # logger should have logging methods
        assert hasattr(logger, "info")
        assert hasattr(logger, "debug")
        assert hasattr(logger, "warning")
        assert hasattr(logger, "error")

    def test_configure_with_custom_settings(self):
        """Test configuration with custom settings"""
        reset_settings()
        settings = Settings(log_level="DEBUG", log_format="text")
        configure_logging(settings)

        # Check that logging is configured
        logger = get_logger("test")
        assert hasattr(logger, "info")
        assert hasattr(logger, "debug")

    def test_configure_with_json_format(self):
        """Test JSON format configuration"""
        reset_settings()
        settings = Settings(log_format="json")
        configure_logging(settings)

        # Check that logging is configured
        logger = get_logger("test")
        assert hasattr(logger, "info")
        assert hasattr(logger, "debug")


class TestGetLogger:
    """Test get_logger function"""

    def test_get_logger_with_name(self):
        """Test getting logger with specific name"""
        logger = get_logger("test_logger")
        # logger should have logging methods
        assert hasattr(logger, "info")
        assert hasattr(logger, "debug")
        assert hasattr(logger, "warning")
        assert hasattr(logger, "error")

    def test_get_logger_without_name(self):
        """Test getting logger without name (uses caller)"""
        logger = get_logger()
        assert hasattr(logger, "info")
        assert hasattr(logger, "debug")

    def test_logger_has_context_methods(self):
        """Test that logger has context methods"""
        logger = get_logger("test")

        # These methods should exist
        assert hasattr(logger, "bind")
        assert hasattr(logger, "info")
        assert hasattr(logger, "debug")
        assert hasattr(logger, "warning")
        assert hasattr(logger, "error")
        assert hasattr(logger, "exception")


class TestLoggingMixin:
    """Test LoggingMixin class"""

    def test_logger_property(self):
        """Test that classes with LoggingMixin have logger property"""

        class TestClass(LoggingMixin):
            pass

        obj = TestClass()
        logger = obj.logger

        # logger should have logging methods
        assert hasattr(logger, "info")
        assert hasattr(logger, "debug")

    def test_logger_logging(self):
        """Test that logger can log messages"""

        class TestClass(LoggingMixin):
            def test_method(self):
                self.logger.info("Test message")

        obj = TestClass()
        # Should not raise any exception
        obj.test_method()
