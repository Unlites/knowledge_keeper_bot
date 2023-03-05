from config.config import Config


class Pagination:
    def __init__(self, current_page) -> None:
        self.current_page = current_page
        self.next_page = current_page + 1
        self.prev_page = current_page - 1
        self.limit = current_page * Config.DISPLAY_LIMIT
        self.offset = self.limit - Config.DISPLAY_LIMIT
        self.limit_for_check_next_page = self.limit + 1
