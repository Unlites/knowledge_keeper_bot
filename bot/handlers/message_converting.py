from bot.dto.record import ResponseRecordDTO


def validation_errors(errors: list[dict]) -> str:
    converted_errors_string = ""
    for error in errors:
        for i in range(len(error["loc"])):
            converted_errors_string += f"\n{error['loc'][i]} - {error['msg']}"
    return converted_errors_string


def displaying_record(record_dto: ResponseRecordDTO) -> str:
    return (
        f"<b>Topic</b>: {record_dto.topic}\n"
        + f"<b>Title</b>: {record_dto.title}\n<b>Content</b>: {record_dto.content}"
    )
