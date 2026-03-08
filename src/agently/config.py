"""
Configuration Management Module
"""

from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class OpenAIConfig(BaseModel):
    """OpenAI configuration"""

    api_key: str = Field(default="", description="OpenAI API key")
    model: str = Field(default="gpt-4", description="Model name")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Temperature")
    max_tokens: int = Field(default=4096, gt=0, description="Max tokens")


class AnthropicConfig(BaseModel):
    """Anthropic configuration"""

    api_key: str = Field(default="", description="Anthropic API key")
    model: str = Field(default="claude-3-opus-20240229", description="Model name")
    max_tokens: int = Field(default=4096, gt=0, description="Max tokens")


class LogConfig(BaseModel):
    """Logging configuration"""

    level: str = Field(default="INFO", description="Log level")
    format: str = Field(default="json", description="Log format (json or text)")


class Settings(BaseSettings):
    """Application settings"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_prefix="AGENTLY_",
    )

    # OpenAI configuration
    openai_api_key: str = Field(default="", description="OpenAI API key")
    openai_model: str = Field(default="gpt-4", description="Model name")
    openai_temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Temperature")
    openai_max_tokens: int = Field(default=4096, gt=0, description="Max tokens")

    # Anthropic configuration
    anthropic_api_key: str = Field(default="", description="Anthropic API key")
    anthropic_model: str = Field(default="claude-3-opus-20240229", description="Model name")
    anthropic_max_tokens: int = Field(default=4096, gt=0, description="Max tokens")

    # Logging
    log_level: str = Field(default="INFO", description="Log level")
    log_format: str = Field(default="json", description="Log format")

    # Project paths
    project_root: Path = Field(default_factory=lambda: Path.cwd())
    config_dir: Path = Field(default_factory=lambda: Path.home() / ".config" / "agently")
    cache_dir: Path = Field(default_factory=lambda: Path.home() / ".cache" / "agently")

    # Performance constraints
    max_memory_mb: int = Field(default=4096, ge=1, description="Max memory MB")
    max_concurrent_sessions: int = Field(
        default=5, ge=1, le=10, description="Max concurrent sessions"
    )
    timeout_simple: int = Field(default=30, ge=1, description="Simple timeout seconds")
    timeout_medium: int = Field(default=60, ge=1, description="Medium timeout seconds")
    timeout_complex: int = Field(default=120, ge=1, description="Complex timeout seconds")


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get global settings instance"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def reset_settings() -> None:
    """Reset global settings (mainly for testing)"""
    global _settings
    _settings = None
