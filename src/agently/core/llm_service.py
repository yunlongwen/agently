"""LLM Service - LangChain integration for AI model interaction"""

from dataclasses import dataclass, field
from typing import Any, Dict, Iterator, List, Optional

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from agently.config import get_settings
from agently.logging import get_logger

logger = get_logger(__name__)


@dataclass
class LLMConfig:
    """Configuration for LLM service"""
    provider: str = "openai"
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 4096
    top_p: float = 1.0
    api_key: Optional[str] = None
    base_url: Optional[str] = None


@dataclass
class ChatMessage:
    """Chat message"""
    role: str
    content: str
    name: Optional[str] = None

    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary format"""
        d = {"role": self.role, "content": self.content}
        if self.name:
            d["name"] = self.name
        return d

    def to_langchain_message(self):
        """Convert to LangChain message"""
        if self.role == "user":
            return HumanMessage(content=self.content)
        elif self.role == "assistant":
            return AIMessage(content=self.content)
        elif self.role == "system":
            return SystemMessage(content=self.content)
        else:
            return HumanMessage(content=self.content)


class LLMService:
    """
    LLM Service - 大语言模型服务

    基于LangChain实现的LLM服务，支持OpenAI和Anthropic。
    """

    def __init__(self, config: Optional[LLMConfig] = None):
        """
        Initialize LLM service

        Args:
            config: LLM configuration
        """
        self.config = config or LLMConfig()
        self.settings = get_settings()
        self._chat_model = None
        self._embeddings = None
        self._initialize_models()

    def _initialize_models(self) -> None:
        """Initialize chat models based on provider"""
        if self.config.provider == "openai":
            api_key = self.config.api_key or self.settings.openai_api_key
            self._chat_model = ChatOpenAI(
                model=self.config.model,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                api_key=api_key,
                base_url=self.config.base_url,
            )
            self._embeddings = OpenAIEmbeddings(api_key=api_key)

        elif self.config.provider == "anthropic":
            try:
                from langchain_anthropic import ChatAnthropic
                api_key = self.config.api_key or self.settings.anthropic_api_key
                self._chat_model = ChatAnthropic(
                    model=self.config.model,
                    temperature=self.config.temperature,
                    max_tokens=self.config.max_tokens,
                    api_key=api_key,
                )
            except ImportError:
                logger.warning("langchain-anthropic not installed, falling back to OpenAI")
                self.config.provider = "openai"
                self._initialize_models()

        else:
            raise ValueError(f"Unsupported provider: {self.config.provider}")

    @property
    def chat_model(self):
        """Get chat model"""
        return self._chat_model

    @property
    def embeddings(self):
        """Get embeddings model"""
        return self._embeddings

    def chat(
        self,
        message: str,
        history: Optional[List[ChatMessage]] = None,
        system_prompt: Optional[str] = None,
    ) -> str:
        """
        Send a chat message and get response

        Args:
            message: User message
            history: Conversation history
            system_prompt: System prompt

        Returns:
            Model response
        """
        messages = []

        # Add system prompt
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))

        # Add history
        if history:
            for msg in history:
                messages.append(msg.to_langchain_message())

        # Add current message
        messages.append(HumanMessage(content=message))

        # Get response
        response = self._chat_model.invoke(messages)

        logger.info(
            "Chat completed",
            provider=self.config.provider,
            model=self.config.model,
            message_length=len(message),
        )

        return response.content

    def stream_chat(
        self,
        message: str,
        history: Optional[List[ChatMessage]] = None,
        system_prompt: Optional[str] = None,
    ) -> Iterator[str]:
        """
        Stream chat response

        Args:
            message: User message
            history: Conversation history
            system_prompt: System prompt

        Yields:
            Response chunks
        """
        messages = []

        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))

        if history:
            for msg in history:
                messages.append(msg.to_langchain_message())

        messages.append(HumanMessage(content=message))

        for chunk in self._chat_model.stream(messages):
            if chunk.content:
                yield chunk.content

    def get_embedding(self, text: str) -> List[float]:
        """
        Get embedding for text

        Args:
            text: Text to embed

        Returns:
            Embedding vector
        """
        if not self._embeddings:
            raise ValueError("Embeddings not initialized for this provider")

        return self._embeddings.embed_query(text)

    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Get embeddings for multiple texts

        Args:
            texts: List of texts

        Returns:
            List of embedding vectors
        """
        if not self._embeddings:
            raise ValueError("Embeddings not initialized for this provider")

        return self._embeddings.embed_documents(texts)

    def get_token_count(self, text: str) -> int:
        """
        Count tokens in text

        Args:
            text: Text to count

        Returns:
            Token count
        """
        try:
            from tiktoken import encoding_for_model
            encoding = encoding_for_model(self.config.model)
            return len(encoding.encode(text))
        except Exception:
            # Fallback estimation
            return len(text.split()) * 2

    def with_structured_output(self, schema: Any):
        """
        Get model with structured output

        Args:
            schema: Output schema (Pydantic model or JSON schema)

        Returns:
            Model with structured output
        """
        return self._chat_model.with_structured_output(schema)

    def bind_tools(self, tools: List[Any]) -> Any:
        """
        Bind tools to the model

        Args:
            tools: List of tools to bind

        Returns:
            Model with bound tools
        """
        return self._chat_model.bind_tools(tools)
