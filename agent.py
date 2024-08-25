from langchain_core.prompts import ChatPromptTemplate
from tools import calculate,get_planet_mass
import re
class ReActAgent:
    def __init__(self, model, tools, system:str=""):
        self.model = model
        self.tools = tools
        self.system = system
        self.messages:list = []
        if self.system:
            self.messages.append(("system",system))


    def _execute(self, message:str="", verbose=True):
        if message:
            self.messages.append(("user",message))
        result = self.model.invoke(ChatPromptTemplate(self.messages).invoke({}))
        if verbose:
            print(message)
            print(result.content)
        self.messages.append(("ai",result.content))
        return result.content

    
    def loop(self, Query, verbose=True):
        response = self._execute(Query, verbose=verbose)
        for i in range(15):
            if "PAUSE" in response and "Action" in response:
                tool, tool_input =  re.findall(r"Action: ([a-z0-9_]+): (.+)", response, re.IGNORECASE)[0]
                if tool in self.tools:
                    tool_res = eval(f"{tool}('{tool_input}')")
                    response = f"Observation: {tool_res}"
                else:
                    response = f"Observation: Tool not found in accessed tools"
            elif "answer" in response.lower():
                response = "Answer: "+ re.findall(r"Answer: (.+)", response, re.IGNORECASE)[0]
                return response

            response = self._execute(response,verbose=verbose)
        return response
    
    
    def __call__(self, Query, verbose=True):
        self.loop(Query, verbose=verbose)