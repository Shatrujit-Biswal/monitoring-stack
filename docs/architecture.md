# Architecture Overview

This project implements a **metrics-only monitoring stack** on AWS EC2 using
**Prometheus** and **Grafana**, with a Python Flask application exposing
application-level metrics and Node Exporter exposing host-level metrics.

The architecture follows a **VM-first, production-style design** with clear
separation of concerns.

---

## EC2 Components

### App EC2
Responsibilities:
- Runs a Python Flask application
- Exposes Prometheus-compatible metrics at `/metrics`
- Runs Node Exporter for system-level metrics
- Application managed as a `systemd` service

Key characteristics:
- Application metrics and host metrics are exposed separately
- No monitoring logic embedded into Prometheus or Grafana

---

### Prometheus EC2
Responsibilities:
- Scrapes metrics from:
  - Flask application
  - Node Exporter
  - Prometheus itself
- Stores time-series data locally
- Runs as a `systemd` service

Key characteristics:
- Pull-based monitoring model
- Centralized metrics collection

---

### Grafana EC2
Responsibilities:
- Visualizes metrics from Prometheus
- Provides dashboards for:
  - Application metrics
  - System metrics

Key characteristics:
- Stateless visualization layer
- Uses Prometheus as a data source

---

## Design Principles

- Clear separation between application, metrics collection, and visualization
- Pull-based metrics scraping
- VM-based observability (no containers)
- Production-aligned Linux service management

---

## Future Enhancements

- Centralized logging using Loki
- Log shipping using Grafana Alloy
- Distributed tracing using OpenTelemetry

