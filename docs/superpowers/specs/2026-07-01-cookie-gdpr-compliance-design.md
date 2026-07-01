# Cookie consent a GDPR súlad pre vinny-expres.sk

Dátum: 2026-07-01

## Cieľ

Doplniť na stránku vinny-expres.sk (Flask, jednostránkový web s kontaktným formulárom)
všetko, čo slovenské právo (GDPR / zákon č. 18/2018 Z.z. o ochrane osobných údajov,
zákon č. 452/2021 Z.z. o elektronických komunikáciách §109 - cookies) vyžaduje:

- cookie consent banner,
- Zásady ochrany osobných údajov,
- Zásady používania cookies,
- odkazy na tieto stránky z pätičky.

Stránka momentálne nesadzuje žiadne cookies (žiadna Flask session, žiadny tracking
skript). Prevádzkovateľ plánuje v budúcnosti pridať Google Analytics, preto banner musí
riešiť súhlas pred načítaním analytických cookies, nie len informovať.

## Prevádzkovateľ (identifikačné údaje pre právne texty)

- Názov: ReDu Company s. r. o.
- IČO: 57695059
- DIČ: 2122887668
- Sídlo: Cajlanská 1830/123, 902 01 Pezinok
- Kontaktný email: vinny.expres.formular@gmail.com

## Architektúra

### Nové routes (`vinnyexpres/app.py`)

- `GET /ochrana-osobnych-udajov` → render `privacy.html`
- `GET /cookies` → render `cookies.html`

Obe stránky používajú rovnaký layout (hlavička/pätička, CSS) ako `index.html`, obsah je
statický text.

### Cookie consent banner

- Nový súbor `assets/js/cookie-consent.js`, čistý vanilla JS, bez závislostí a bez
  externého CMP (konzistentné s existujúcim jQuery/vanilla JS štýlom projektu, žiadny
  ďalší tretí skript, ktorý by sám osebe musel riešiť súhlas).
- Načítaný z `templates/index.html`, `privacy.html`, `cookies.html` (spoločný include).
- Banner (fixed bottom bar) sa zobrazí, ak cookie `cookie_consent` neexistuje. Tri akcie:
  - **Prijať všetky** → `document.cookie = "cookie_consent=accepted; max-age=15552000; path=/"`,
    zavolá `loadAnalytics()`, banner sa skryje.
  - **Odmietnuť** → uloží `cookie_consent=rejected` (rovnaká expirácia), banner sa skryje,
    `loadAnalytics()` sa nevolá.
  - **Nastavenia** → zatiaľ binárne (essential vs. analytics), keďže momentálne existuje
    len jedna neesenciálna kategória (Google Analytics). Ak pribudnú ďalšie kategórie
    (marketing a pod.), rozšíri sa v budúcom spec-e.
- `loadAnalytics()` je exportovaná funkcia, v tejto fáze **no-op** (bez GA kódu, keďže GA
  ešte nie je pridané) — pripravená na doplnenie GA `gtag.js` snippetu neskôr bez zásahu
  do consent logiky.
- Odkaz "Nastavenia cookies" v pätičke zavolá funkciu, ktorá zmaže cookie `cookie_consent`
  a znova zobrazí banner (umožňuje zmeniť rozhodnutie).

### Pätička (`templates/index.html` a nové stránky)

Pridané odkazy: "Zásady ochrany osobných údajov", "Používanie cookies", "Nastavenia
cookies", a základné identifikačné údaje prevádzkovateľa (názov, IČO, sídlo).

## Právny obsah stránok

### Zásady ochrany osobných údajov (`privacy.html`)

- Identifikácia prevádzkovateľa (viď vyššie).
- Účel spracovania: vybavenie dopytu zaslaného cez kontaktný formulár (meno, telefón,
  email, text správy).
- Právny základ: čl. 6 ods. 1 písm. b) GDPR (predzmluvné vzťahy / vybavenie dopytu) resp.
  písm. f) (oprávnený záujem prevádzkovateľa odpovedať na dopyt).
- Doba uchovávania: údaje z formulára sa uchovávajú len po dobu nevyhnutnú na vybavenie
  dopytu a prípadnú komunikáciu (napr. 12 mesiacov), potom sa mažú.
- Príjemcovia: žiadny externý spracovateľ okrem poskytovateľa emailu (Google/Gmail),
  ktorý doručuje odpoveď.
- Práva dotknutej osoby: prístup, oprava, výmaz, obmedzenie spracúvania, námietka,
  prenosnosť, právo podať sťažnosť na Úrad na ochranu osobných údajov SR.
- Kontakt na uplatnenie práv: vinny.expres.formular@gmail.com.

### Zásady používania cookies (`cookies.html`)

- Vysvetlenie, čo sú cookies a na čo slúžia.
- Aktuálny stav: stránka nepoužíva žiadne nevyhnutné (funkčné) cookies okrem cookie
  `cookie_consent`, ktorá si pamätá voľbu súhlasu (nevyžaduje súhlas, keďže ide o
  technicky nevyhnutnú cookie).
- Analytické cookies (Google Analytics: `_ga`, `_gid`) — označené ako "pripravované /
  aktivujú sa len po súhlase", s vysvetlením účelu (štatistika návštevnosti) a doby
  platnosti.
- Ako odvolať súhlas: odkaz/tlačidlo "Nastavenia cookies" v pätičke.

## Testovanie

Manuálne v prehliadači (dev server):

1. Prvá návšteva → banner sa zobrazí.
2. Klik "Prijať všetky" → banner zmizne, cookie `cookie_consent=accepted` existuje,
   po refreshi sa banner nezobrazí znova.
3. Klik "Odmietnuť" (v inom prehliadači / po zmazaní cookie) → banner zmizne, cookie
   `cookie_consent=rejected`.
4. "Nastavenia cookies" v pätičke → zmaže cookie, banner sa zobrazí znova.
5. `/ochrana-osobnych-udajov` a `/cookies` vrátia HTTP 200 a zobrazia očakávaný obsah.

## Mimo rozsahu

- Samotná integrácia Google Analytics (skript `gtag.js`) — pridá sa neskôr, hook
  `loadAnalytics()` je pripravený.
- Obchodné podmienky / reklamačný poriadok — nepotrebné, stránka nie je e-shop.
- Viacjazyčná verzia právnych textov — stránka je len po slovensky.
