"""Tests for configuration management"""

import os
from pathlib import Path

import pytest
from pydantic import ValidationError

from agently.config import Settings, get_settings, reset_settings
class TestSettings:
    """Test Settings class"""

    def test_default_values(self):
        """Test default configuration values"""
        settings = Settings()

        assert settings.openai_api_key == ""
        assert settings.openai_model == "gpt-4"
        assert settings.openai_temperature == 0.7
        assert settings.openai_max_tokens == 4096

        assert settings.anthropic_api_key == ""
        assert settings.anthropic_model == "claude-3-opus-20240229"
        assert settings.anthropic_max_tokens == 4096

        assert settings.log_level == "INFO"
        assert settings.log_format == "json"

        assert settings.max_memory_mb == 4096
        assert settings.max_concurrent_sessions == 5
        assert settings.timeout_simple == 30
        assert settings.timeout_medium == 60
        assert settings.timeout_complex == 120

    def test_env_variables(self):
        """Test loading from environment variables"""
        # Set environment variables
        os.environ["AGENTLY_OPENAI_API_KEY"] = "test-key"
        os.environ["AGENTLY_OPENAI_MODEL"] = "gpt-3.5-turbo"
        os.environ["AGENTLY_LOG_LEVEL"] = "DEBUG"
        os.environ["AGENTLY_MAX_MEMORY_MB"] = "8192"

        settings = Settings()

        assert settings.openai_api_key == "test-key"
        assert settings.openai_model == "gpt-3.5-turbo"
        assert settings.log_level == "DEBUG"
        assert settings.max_memory_mb == 8192

        # Cleanup
        del os.environ["AGENTLY_OPENAI_API_KEY"]
        del os.environ["AGENTLY_OPENAI_MODEL"]
        del os.environ["AGENTLY_LOG_LEVEL"]
        del os.environ["AGENTLY_MAX_MEMORY_MB"]

    def test_validation(self):
        """Test configuration validation"""
        # Test temperature validation
        settings = Settings(openai_temperature=0.5)
        assert settings.openai_temperature == 0.5

        with pytest.raises(ValidationError):
            Settings(openai_temperature=-0.1)

        with pytest.raises(ValidationError):
            Settings(openai_temperature=2.1)
    def test_paths(self):
        """Test default paths"""
        settings = Settings()

        assert isinstance(settings.project_root, Path)
        assert isinstance(settings.config_dir, Path)
        assert isinstance(settings.cache_dir, Path)

        assert settings.config_dir == Path.home() / ".config" / "agently"
        assert settings.cache_dir == Path.home() / ".cache" / "agently"


class TestGlobalSettings:
    """Test global settings singleton"""

    def test_get_settings_singleton(self):
        """Test get_settings returns singleton"""
        reset_settings()

        settings1 = get_settings()
        settings2 = get_settings()

        assert settings1 is settings2

    def test_reset_settings(self):
        """Test reset_settings clears singleton"""
        reset_settings()

        settings1 = get_settings()
        reset_settings()
        settings2 = get_settings()

        assert settings1 is not settings2
