from models import LogAnalysis
from dependencies import LogDependencies
from tools import head_log_file, read_log_file, search_log_file, tail_log_file
from system_prompt import get_system_prompt
from pydantic_ai import Agent, RunContext
from pydantic_ai.providers.ollama import OllamaProvider
from pydantic_ai.models.ollama import OllamaModel


def register_tools(agent: Agent):
    @agent.tool
    def get_log(ctx: RunContext[LogDependencies]) -> str:
        """
        REQUIRED FIRST STEP for log analysis.

        Reads the complete log file that is currently being analyzed.
        Always call this tool before explaining failures or errors.
        """
        return read_log_file(ctx.deps.log_file)

    @agent.tool
    def search_log(ctx: RunContext[LogDependencies], search_term: str) -> str:
        """
        Searches for a term in the log file that is currently being analyzed.
        This can be useful for finding specific errors or failures.
        """
        return search_log_file(ctx.deps.log_file, search_term=search_term)

    @agent.tool
    def head_log(ctx: RunContext[LogDependencies], lines: int = 10) -> str:
        """
        Reads the first N lines of the log file that is currently being analyzed.
        This can be useful for quickly checking the start of a log file.
        """
        return head_log_file(ctx.deps.log_file, lines=lines)

    @agent.tool
    def tail_log(ctx: RunContext[LogDependencies], lines: int = 10) -> str:
        """
        Reads the last N lines of the log file that is currently being analyzed.
        This can be useful for quickly checking recent errors or failures.
        """
        return tail_log_file(ctx.deps.log_file, lines=lines)

    @agent.tool
    def count_log_lines(ctx: RunContext[LogDependencies]) -> int:
        """
        Counts the number of lines in the log file that is currently being analyzed.
        This can be useful for understanding the size of a log file.
        """
        return count_log_lines(ctx.deps.log_file)


def load_home_agent() -> Agent:
    """Loads the home agent with the necessary tools and system prompt."""

    model_settings = {"max_new_tokens": 2048, "do_sample": False, "think": True}
    model_name = "home-model"
    home_model = OllamaModel(
        model_name,
        provider=OllamaProvider(base_url="http://localhost:11434/v1"),
        settings=model_settings,
    )
    system_prompt = get_system_prompt(log_prompt=True)

    home_agent = Agent(home_model, system_prompt=system_prompt, output_type=LogAnalysis)
    register_tools(home_agent)
    return home_agent
