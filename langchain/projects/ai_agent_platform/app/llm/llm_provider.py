from langchain_openai import ChatOpenAI
from langchain_core.language_models import BaseChatModel
from app.configs.settings import LLM_PROVIDER
from dotenv import load_dotenv
from langchain_community.llms import Ollama

load_dotenv()

class DummyLLM(BaseChatModel):
    """Dummy fallback LLM when no real provider is selected."""

    def _generate(self, messages, stop=None, **kwargs):
        from langchain_core.outputs import ChatResult, ChatGeneration
        from langchain_core.messages import AIMessage

        input_text = "\n".join([m.content for m in messages])
        output_text = f"(DummyLLM) {input_text}"

        return ChatResult(generations=[ChatGeneration(message=AIMessage(content=output_text))])

    @property
    def _llm_type(self) -> str:
        return "dummy_llm"

    @property
    def lc_serializable(self) -> bool:
        return False

def get_llm():
    """
    Returns the LLM instance based on configuration.
    Supported providers:
    - openai
    - ollama
    - dummy
    """

    provider = LLM_PROVIDER.lower()

    if provider == "openai":
        return ChatOpenAI(
            model="gpt-4-turbo",
            temperature=0.0,
        )

    elif provider == "ollama":
        # Default model: llama3 (You can change to codellama, phi3 etc)
        return Ollama(
            model="llama3"
        )

    elif provider == "dummy":
        return DummyLLM()
    else:
        raise ValueError(f"Unsupported LLM Provider: {LLM_PROVIDER}")