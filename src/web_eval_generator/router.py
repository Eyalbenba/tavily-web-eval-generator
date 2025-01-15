from typing import Literal
from langgraph.types import Send
def save_router(state) -> Literal["save_dataset_to_langsmith", "save_dataset_to_local"]:
    """Routes the workflow after the 'generate_qa' step.

     Decides whether to save to langsmith or not."""
    try:
        if state.save_to_langsmith:
            return "save_dataset_to_langsmith"
        else:
            return "save_dataset_to_local"
    except Exception as e:
        return "save_dataset_to_local"

def start_router(state) -> Literal["generate_search_queries_on_subject", "tavily_search"]:
    """Routes the workflow after the 'Start' step.

     If no subject is Inputted, it falls back to general questions for reevaluation."""
    try:
        if state.qa_subject != 'general':
            return "generate_search_queries_on_subject"
        else:
            return "tavily_search"
    except Exception as e:
        return "tavily_search"

def map_qa(state):
    # Map Function
    return [Send("generate_qa", {"page_content": result.get('content', '')}) for url,result in state.search_results.items()]