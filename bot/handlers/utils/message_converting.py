from bot.dto.record import GetRecordDTO


def validation_errors(errors: list[dict]) -> str:
    converted_errors_string = ""
    for error in errors:
        for i in range(len(error["loc"])):
            converted_errors_string += f"\n{error['loc'][i]} - {error['msg']}"
    return converted_errors_string


def displaying_record(record_dto: GetRecordDTO) -> str:
    return (
        f"*Topic*: {record_dto.topic}\n"
        + f"*Title*: {record_dto.title}\n*Content*: {record_dto.content}"
    )
