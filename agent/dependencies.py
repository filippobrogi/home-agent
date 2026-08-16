from dataclasses import dataclass


@dataclass
class AppContext:
    user_id: str


@dataclass
class LogDependencies:
    log_file: str


def create_dependencies(log_file: str) -> LogDependencies:
    """
    Function to create dependencies for the agent. This can be used to pass user-specific information to the agent.
    """
    return LogDependencies(log_file=log_file)
