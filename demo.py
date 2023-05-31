import os
# please use your key
os.environ["SERPAPI_API_KEY"] = ""

from langchain.agents import initialize_agent, Tool
from langchain.llms import AI21
from langchain.llms.base import LLM
from langchain import LLMMathChain, SerpAPIWrapper


from langchain.llms import OpenAIChat
from langchain.agents import tool
from langchain.chains.conversation.memory import ConversationBufferMemory
from typing import Optional, List, Mapping, Any
import requests
from langchain.llms.utils import enforce_stop_tokens

class VicunaLLM(LLM):
    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        data = {"query": prompt}
        response = requests.post(
            "http://8.130.118.207:8080/post", # this is the IP of my gpu machine
            json= data
        )
        response.raise_for_status()
        output = response.text.strip()[len(prompt):]
        if stop:
            output = enforce_stop_tokens(output, stop)
        return output

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {

        }
llm = VicunaLLM()
search = SerpAPIWrapper()
llm_math_chain = LLMMathChain(llm=llm, verbose=True)
tools = [
    Tool(
        name = "Search",
        func=search.run,
        description="useful for when you need to answer questions about current events"
    ),
    Tool(
        name="Calculator",
        func=llm_math_chain.run,
        description="useful for when you need to answer questions about math"
    )
]
llm = VicunaLLM()
memory = ConversationBufferMemory(memory_key="chat_history")
agent = initialize_agent(tools, llm, agent= "zero-shot-react-description", verbose=True, memory=memory,max_iterations=4,early_stopping_method="generate")
agent.run("The current age of the President of the United States multiplied by 0.5.")
