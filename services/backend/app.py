from flask import Flask, jsonify
import os
import time
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

REQUEST_COUNT = Counter('backend_requests_total', 'Total request count', ['endpoint'])
LATENCY = Histogram('backend_request_latency_seconds', 'Request latency', ['endpoint'])

@app.route("/")
def index():
    start = time.time()
    msg = {"service": "backend", "message": "Hello from backend!", "env": os.getenv("APP_ENV","local")}
    duration = time.time() - start
    REQUEST_COUNT.labels("/").inc()
    LATENCY.labels("/").observe(duration)
    return jsonify(msg)

@app.route("/healthz")
def healthz():
    return "ok", 200

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
