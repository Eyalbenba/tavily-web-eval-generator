import asyncio
from datetime import datetime
from tavily import AsyncTavilyClient

class Tavily:
    def __init__(self):
        self.client = AsyncTavilyClient()

    async def search(self, sub_queries: list[str], sources_dict: dict):
        """
        Perform searches for each sub-query using the Tavily Search concurrently.

        :param sub_queries: List of search queries.
        :param sources_dict: Dictionary to store unique search results, keyed by URL.
        """

        # Define a coroutine function to perform a single search with error handling
        async def perform_search(query):
            try:
                # Add date to the query as we need the most recent results
                query_with_date = f"{query} {datetime.now().strftime('%m-%Y')}"
                tavily_response = await self.client.search(query=query_with_date, topic="news",days=3, max_results=8)
                return tavily_response['results']
            except Exception as e:
                # Handle any exceptions, log them, and return an empty list
                print(f"Error occurred during search for query '{query}': {str(e)}")
                return []

        # Run all the search tasks in parallel
        search_tasks = [perform_search(itm) for itm in sub_queries]
        search_responses = await asyncio.gather(*search_tasks)

        # Combine the results from all the responses and update the sources_dict
        for response in search_responses:
            for result in response:
                url = result.get("url")
                if url and url not in sources_dict:
                    # Add the result to sources_dict if the URL is not already present
                    sources_dict[url] = result

        return sources_dict