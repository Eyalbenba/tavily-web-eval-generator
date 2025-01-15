from langchain_openai import ChatOpenAI


class Config:
    def __init__(self):
        """
        Initializes the configuration for the agents
        """
        self.LLM = ChatOpenAI(model="gpt-4o", temperature=0.2)
        self.save_to_langsmith = False
        self.DEBUG = False
