"""Tests for model service"""

from pathlib import Path
from unittest.mock import patch

import pytest

from agently.core.model_service import ModelService


class TestModelService:
    """Test ModelService class"""

    def test_init_service(self):
        """Test initializing model service"""
        from agently.config import Settings

        with patch("agently.core.model_service.OpenAIChat"):
            with patch("agently.core.model_service.AnthropicChat"):
                service = ModelService()

        assert service is not None

    @pytest.mark.parametrize("model_name,api_key_env", [
        ("openai", "AGENTLY_OPENAI_API_KEY"),
        ("anthropic", "AGENTLY_ANTHROPIC_API_KEY"),
    ])
    def test_get_chat_completion(self, tmp_path: Path, model_name, api_key_env):
        """Test getting chat completion from model"""
        import os

        os.environ[api_key_env] = "test-key"
        service = ModelService()

        response = service.get_chat_completion("test prompt")

        assert response is not None
        assert isinstance(response, dict)
        assert "content" in response or "message" in response

    def test_get_chat_completion_no_api_key(self, tmp_path: Path):
        """Test chat completion without API key should raise error"""
        import os

        os.environ["AGENTLY_OPENAI_API_KEY"] = ""
        service = ModelService()

        with pytest.raises(ValueError):
            service.get_chat_completion("test")

    def test_get_embedding(self, tmp_path: Path):
        """Test getting embedding"""
        import os

        os.environ["AGENTLY_OPENAI_API_KEY"] = "test-key"
        service = ModelService()

        embedding = service.get_embedding("test text")

        assert embedding is not None
        assert isinstance(embedding, list)
        assert len(embedding) > 0
        assert all(isinstance(vec, float) for vec in embedding)

    def test_get_embedding_no_api_key(self, tmp_path: Path):
        """Test embedding without API key should raise error"""
        import os

        os.environ["AGENTLY_OPENAI_API_KEY"] = ""
        service = ModelService()

        with pytest.raises(ValueError):
            service.get_embedding("test")
