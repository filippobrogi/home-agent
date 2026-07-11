system_prompt_simple = """

You are an home assistant supposed to help the user with their daily tasks.

Use tools whenever you need external information.

ONLY respond with JSON. No explanations or text. Always use the tools when relevant.

"""


def get_system_prompt(simple_prompt: bool = False) -> str:
    if simple_prompt:
        return system_prompt_simple
    else:
        return system_prompt_simple