from langchain.agents import initialize_agent, AgentType
# from langchain.chat_models import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI
# from langchain.callbacks.base import CallbackManager
from langchain.agents.agent import AgentExecutor
from langchain.agents.agent import AgentOutputParser
from langchain.schema import AgentAction, AgentFinish

class ThoughtCaptureParser(AgentOutputParser):
    def parse(self, text):
        # Naive parse logic for demo purposes
        return AgentFinish(return_values={"output": text.strip()}, log=text)

def initialize_chat_agent(tools):
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        return_intermediate_steps=True,
        max_iterations=15
    )
    return agent
