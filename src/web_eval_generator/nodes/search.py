import random
import asyncio

class MultiProviderSearchAgent:
    def __init__(self, cfg, utils):
        self.cfg = cfg
        self.utils = utils
        self.providers = self.utils.search_providers
        # self.providers = {
        #     "tavily": self.utils.tavily.search,
        #     # Add additonal serarch providers here
        #     # "search_provider_2": self.utils.search_provider_2.search,
        #     # "search_provider_3": self.utils.search_provider_3.search,
        # }

    async def run(self, state):
        msg = "🔎 Running Multi-Provider Search...\n"
        if self.cfg.DEBUG:
            print(msg)

        search_tasks = []
        query_metadata = []

        for subject, search_queries in state.search_queries.items():
            # Distribute queries among providers
            providers = list(self.providers.keys())
            num_providers = len(providers)

            # First, ensure at least one query per provider and per subject
            for i, provider in enumerate(providers):
                if i < len(search_queries):
                    search_tasks.append(self.providers[provider](search_queries[i]))
                    query_metadata.append({"query": search_queries[i], "provider": provider, "subject": subject})

            # Then randomly distribute any remaining queries
            for query in search_queries[num_providers:]:
                provider_name = random.choice(providers)
                search_tasks.append(self.providers[provider_name](query))
                query_metadata.append({"query": query, "provider": provider_name, "subject": subject})

        # Run all searches in parallel with exception handling
        search_results = []

        # Calculate total number of batches (round up)
        batch_size = 10
        total_batches = (len(search_tasks) + batch_size - 1) // batch_size
        batch_num = 1

        i = 0
        while i < len(search_tasks):
            if self.cfg.DEBUG:
                print(f"Processing web searches batch {batch_num}/{total_batches}...")  # Log batch number out of total
            batch_tasks = search_tasks[i:i + batch_size]
            batch_metadata = query_metadata[i:i + batch_size]
            try:
                results = await asyncio.gather(*batch_tasks, return_exceptions=True)
                for j, result in enumerate(results):
                    meta = batch_metadata[j]
                    if isinstance(result, Exception):
                        if self.cfg.DEBUG:
                            print(
                                f"Search failed for query '{meta['query']}' (subject:'{meta['subject']}' with provider '{meta['provider']}': {str(result)}")
                        search_results.append(None)
                    else:
                        search_results.append(result)
            except Exception as e:
                if self.cfg.DEBUG:
                    print(f"Unexpected error during parallel search execution: {str(e)}")
            i += batch_size
            batch_num += 1
            print()

        # Format results with provider information
        formatted_results = []
        for i, result in enumerate(search_results):
            if not result or not isinstance(result, dict):  # Ensure result is a non-empty dict
                continue

            if "error" in result:
                if self.cfg.DEBUG:
                    print(result.get("error"))
                continue

            provider = query_metadata[i]["provider"]
            subject = query_metadata[i]["subject"]

            for url, item in result.items():
                try:
                    formatted_results.append({
                        "citations": item.get("citations", []),
                        "content": item.get("content", ""),
                        "provider": provider,
                        "subject": subject,
                        "query": query_metadata[i]["query"]
                    })
                except Exception as e:
                    if self.cfg.DEBUG:
                        print(f"Error in formatting {provider} result: {e}")
                    continue

        return {"messages": msg, "search_results": formatted_results}


