import requests
from django.conf import settings

def verify_turnstile_token(token: str, remote_ip: str | None = None) -> bool:
    if not token:
        return False

    payload = {
        "secret": settings.CLOUDFLARE_TURNSTILE_SECRET_KEY,
        "response": token,
    }

    if remote_ip:
        payload["remoteip"] = remote_ip

    try:
        response = requests.post(
            "https://challenges.cloudflare.com/turnstile/v0/siteverify",
            data=payload,
            timeout=5,
        )
        result = response.json()
        return result.get("success", False)

    except requests.RequestException:
        return False