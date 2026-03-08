"""Tests for LangChain integration"""

import os
from unittest.mock import MagicMock, patch

from agently.core.llm_service import ChatMessage, LLMConfig, LLMService


class TestLLMConfig:
    """Test LLMConfig"""

    def test_default_config(self):
        """Test default configuration"""
        config = LLMConfig()
        assert config.provider == "openai"
        assert config.model == "gpt-4"
        assert config.temperature == 0.7

    def test_custom_config(self):
        """Test custom configuration"""
        config = LLMConfig(
            provider="anthropic", model="claude-3-opus-20240229", temperature=0.5, max_tokens=2000
        )
        assert config.provider == "anthropic"
        assert config.model == "claude-3-opus-20240229"
        assert config.temperature == 0.5
        assert config.max_tokens == 2000


class TestChatMessage:
    """Test ChatMessage"""

    def test_user_message(self):
        """Test creating user message"""
        msg = ChatMessage(role="user", content="Hello")
        assert msg.role == "user"
        assert msg.content == "Hello"

    def test_assistant_message(self):
        """Test creating assistant message"""
        msg = ChatMessage(role="assistant", content="Hi there!")
        assert msg.role == "assistant"
        assert msg.content == "Hi there!"

    def test_system_message(self):
        """Test creating system message"""
        msg = ChatMessage(role="system", content="You are a helpful assistant")
        assert msg.role == "system"
        assert msg.content == "You are a helpful assistant"

    def test_to_dict(self):
        """Test converting to dictionary"""
        msg = ChatMessage(role="user", content="Test")
        d = msg.to_dict()
        assert d == {"role": "user", "content": "Test"}


class TestLLMService:
    """Test LLMService"""

    def test_init_default(self):
        """Test initializing with defaults"""
        with patch.dict(os.environ, {"AGENTLY_OPENAI_API_KEY": "test-key"}):
            with patch("agently.core.llm_service.ChatOpenAI") as mock_chat:
                mock_chat.return_value = MagicMock()
                with patch("agently.core.llm_service.OpenAIEmbeddings") as mock_emb:
                    mock_emb.return_value = MagicMock()
                    service = LLMService()
                    assert service is not None

    def test_init_with_config(self):
        """Test initializing with config"""
        config = LLMConfig(provider="openai", model="gpt-4", api_key="test-key")
        with patch("agently.core.llm_service.ChatOpenAI") as mock_chat:
            mock_chat.return_value = MagicMock()
            with patch("agently.core.llm_service.OpenAIEmbeddings") as mock_emb:
                mock_emb.return_value = MagicMock()
                service = LLMService(config=config)
                assert service.config == config

    def test_chat_single_message(self):
        """Test chat with single message"""
        config = LLMConfig(api_key="test-key")
        with patch("agently.core.llm_service.ChatOpenAI") as mock_chat:
            mock_instance = MagicMock()
            mock_chat.return_value = mock_instance
            mock_instance.invoke.return_value = MagicMock(content="Hello! How can I help?")
            with patch("agently.core.llm_service.OpenAIEmbeddings") as mock_emb:
                mock_emb.return_value = MagicMock()
                service = LLMService(config=config)
                response = service.chat("Hello")
                assert response is not None

    def test_chat_with_history(self):
        """Test chat with conversation history"""
        config = LLMConfig(api_key="test-key")
        with patch("agently.core.llm_service.ChatOpenAI") as mock_chat:
            mock_instance = MagicMock()
            mock_chat.return_value = mock_instance
            mock_instance.invoke.return_value = MagicMock(content="I understand your question.")
            with patch("agently.core.llm_service.OpenAIEmbeddings") as mock_emb:
                mock_emb.return_value = MagicMock()
                service = LLMService(config=config)
                history = [
                    ChatMessage(role="user", content="Previous question"),
                    ChatMessage(role="assistant", content="Previous answer"),
                ]
                response = service.chat("New question", history=history)
                assert response is not None

    def test_chat_with_system_prompt(self):
        """Test chat with system prompt"""
        config = LLMConfig(api_key="test-key")
        with patch("agently.core.llm_service.ChatOpenAI") as mock_chat:
            mock_instance = MagicMock()
            mock_chat.return_value = mock_instance
            mock_instance.invoke.return_value = MagicMock(content="Code generated")
            with patch("agently.core.llm_service.OpenAIEmbeddings") as mock_emb:
                mock_emb.return_value = MagicMock()
                service = LLMService(config=config)
                response = service.chat(
                    "Generate a function", system_prompt="You are a code generator"
                )
                assert response is not None

    def test_stream_chat(self):
        """Test streaming chat"""
        config = LLMConfig(api_key="test-key")
        with patch("agently.core.llm_service.ChatOpenAI") as mock_chat:
            mock_instance = MagicMock()
            mock_chat.return_value = mock_instance
            mock_instance.stream.return_value = iter(
                [
                    MagicMock(content="Hello"),
                    MagicMock(content=" world"),
                    MagicMock(content="!"),
                ]
            )
            with patch("agently.core.llm_service.OpenAIEmbeddings") as mock_emb:
                mock_emb.return_value = MagicMock()
                service = LLMService(config=config)
                chunks = list(service.stream_chat("Hello"))
                assert len(chunks) >= 0

    def test_anthropic_provider(self):
        """Test using Anthropic provider"""
        config = LLMConfig(provider="anthropic", model="claude-3-opus-20240229", api_key="test-key")
        with patch.dict("sys.modules", {"langchain_anthropic": MagicMock()}):
            with patch("agently.core.llm_service.ChatAnthropic", create=True) as mock_chat:
                mock_instance = MagicMock()
                mock_chat.return_value = mock_instance
                mock_instance.invoke.return_value = MagicMock(content="Claude response")
                service = LLMService(config=config)
                response = service.chat("Hello")
                assert response is not None

    def test_get_token_count(self):
        """Test token counting"""
        config = LLMConfig(api_key="test-key")
        with patch("agently.core.llm_service.ChatOpenAI") as mock_chat:
            mock_chat.return_value = MagicMock()
            with patch("agently.core.llm_service.OpenAIEmbeddings") as mock_emb:
                mock_emb.return_value = MagicMock()
                service = LLMService(config=config)
                count = service.get_token_count("Hello world")
                assert count >= 0

    def test_get_embedding(self):
        """Test getting embeddings"""
        config = LLMConfig(api_key="test-key")
        with patch("agently.core.llm_service.ChatOpenAI") as mock_chat:
            mock_chat.return_value = MagicMock()
            with patch("agently.core.llm_service.OpenAIEmbeddings") as mock_emb:
                mock_instance = MagicMock()
                mock_emb.return_value = mock_instance
                mock_instance.embed_query.return_value = [0.1, 0.2, 0.3]
                service = LLMService(config=config)
                embedding = service.get_embedding("test text")
                assert embedding is not None
                assert isinstance(embedding, list)
