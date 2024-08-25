from utils import initialize_gemini
from tools import calculate, get_planet_mass
from prompts import sysmtem_prompt
from agent import ReActAgent

from termcolor import colored

import argparse

def main():
    model = initialize_gemini(api_config_path="config/api1.yaml") 
    tools = [calculate.__name__, get_planet_mass.__name__]
    omar = ReActAgent(model, tools, sysmtem_prompt)

    while True:
        query = colored(input("Enter your query (or 'exit' to quit): "),"cyan")
        if  "exit" in query.lower():
            print(colored("Exiting...",'red'))
            break
        else:
        # Pass the query to the agent for processing and response
            response = omar.loop(query)
            print(colored(response,'red'))
if __name__ == '__main__':
    main()