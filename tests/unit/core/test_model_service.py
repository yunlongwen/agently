"""Tests for model service"""

import os
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from agently.core.model_service import ModelService


class TestModelService:
    """Test ModelService class"""

    def test_init_service(self):
        """Test initializing model service"""
        service = ModelService()
        assert service is not None

    def test_get_chat_completion(self):
        """Test getting chat completion from model"""
        service = ModelService()
        response = service.get_chat_completion("test prompt")
        assert response is not None
        assert isinstance(response, str)

    def test_get_chat_completion_by_provider_openai(self):
        """Test chat completion with OpenAI provider"""
        with patch.dict(os.environ, {"AGENTLY_OPENAI_API_KEY": "test-key"}):
            service = ModelService()
            response = service.get_chat_completion_by_provider("test prompt", "openai")
            assert response is not None

    def test_get_chat_completion_by_provider_anthropic(self):
        """Test chat completion with Anthropic provider"""
        with patch.dict(os.environ, {"AGENTLY_ANTHROPIC_API_KEY": "test-key"}):
            service = ModelService()
            response = service.get_chat_completion_by_provider("test prompt", "anthropic")
            assert response is not None

    def test_get_chat_completion_no_api_key(self):
        """Test chat completion without API key should raise error"""
        service = ModelService()
        with patch.dict(os.environ, {"AGENTLY_OPENAI_API_KEY": ""}, clear=False):
            with pytest.raises(ValueError):
                service.get_chat_completion_by_provider("test", "openai")

    def test_get_embedding(self):
        """Test getting embedding"""
        service = ModelService()
        embedding = service.get_embedding("test text")
        assert embedding is not None
        assert isinstance(embedding, list)

    def test_unsupported_provider(self):
        """Test unsupported provider raises error"""
        service = ModelService()
        with pytest.raises(ValueError):
            service.get_chat_completion_by_provider("test", "unsupported")
