import threading
import uuid

_local = threading.local()


def set_current_request_context(request):
    """
    Salva nel thread corrente alcune informazioni della request.
    Queste informazioni saranno poi lette dal logging filter.
    """
    user = getattr(request, "user", None)

    if user is not None and user.is_authenticated:
        user_id = user.id
        username = user.username
    else:
        user_id = None
        username = "anonymous"

    _local.user_id = user_id
    _local.username = username
    _local.method = request.method
    _local.path = request.get_full_path()
    _local.request_id = str(uuid.uuid4())


def clear_current_request_context():
    """
    Pulisce il contesto alla fine della request.
    Evita che dati di una request restino disponibili nella successiva.
    """
    _local.user_id = None
    _local.username = "anonymous"
    _local.method = "-"
    _local.path = "-"
    _local.request_id = "-"


def get_current_request_context():
    """
    Restituisce i dati salvati per la request corrente.
    """
    return {
        "user_id": getattr(_local, "user_id", None),
        "username": getattr(_local, "username", "anonymous"),
        "method": getattr(_local, "method", "-"),
        "path": getattr(_local, "path", "-"),
        "request_id": getattr(_local, "request_id", "-"),
    }