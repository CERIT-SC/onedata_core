import logging
import sys
from flask import Flask
from views.example import example_bp
from views.onezone import onezone_bp

app = Flask(__name__, static_url_path='', static_folder="static")
app.register_blueprint(example_bp)
app.register_blueprint(onezone_bp)


@app.route("/")
def index():
    """
    Returns application index
    """
    return "Return from the Hello side"


@app.route('/favicon.ico')
def favicon():
    """
    Returns application favicon
    """
    return app.send_static_file('favicon.ico')


if __name__ == "__main__":
    logging.basicConfig(
        handlers=[
            logging.FileHandler("syslog.log", mode="w", encoding="utf-8"),
            logging.StreamHandler(sys.stdout)
        ],
        level=logging.DEBUG,
        format='%(asctime)s:%(levelname)s:%(name)s@%(threadName)s:%(message)s'
    )

    with app.app_context():
        app.config["SECRET_KEY"] = "SECRET_KEY"

    app.run(debug=True, port=5000)
