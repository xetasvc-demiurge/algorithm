#!/usr/bin/env python3
# api_retry.py
# Implements:
# 1. Calls an API
# 2. Check for HTTP errors
# 3. Check for malformed responses
# 4. Check for time outs
# 5. Log the errors
# 6. Retry the API Call
# 7. Stop after 5 retries

import json
import logging
import time
from typing import Optional

try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
except ImportError as exc:
    raise SystemExit(
        "Missing dependency: install it with 'pip install requests'."
    ) from exc

# -------- Configuration --------
# API_URL = "https://jsonplaceholder.typicode.com/users"   # <-- replace with your endpoint
API_URL = "https://jsonplaceholder.typicode.com/users/999999"   # <-- replace with your endpoint
TIMEOUT_SECONDS = 5                        # Step 4: timeout for each request
MAX_RETRIES = 3                            # Step 7: stop after 5 retries
BACKOFF_FACTOR = 1                         # backoff: 0, 1, 2, 4, ... seconds
STATUS_FORCELIST = [429, 500, 502, 503, 504]  # statuses considered transient
# -------------------------------

# Step 5: Log the errors
logger = logging.getLogger("api_retry")
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def make_session_with_retries(max_retries: int, backoff_factor: float, status_forcelist):
    """
    Create a requests.Session that uses urllib3 Retry for idempotent retries.
    Note: Retry via HTTPAdapter covers many network/HTTP errors; we still
    perform explicit retries for JSON/malformed/timeouts below to cover all checks.
    """
    session = requests.Session()
    retry = Retry(
        total=max_retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        allowed_methods=frozenset(["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"]),
        raise_on_status=False,  # don't raise for status; we'll handle responses manually
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def call_api(session: requests.Session, url: str, timeout: float) -> Optional[dict]:
    """
    Step 1: Calls an API
    Step 2: Check for HTTP errors
    Step 3: Check for malformed responses (expects JSON)
    Step 4: Check for timeouts (via requests timeout)
    Returns parsed JSON dict on success, None on unrecoverable failure.
    """
    try:
        resp = session.get(url, timeout=timeout)
    except requests.Timeout as e:
        # Step 5: Log the errors
        logger.warning("Request timed out: %s", e)
        raise
    except requests.RequestException as e:
        # network-level errors (DNS, connection refused, etc.)
        logger.error("Network/request exception: %s", e)
        raise

    # Step 2: Check for HTTP errors (non-2xx)
    if not resp.ok:
        logger.warning("HTTP error: %s %s", resp.status_code, resp.reason)
        # treat certain status codes as transient (Retry handled by session/Retry config)
        raise requests.HTTPError(f"HTTP {resp.status_code}: {resp.reason}", response=resp)

    # Step 3: Check for malformed responses (expecting JSON)
    try:
        data = resp.json()
    except ValueError as e:
        logger.error("Malformed JSON response: %s", e)
        raise

    return data


def fetch_with_retries(url: str, max_retries: int, timeout: float, backoff_factor: float):
    session = make_session_with_retries(max_retries, backoff_factor, STATUS_FORCELIST)

    attempt = 0
    while attempt < max_retries:
        attempt += 1
        try:
            logger.info("Attempt %d to call API: %s", attempt, url)
            data = call_api(session, url, timeout)
            logger.info("API call succeeded on attempt %d", attempt)
            return data
        except (requests.Timeout,) as e:
            logger.warning("Timeout on attempt %d: %s", attempt, e)
        except requests.HTTPError as e:
            # For 4xx you might want to stop immediately; treat 5xx/429 as retryable
            status = getattr(e, "response", None)
            status_code = status.status_code if status is not None else None
            if status_code and 400 <= status_code < 500 and status_code not in STATUS_FORCELIST:
                logger.error("Client error %s (not retrying): %s", status_code, e)
                break
            logger.warning("HTTP error on attempt %d: %s", attempt, e)
        except requests.RequestException as e:
            logger.warning("Request exception on attempt %d: %s", attempt, e)
        except Exception as e:
            # This covers malformed JSON and unexpected errors
            logger.error("Unexpected error on attempt %d: %s", attempt, e)

        # Step 6: Retry the API Call (with exponential backoff)
        if attempt < max_retries:
            sleep_time = backoff_factor * (2 ** (attempt - 1))
            logger.info("Retrying after %.1f seconds...", sleep_time)
            time.sleep(sleep_time)
        else:
            logger.error("Reached max retries (%d). Giving up.", max_retries)

    return None


def main():
    result = fetch_with_retries(API_URL, MAX_RETRIES, TIMEOUT_SECONDS, BACKOFF_FACTOR)
    if result is None:
        logger.error("Failed to fetch valid response after %d attempts", MAX_RETRIES)
    else:
        # For demonstration, pretty-print part of the response
        logger.info("Received JSON keys: %s", list(result.keys()) if isinstance(result, dict) else "not a dict")
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()