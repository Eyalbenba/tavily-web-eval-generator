from langchain_core.messages import SystemMessage, HumanMessage
from web_eval_generator.prompts import *
from web_eval_generator.state import *
from pydantic import BaseModel, Field
import time


class SubjectOrientedSearchQueries(BaseModel):
    search_queries: List[str] = Field(
        ...,
        description="A list of search queries designed to cover different aspects of the subject with context-specific relevance."
    )

class QASearchQueries:
    """Agent responsible for generating subqueries about a person for research purposes"""

    def __init__(self, cfg,utils):
        self.cfg = cfg
        self.utils = utils
        self.model = cfg.LLM
        self.default_system_prompt = QA_QUERIES_SYSTEM_PROMPT
        self.default_user_prompt = QA_QUERIES_USER_PROMPT

    async def run(self,state):
        all_search_queries = {}
        msgs = ""
        # Dividing by 3 because each provider yields multiple sources,
        # and Q and A pairs will be generated for each individual source.
        num_queries_per_subject = max(len(self.utils.search_providers), (state.num_qa // len(state.qa_subjects) // 3)+1)

        for subject in state.qa_subjects:
            msg = f"🗞️ Beginning QA Search Query generation based on subject '{subject}' process...\n"
            msgs += f"{msg}"
            if self.cfg.DEBUG:
                print(msg)

            system_prompt = self.default_system_prompt.format(num_queries=num_queries_per_subject, today=time.strftime("%B %d, %Y"), year=time.strftime("%Y"))
            user_prompt = self.default_user_prompt.format(subject=subject)
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]

            try:
                # Invoke the model with the structured output
                response = await self.model.with_structured_output(SubjectOrientedSearchQueries).ainvoke(messages)
                search_queries = response.search_queries[:num_queries_per_subject]
                all_search_queries[subject]=search_queries

                msg =  f"🤔 Generated {len(search_queries)} Search Queries for subject '{subject}':\n{search_queries}\n"
                msgs += f"{msg}"
                if self.cfg.DEBUG:
                    print(msg)
            except Exception as e:
                # Handle and log errors
                msg = f"Error in QA Generator for subject '{subject}': {e}\n"
                msgs += f"{msg}"
                if self.cfg.DEBUG:
                    print(msgs)

        if not all_search_queries:
            raise ValueError(f"Failed to generate QA pairs")
        return {"search_queries": all_search_queries, "messages": msgs}
