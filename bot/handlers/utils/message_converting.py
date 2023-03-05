def validation_errors(errors: list[dict]) -> str:
    converted_errors_string = ""
    for error in errors:
        for i in range(len(error["loc"])):
            converted_errors_string += f"\n{error['loc'][i]} - {error['msg']}"
    return converted_errors_string
