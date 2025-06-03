class SearchProviderTemplate:
    def __init__(self, config):
        self.config = config
        pass

    async def search(self, query):
        # Make sure to call the search provider asynchronously to enable concurrent search and reduce the latency
        # Return a dictionary where each key is source url or sources found and the value is a dictionary with the following keys:
        # - "content": str - the content of the search result with avalibile metadata (e.g f"url:{url}, title:{title}, content:{content}")
        # - "provider": str - the name of the search provider
        # - "citations": list[str] - a list of citations for the search result
        pass