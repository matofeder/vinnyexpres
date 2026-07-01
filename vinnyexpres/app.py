import logging
import pytz
from datetime import datetime
from smtplib import SMTPException

from flask import Flask, render_template, request, send_from_directory, Response
from flask_bootstrap import Bootstrap

from .loggers import setup_logging
from .utils import email_sent, email_validate, ValidateEmailError

setup_logging()
log = logging.getLogger(__name__)

app = Flask(__name__, template_folder="../templates", static_folder="../assets")
Bootstrap(app)


@app.route("/robots.txt")
@app.route("/sitemap.xml")
@app.route("/favicon.ico")
def static_from_root():
    return send_from_directory("../assets", request.path[1:])


@app.route("/")
@app.route("/index/")
def main_page():
    return render_template("index.html")


@app.route("/ochrana-osobnych-udajov")
def privacy_policy():
    return render_template("privacy.html")


AUTO_REPLY = """
Ďakujeme za prejavený záujem.
Vašu požiadavku spracujeme a budeme Vás kontaktovať.

S pozdravom,

Vínny Expres
"""


@app.route("/form", methods=["POST", "GET"])
def form_data():
    data = request.get_json()
    name = data["name"]
    phone = data["phone"]
    email = data["email"]
    text = data["text"]

    # try:
    #     email_validate(email)
    # except ValidateEmailError:
    #     log.error("Failed to validate form email %r" % email)
    #     return Response(
    #         "Failed to validate form email",
    #         status=403,
    #     )

    now = "{0:%Y-%m-%d %H:%M:%S}".format(
        datetime.now(pytz.timezone("Europe/Bratislava"))
    )
    form = f"Cas: {now}\nMeno: {name}\nTelefon: {phone}\nEmail: {email}\nText: {text}\n"

    try:
        email_sent(form)
        email_sent(AUTO_REPLY, email_to=email)
    except SMTPException:
        log.error("Failed to sent form email %r" % form)
        return Response(
            "Failed to sent form email",
            status=500,
        )

    log.info("Form email was sent successfully: %r" % form)
    return Response(
        "OK",
        status=200,
    )


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host="0.0.0.0", debug=True, port=5000)
