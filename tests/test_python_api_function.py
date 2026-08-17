import responses

from python_API_function import fetch_with_retries

URL = "https://example.test/api/resource"


@responses.activate
def test_fetch_with_retries_succeeds_first_try():
    responses.add(responses.GET, URL, json={"ok": True}, status=200)
    result = fetch_with_retries(URL, max_retries=3, timeout=1, backoff_factor=0)
    assert result == {"ok": True}


@responses.activate
def test_fetch_with_retries_gives_up_after_max_retries():
    for _ in range(3):
        responses.add(responses.GET, URL, status=500)
    result = fetch_with_retries(URL, max_retries=3, timeout=1, backoff_factor=0)
    assert result is None


@responses.activate
def test_fetch_with_retries_stops_immediately_on_client_error():
    responses.add(responses.GET, URL, status=404)
    result = fetch_with_retries(URL, max_retries=3, timeout=1, backoff_factor=0)
    assert result is None
