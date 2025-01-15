from langchain_core.messages import SystemMessage, HumanMessage
from web_eval_generator.prompts import *
from web_eval_generator.state import *
from pydantic import BaseModel, Field



class SubjectOrientedSearchQueries(BaseModel):
    search_queries: List[str] = Field(
        ...,
        description="A list of search queries designed to cover different aspects of the subject with context-specific relevance."
    )

class QA_Search_Queries:
    """Agent responsible for generating subqueries about a person for research purposes"""

    def __init__(self, cfg,utils):
        self.cfg = cfg
        self.utils = utils
        self.model = cfg.LLM
        self.default_system_prompt = QA_QUERIES_SYSTEM_PROMPT
        self.default_user_prompt = QA_QUERIES_USER_PROMPT

    async def run(self,state):
        msgs = f" 🗞️ Beginning QA Search Query generation based on subject {state.qa_subject} process...\n"
        if self.cfg.DEBUG:
            print(msgs)

        system_prompt = self.default_system_prompt.format(num_queries=state.num_qa/5)
        user_prompt = self.default_user_prompt.format(subject=state.qa_subject)
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]

        try:
            # Invoke the model with the structured output
            response = await self.model.with_structured_output(SubjectOrientedSearchQueries).ainvoke(messages)
            search_queries = response.search_queries

            msgs += f"\n 🤔 Generated Search Queries for subject {state.qa_subject}."
            if self.cfg.DEBUG:
                print(msgs)

            return {"search_queries": search_queries,"messages": msgs}

        except Exception as e:
            # Handle and log errors
            msgs = f"Error in QA Generator: {e}"
            if self.cfg.DEBUG:
                print(msgs)
            raise ValueError(f"Failed to generate QA pairs: {e}")
