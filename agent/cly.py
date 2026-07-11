import asyncio
import time

from home_agent import create_dependencies, load_home_agent



async def main():
    while True:
        query = input("How can I help you: ")
        start = time.perf_counter()
        home_agent = load_home_agent()
        response = await home_agent.run(query, deps=create_dependencies(user_id="filippo"))
        end = time.perf_counter()
        print(f"Time taken: {end - start}, response: {response.output}")

if __name__ == "__main__":
    asyncio.run(main())

