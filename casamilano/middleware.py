from .logging_context import (
    set_current_request_context,
    clear_current_request_context,
)


class RequestLoggingContextMiddleware:
    """
    Middleware che salva i dati della request corrente
    in un contesto temporaneo leggibile dal logging filter.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        set_current_request_context(request)

        try:
            response = self.get_response(request)
            return response
        finally:
            clear_current_request_context()