from langgraph.graph import StateGraph, START
from web_eval_generator.state import *
from web_eval_generator.nodes import QA_Search_Queries , TavilySearchAgent , QAGenerator , LangSmithDatasetSaver , LocalDatasetSaver
from web_eval_generator.router import map_qa,save_router,start_router
from web_eval_generator.config import Config
from web_eval_generator.utils.all import Utils

utils = Utils()
cfg = Config()
# Initialize agents
qa_search_queries = QA_Search_Queries(cfg,utils)
search = TavilySearchAgent(cfg,utils)
generate_qa = QAGenerator(cfg,utils)
langsmith_save = LangSmithDatasetSaver()
local_save = LocalDatasetSaver()

# Define a Langgraph graph
graph = StateGraph(GeneratorState, input=InputState, output=OutputState)

# Add nodes to the graph
graph.add_node("generate_search_queries_on_subject", qa_search_queries.run)
graph.add_node("tavily_search", search.run)
graph.add_node("generate_qa", generate_qa.run)
graph.add_node("save_dataset_to_langsmith", langsmith_save.run)
graph.add_node("save_dataset_to_local", local_save.run)

# Add Edges to the graph
graph.add_conditional_edges(START,start_router)
graph.add_edge("generate_search_queries_on_subject", "tavily_search")
graph.add_conditional_edges("tavily_search", map_qa, ["generate_qa"])
graph.add_conditional_edges('generate_qa', save_router)

graph = graph.compile()
graph.name = "Tavily RAG Web Search Dataset Generator"
