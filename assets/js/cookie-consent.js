(function () {
  var CONSENT_COOKIE = "cookie_consent";
  var CONSENT_MAX_AGE = 60 * 60 * 24 * 180; // 180 dní

  function getCookie(name) {
    var match = document.cookie.match(new RegExp("(?:^|; )" + name + "=([^;]*)"));
    return match ? decodeURIComponent(match[1]) : null;
  }

  function setCookie(name, value) {
    document.cookie = name + "=" + encodeURIComponent(value) + "; max-age=" + CONSENT_MAX_AGE + "; path=/; SameSite=Lax; Secure";
  }

  function deleteCookie(name) {
    document.cookie = name + "=; max-age=0; path=/";
  }

  function loadAnalytics() {
    // Google Analytics sa zatiaľ nepoužíva. Keď bude pridané, gtag.js
    // skript sa vloží sem - zavolá sa len ak bol udelený súhlas.
  }

  function showBanner() {
    var banner = document.getElementById("cookie-consent-banner");
    if (banner) {
      banner.style.display = "block";
    }
  }

  function hideBanner() {
    var banner = document.getElementById("cookie-consent-banner");
    if (banner) {
      banner.style.display = "none";
    }
  }

  function accept() {
    setCookie(CONSENT_COOKIE, "accepted");
    hideBanner();
    loadAnalytics();
  }

  function reject() {
    setCookie(CONSENT_COOKIE, "rejected");
    hideBanner();
  }

  function openSettings() {
    deleteCookie(CONSENT_COOKIE);
    showBanner();
  }

  document.addEventListener("DOMContentLoaded", function () {
    var acceptBtn = document.getElementById("cookie-consent-accept");
    var rejectBtn = document.getElementById("cookie-consent-reject");
    var settingsLink = document.getElementById("cookie-consent-settings-link");

    if (acceptBtn) acceptBtn.addEventListener("click", accept);
    if (rejectBtn) rejectBtn.addEventListener("click", reject);
    if (settingsLink) {
      settingsLink.addEventListener("click", function (e) {
        e.preventDefault();
        openSettings();
      });
    }

    var consent = getCookie(CONSENT_COOKIE);
    if (consent === "accepted") {
      loadAnalytics();
    } else if (consent === null) {
      showBanner();
    }
  });
})();
