def test_index_page_includes_cookie_consent_banner(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b'id="cookie-consent-banner"' in response.data
    assert b'/assets/js/cookie-consent.js' in response.data
