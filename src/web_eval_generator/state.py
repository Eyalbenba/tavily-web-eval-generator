from pydantic import BaseModel, Field ,model_validator
from typing import Dict, List, Any, Optional, Union , Annotated
from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages
import operator




##### Main Input , Output and Generator States ####
class InputState(BaseModel):
    num_qa: Optional[int] = Field(
        default=100,
        description="Number of Question Answer Items to Generate",
        examples=[100]
    )
    qa_subjects: Optional[List[str]] = Field(
        default=["general"],
        description="QA Subjects",
        examples=[["Sports", "Stocks", "News"]])

    save_to_langsmith: Optional[bool] = Field(
        default=False,
        description="Flag to indicate whether to save the generated data to LangSmith.",
        examples=[True]
    )

class OutputState(BaseModel):
    output_message: Optional[str] = Field(
        None,
        description="The output message indicating where the dataset was saved."
    )



class QAState(BaseModel):
    page_content: str
    citations: list[str]
    subject: str

class GeneratorState(InputState, OutputState):
    search_queries: Dict[str, List[str]] = Field(
        default_factory=lambda: {
            "Technology": ["Technology news of today"],
            "Sports": ["Sports news of today"],
            "Stock Market": ["Stock market updates of today"],
            "World Politics": ["World politics news of today"],
            "Entertainment": ["Entertainment news of today"],
            "Weather": ["Weather forecast of today"],
            "Health": ["Health and wellness news of today"],
            "Science": ["Science discoveries of today"],
            "Business": ["Business trends of today"],
            "Education": ["Education news of today"]
        },
        description="A default dictionary of topic to list of search queries covering a variety of subjects."
    )
    # search_results: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    search_results: Any = Field(default_factory=list)
    q_and_a: Annotated[list, operator.add] = Field(default_factory=list)
    dataset: list = Field(default_factory=list)