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
        example="100",
    )
    qa_subject: Optional[str] = Field(
        default="general",
        description="QA Subject Name",
        example="Sports, Stocks, News....",)

    save_to_langsmith: Optional[bool] = Field(
        default=True,
        description="Flag to indicate whether to save the generated data to LangSmith.",
        example=True,
    )

class OutputState(BaseModel):
    output_message: Optional[str] = Field(
        None,
        description="The output message indicating where the dataset was saved."
    )



class QAState(BaseModel):
    page_content: str

class GeneratorState(InputState, OutputState):
    search_queries: List[str] = Field(
        default_factory=lambda: [
            "Technology news of today",
            "Sports news of today",
            "Stock market updates of today",
            "World politics news of today",
            "Entertainment news of today",
            "Weather forecast of today",
            "Health and wellness news of today",
            "Science discoveries of today",
            "Business trends of today",
            "Education news of today"
        ],
        description="A default list of search queries covering a variety of topics."
    )
    search_results: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    q_and_as: Annotated[list, operator.add] = Field(default_factory=list)





