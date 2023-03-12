from enum import Enum


class CallbackOperation(Enum):
    GET_RECORD_BY_ID = 1
    SEARCH_RECORDS_BY_TITLE_SWITCH_PAGE = 2
    GET_ALL_RECORDS_SWITCH_PAGE = 3
    GET_RECORDS_BY_TOPIC = 4
