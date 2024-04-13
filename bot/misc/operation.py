from ..enums import Operation


def get_operation_snippet(data: dict, operation: str) -> int:
    """
    Get the operation snippet.

    :param data: The data.
    :param operation: The operation.
    :return: The bet.
    """
    if operation == Operation.ADD:
        data["bet"] = min(5000, data["bet"] + 10)
    elif operation == Operation.SUB:
        data["bet"] = max(10, data["bet"] - 10)
    elif operation == Operation.MIN:
        data["bet"] = 10
    elif operation == Operation.MAX:
        data["bet"] = 5000
    else:
        data["bet"] *= 2
        data["bet"] = min(5000, data["bet"])

    return data["bet"]
