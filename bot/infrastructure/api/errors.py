class KnowledgeKeeperAPIError(Exception):
    def __init__(self, detail):
        self.default_message = None
        self.detail = detail
    
    def __str__(self):
        return self.default_message or self.detail


class KnowledgeKeeperAPIUnauthorized(Exception):
    pass


class KnowledgeKeeperAPIConnectionError(KnowledgeKeeperAPIError):
    def __init__(self, detail):
        self.default_message = "can't connect to Knowledge Keeper API"
        self.detail = detail


