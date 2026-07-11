

from attr import dataclass

from system_prompt import get_system_prompt
from pydantic_ai import Agent, RunContext
from pydantic_ai.providers.ollama import OllamaProvider
from pydantic_ai.models.ollama import OllamaModel
from datetime import datetime


@dataclass
class AppContext:
    user_id: str

def create_dependencies(user_id: str) -> AppContext:
    """
    Function to create dependencies for the agent. This can be used to pass user-specific information to the agent.
    """
    return AppContext(user_id=user_id)

def register_tools(agent: Agent):
    
    @agent.tool
    def get_current_time(ctx: RunContext[AppContext]) -> str:
        """
        Returns the current server time.
        Use this when the user asks what time it is.
        """
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def load_home_agent() -> Agent:
    """
    Function to load the home agent. If no_gpu is True, it loads the agent with the local model and dependencies.

    This function can be used to load the agent in different environments (local or cloud) without changing the code.
    """
       
    model_settings = { "max_new_tokens": 2048, "do_sample": False, "think": True }
    model_name = "home-model"
    home_model = OllamaModel(model_name, provider=OllamaProvider(base_url='http://localhost:11434/v1'), settings=model_settings)
    system_prompt = get_system_prompt(simple_prompt=True)
    
    home_agent = Agent(home_model, system_prompt=system_prompt)
    register_tools(home_agent)
    return home_agent