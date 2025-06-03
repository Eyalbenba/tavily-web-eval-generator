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

def start_router(state) -> Literal["generate_search_queries_on_subject", "web_search"]:
    """Routes the workflow after the 'Start' step.

     If no subject is Inputted, it falls back to general questions for reevaluation."""
    try:
        if state.qa_subjects != ['general']:
            return "generate_search_queries_on_subject"
        else:
            return "web_search"
    except Exception as e:
        return "web_search"

def map_qa(state):
    # Map Function
    return [
        Send("generate_qa", {
            "page_content": result["content"],
            "provider": result["provider"],
            "citations": result["citations"],
            "subject": result["subject"],
        })
        for result in state.search_results
    ]