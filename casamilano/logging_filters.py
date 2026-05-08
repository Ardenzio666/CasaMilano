from .logging_context import get_current_request_context


class RequestContextFilter:
    """
    Aggiunge ai record di logging le informazioni della request corrente.
    """

    def filter(self, record):
        context = get_current_request_context()

        user_id = context["user_id"]
        username = context["username"]

        if user_id:
            record.user = f"{user_id}:{username}"
        else:
            record.user = "anonymous"

        record.method = context["method"]
        record.path = context["path"]
        record.request_id = context["request_id"]

        return True