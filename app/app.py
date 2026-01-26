import time
import random
import logging
from flask import Flask, request, jsonify

from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

# -----------------------------
# Logging setup (Loki-friendly)
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s level=%(levelname)s service=demo-app message=%(message)s",
)
logger = logging.getLogger("demo-app")

# -----------------------------
# Tracing setup (Tempo / OTLP)
# -----------------------------
resource = Resource(attributes={
    "service.name": "demo-observability-app"
})

trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

otlp_exporter = OTLPSpanExporter()
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# -----------------------------
# Metrics (Prometheus)
# -----------------------------
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["endpoint"]
)

ERROR_COUNT = Counter(
    "application_errors_total",
    "Total application errors"
)

# -----------------------------
# Flask App
# -----------------------------
app = Flask(__name__)

@app.route("/health")
def health():
    logger.info("Health check requested")
    return {"status": "ok"}

@app.route("/work")
def do_work():
    with tracer.start_as_current_span("process_work") as span:
        start_time = time.time()

        processing_time = random.uniform(0.1, 1.5)
        time.sleep(processing_time)

        if random.random() < 0.25:
            ERROR_COUNT.inc()
            logger.error("Simulated application error")
            span.record_exception(Exception("simulated failure"))
            span.set_status(trace.Status(trace.StatusCode.ERROR))
            status = 500
            response = {"result": "error"}
        else:
            logger.info("Work processed successfully")
            status = 200
            response = {"result": "success"}

        duration = time.time() - start_time

        REQUEST_COUNT.labels(
            method="GET",
            endpoint="/work",
            status=status
        ).inc()

        REQUEST_LATENCY.labels(endpoint="/work").observe(duration)

        span.set_attribute("app.processing_time", duration)
        span.set_attribute("app.status_code", status)

        return jsonify(response), status

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    logger.info("Starting demo observability application")
    app.run(host="0.0.0.0", port=8080)

