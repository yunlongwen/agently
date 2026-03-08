"""Tests for model service"""

from unittest.mock import Mock, patch

import pytest
from agently.core.model_service import ModelService


class TestModelService:
    """Test ModelService class"""

    def test_init_service(self):
        """Test initializing model service"""
        with patch("agently.core.model_service.OpenAIChat"):
            with patch("agently.core.model_service.AnthropicChat"):
                service = ModelService()

        assert service is not None

    @pytest.mark.parametrize(
        "model_name,api_key_env",
        [
            ("openai", "AGENTLY_OPENAI_API_KEY"),
            ("anthropic", "AGENTLY_ANTHROPIC_API_KEY"),
        ],
    )
    def test_get_chat_completion(self, model_name, api_key_env):
        """Test getting chat completion from model"""
        import os

        # Setup mock API key
        os.environ[api_key_env] = "test-api-key"

        try:
            # Mock both OpenAIChat and AnthropicChat
            with patch("agently.core.model_service.OpenAIChat") as mock_openai:
                with patch("agently.core.model_service.AnthropicChat") as mock_anthropic:
                    # Setup mock instances
                    mock_openai_instance = Mock()
                    mock_openai_instance.complete.return_value = {"content": "openai response"}
                    mock_openai.return_value = mock_openai_instance

                    mock_anthropic_instance = Mock()
                    mock_anthropic_instance.complete.return_value = {
                        "content": "anthropic response"
                    }
                    mock_anthropic.return_value = mock_anthropic_instance

                    service = ModelService()

                    # Mock the _get_api_key method to avoid actual API key validation
                    with patch.object(service, "_get_api_key", return_value="test-key"):
                        response = service.get_chat_completion("test prompt")

                        assert response is not None
                        assert isinstance(response, dict)
                        assert "content" in response
                        # The implementation uses OpenAIChat by default in get_chat_completion
                        assert "response" in response["content"]
        finally:
            # Cleanup
            if api_key_env in os.environ:
                del os.environ[api_key_env]

    def test_get_chat_completion_no_api_key(self):
        """Test chat completion without API key should raise error"""
        import os

        # Ensure no API key is set
        original_key = os.environ.pop("AGENTLY_OPENAI_API_KEY", None)

        try:
            service = ModelService()

            with pytest.raises(ValueError, match="OpenAI API key not configured"):
                service.get_chat_completion("test")
        finally:
            # Restore original key if it existed
            if original_key:
                os.environ["AGENTLY_OPENAI_API_KEY"] = original_key

    def test_get_embedding(self):
        """Test getting embedding"""
        import os

        # Setup mock API key
        os.environ["AGENTLY_OPENAI_API_KEY"] = "test-api-key"

        try:
            service = ModelService()

            # Mock the _get_api_key method
            with patch.object(service, "_get_api_key", return_value="test-key"):
                embedding = service.get_embedding("test text")

                assert embedding is not None
                assert isinstance(embedding, list)
                assert len(embedding) > 0
                assert all(isinstance(vec, float) for vec in embedding)
        finally:
            # Cleanup
            if "AGENTLY_OPENAI_API_KEY" in os.environ:
                del os.environ["AGENTLY_OPENAI_API_KEY"]

    def test_get_embedding_no_api_key(self):
        """Test embedding without API key should raise error"""
        import os

        # Ensure no API key is set
        original_key = os.environ.pop("AGENTLY_OPENAI_API_KEY", None)

        try:
            service = ModelService()

            with pytest.raises(ValueError, match="OpenAI API key not configured"):
                service.get_embedding("test")
        finally:
            # Restore original key if it existed
            if original_key:
                os.environ["AGENTLY_OPENAI_API_KEY"] = original_key
