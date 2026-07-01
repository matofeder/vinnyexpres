def test_index_page_includes_cookie_consent_banner(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b'id="cookie-consent-banner"' in response.data
    assert b'/assets/js/cookie-consent.js' in response.data


def test_index_page_includes_footer_legal_links(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"ReDu Company s. r. o." in response.data
    assert b'href="/ochrana-osobnych-udajov"' in response.data
    assert b'href="/cookies"' in response.data
    assert b'id="cookie-consent-settings-link"' in response.data


def test_privacy_page_returns_200(client):
    response = client.get("/ochrana-osobnych-udajov")

    assert response.status_code == 200
    assert "Zásady ochrany osobných údajov".encode("utf-8") in response.data
    assert b"57695059" in response.data
    assert b'id="cookie-consent-banner"' in response.data
    assert b"ReDu Company s. r. o." in response.data
    assert b'id="cookie-consent-settings-link"' in response.data


def test_cookies_page_returns_200(client):
    response = client.get("/cookies")

    assert response.status_code == 200
    assert "Používanie cookies".encode("utf-8") in response.data
    assert b"cookie_consent" in response.data
    assert b'id="cookie-consent-banner"' in response.data
    assert b"ReDu Company s. r. o." in response.data
    assert b'id="cookie-consent-settings-link"' in response.data


def test_cookie_consent_js_is_served(client):
    response = client.get("/assets/js/cookie-consent.js")

    assert response.status_code == 200
