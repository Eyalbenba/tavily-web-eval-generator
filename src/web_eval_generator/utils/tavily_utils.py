from datetime import datetime
from tavily import AsyncTavilyClient

class Tavily:
    def __init__(self):
        self.client = AsyncTavilyClient()

    async def search(self, query):
        """
        Perform searches for each sub-query using the Tavily Search concurrently.

        :param query: search query.
        """
        try:
            sources_dict = {} # Return a dictionary
            tavily_response = await self.client.search(query=query, search_depth="basic", include_raw_content=True,
                                                       max_results=5, auto_parameters=True)
            search_response = tavily_response['results']
            print("Tavily search took {} seconds".format(tavily_response['response_time']))

            # Combine the results from all the responses and update the sources_dict
            for result in search_response:
                url = result.get("url")
                if url:
                    # Add the result to sources_dict if the URL is not already present
                    sources_dict[url] = {
                        "content": f"title:{result.get('title')}, 'content':{result.get('raw_content',result.get('content', ''))}",
                        "provider": "tavily",
                        "citations": [url]
                    }

            return sources_dict
        except Exception as e:
            return {
                "error": f"Error occurred during tavily search for query '{query}': {e}"
            }