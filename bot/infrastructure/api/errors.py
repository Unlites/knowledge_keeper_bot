class KnowledgeKeeperAPIError(Exception):
    def __init__(self, detail):
        self.detail = detail
    
    def __str__(self):
        return self.detail


class KnowledgeKeeperAPIUnauthorized(Exception):
    pass


class KnowledgeKeeperAPIConnectionError(KnowledgeKeeperAPIError):
    def __init__(self, detail):
        self.message = "can't connect to Knowledge Keeper API"
        self.detail = detail
    
    def __str__(self):
        return self.message


