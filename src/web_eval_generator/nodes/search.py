
class TavilySearchAgent:
    def __init__(self, cfg,utils):
        self.cfg = cfg
        self.utils = utils

    async def run(self, state):
        search_queries = state.search_queries
        msg = "🔎 Tavily Searching ...\n" + "\n".join(f'"{query}"' for query in search_queries)
        if self.cfg.DEBUG:
            print(msg)
        search_results = await self.utils.tavily.search(search_queries, state.search_results)
        return {"messages": msg, "search_results": search_results}