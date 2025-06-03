from .tavily_utils import Tavily
# from .search_provider_template import SearchProviderTemplate


class Utils:
    def __init__(self, config):
        self.search_providers = {
            "tavily": Tavily(config).search
             # self.search_provider_2 = SearchProviderTemplate().search
        }
       