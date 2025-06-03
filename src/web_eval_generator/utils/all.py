from .tavily_utils import Tavily
# from .search_provider_template import SearchProviderTemplate


class Utils:
    def __init__(self):
        self.search_providers = {
            "tavily": Tavily().search
             # self.search_provider_2 = SearchProviderTemplate().search
        }
       