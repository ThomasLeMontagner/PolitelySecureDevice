"""Email credentials used by the alerting client via ALERT_SENDER_EMAIL, ALERT_EMAIL_PASSWORD, and ALERT_RECEIVER_EMAIL."""

from __future__ import annotations

import os


def get_environment_variable(key: str) -> str:
    """Fetch an environment variable or raise if missing."""
    value = os.getenv(key)
    if not value:
        raise RuntimeError(f"Environment variable {key} must be set for email sending.")
    return value


SENDER_EMAIL = get_environment_variable("ALERT_SENDER_EMAIL")
SENDER_PASSWORD = get_environment_variable("ALERT_EMAIL_PASSWORD")
RECEIVER_EMAIL = get_environment_variable("ALERT_RECEIVER_EMAIL")
