import asyncio
import time

from dependencies import create_dependencies
from home_agent import load_home_agent


import logging

logging.basicConfig(level=logging.DEBUG)


async def agent_main():
    while True:
        log_file = input("Enter the log file name: ")

        query = ("Analyze this log and find the failure",)
        start = time.perf_counter()
        home_agent = load_home_agent()
        response = await home_agent.run(
            query, deps=create_dependencies(log_file=log_file)
        )
        end = time.perf_counter()
        print(f"Time taken: {end - start}, response: {response.output}")


if __name__ == "__main__":
    try:
        asyncio.run(agent_main())
    except KeyboardInterrupt:
        print("Exiting...")
        exit(0)
