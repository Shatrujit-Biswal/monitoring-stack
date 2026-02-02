import os
import time
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify, request

# ----------------------------
# Logging setup (FILE-BASED)
# ----------------------------

LOG_DIR = "/var/log/demo-app"
LOG_FILE = f"{LOG_DIR}/app.log"

os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("demo-app")
logger.setLevel(logging.INFO)

file_handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=10 * 1024 * 1024,  # 10 MB
    backupCount=5
)

formatter = logging.Formatter(
    "%(asctime)s level=%(levelname)s service=demo-app message=%(message)s"
)

file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.propagate = False

# ----------------------------
# Flask application
# ----------------------------

app = Flask(__name__)

@app.route("/")
def index():
    logger.info("Root endpoint called")
    return jsonify({"status": "ok", "message": "Demo observability app running"})

@app.route("/health")
def health():
    logger.info("Health check requested")
    return jsonify({"status": "healthy"})

@app.route("/work")
def do_work():
    logger.info("Work endpoint triggered")
    time.sleep(1)
    logger.info("Work completed successfully")
    return jsonify({"result": "done"})

@app.errorhandler(Exception)
def handle_exception(e):
    logger.error("Unhandled exception occurred", exc_info=True)
    return jsonify({"error": "internal server error"}), 500

# ----------------------------
# App startup
# ----------------------------

if __name__ == "__main__":
    logger.info("Starting demo observability application")
    app.run(host="0.0.0.0", port=8080)

