import os
import time
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify, request

from prometheus_client import (
    Counter,
    Histogram,
    Gauge,
    generate_latest,
    CONTENT_TYPE_LATEST
)

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

# ----------------------------
# Prometheus Metrics
# ----------------------------

HTTP_REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

HTTP_REQUEST_LATENCY = Histogram(
    "http_request_latency_seconds",
    "HTTP request latency",
    ["endpoint"]
)

APP_UP = Gauge(
    "app_up",
    "Application availability"
)

APP_UP.set(1)

# ----------------------------
# Routes
# ----------------------------

@app.route("/")
@HTTP_REQUEST_LATENCY.labels(endpoint="/").time()
def index():
    HTTP_REQUESTS_TOTAL.labels("GET", "/", 200).inc()
    logger.info("Root endpoint called")
    return jsonify({"status": "ok", "message": "Demo observability app running"})


@app.route("/health")
@HTTP_REQUEST_LATENCY.labels(endpoint="/health").time()
def health():
    HTTP_REQUESTS_TOTAL.labels("GET", "/health", 200).inc()
    logger.info("Health check requested")
    return jsonify({"status": "healthy"})


@app.route("/work")
@HTTP_REQUEST_LATENCY.labels(endpoint="/work").time()
def do_work():
    logger.info("Work endpoint triggered")
    time.sleep(1)
    HTTP_REQUESTS_TOTAL.labels("GET", "/work", 200).inc()
    logger.info("Work completed successfully")
    return jsonify({"result": "done"})


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


@app.errorhandler(Exception)
def handle_exception(e):
    HTTP_REQUESTS_TOTAL.labels(
        request.method,
        request.path,
        500
    ).inc()
    logger.error("Unhandled exception occurred", exc_info=True)
    return jsonify({"error": "internal server error"}), 500


# ----------------------------
# App startup
# ----------------------------

if __name__ == "__main__":
    logger.info("Starting demo observability application")
    app.run(host="0.0.0.0", port=8080)

