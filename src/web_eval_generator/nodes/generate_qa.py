from web_eval_generator.prompts import QA_GENERATION_SYSTEM_PROMPT,QA_GENERATION_USER_PROMPT
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel,Field
from typing import List, Dict
from web_eval_generator.state import QAState
import time

class QA(BaseModel):
    question: str = Field(
        ...,
        description="A question generated from the content."
    )
    answer: str = Field(
        ...,
        description="The corresponding answer to the question."
    )
    answer_context: str = Field(description="The exact text from the source that contains the answer.")

class QAList(BaseModel):
    qa_list: List[QA] = Field(
        ...,
        description="A list of QA pairs, each containing a question and its corresponding answer."
    )

class QAWithProvider(BaseModel):
    question: str
    answer: str
    answer_context: str
    provider: str
    subject: str
    citations: list[str]

class QAGenerator:
    def __init__(self,cfg,utils):
        self.model = cfg.LLM
        self.cfg = cfg
        self.default_system_prompt = QA_GENERATION_SYSTEM_PROMPT
        self.default_user_prompt = QA_GENERATION_USER_PROMPT
        self.utils = utils

    async def run(self, state: QAState):
        """
        Generate 10 question-and-answer pairs based on the given page content.

        Args:
            state (QAState): The state containing the page content.

        Returns:
            List[Dict[str, str]]: A list of dictionaries containing question-answer pairs.
        """
        msgs = "🤔 Running QA Generator"
        if self.cfg.DEBUG:
            print(msgs)
        page_content = state['page_content']
        provider = state['provider']  # Get provider from state
        citations = state['citations']
        subject = state['subject']

        # Create system and user messages for the model
        system_message = SystemMessage(content=self.default_system_prompt, today=time.strftime("%B %d, %Y"))
        user_message = HumanMessage(
            content=self.default_user_prompt.format(page_content=page_content)
        )
        messages = [system_message, user_message]
        try:
            response = await self.model.with_structured_output(QAList).ainvoke(messages)
            # Convert QA to QAWithProvider
            qa_with_provider = [
                QAWithProvider(
                    question=qa.question,
                    answer=qa.answer,
                    answer_context=qa.answer_context,
                    provider=provider,
                    subject=subject,
                    citations=citations
                ) for qa in response.qa_list if qa.question != "SKIP"
            ]
            return {"q_and_a":qa_with_provider}
        except Exception as e:
            # Handle and log errors
            msgs = f"Error in QA Generator: {e}"
            if self.cfg.DEBUG:
                print(msgs)
