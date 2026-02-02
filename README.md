# Monitoring Stack on AWS EC2 (Metrics Only)

A production-aligned monitoring stack using **Prometheus** and **Grafana** on AWS EC2,
with a Python Flask application exposing application metrics and **Node Exporter**
providing system-level metrics.

This project focuses on **VM-based observability** using Linux services and a
pull-based monitoring model.

---

## Architecture

The monitoring stack is deployed across three EC2 instances with clear separation
of responsibilities:

### App EC2
- Python Flask application
- Exposes Prometheus metrics at `/metrics`
- Node Exporter for host-level metrics
- Application managed using `systemd`

### Prometheus EC2
- Scrapes application and host metrics
- Stores time-series data locally
- Runs as a `systemd` service

### Grafana EC2
- Visualizes metrics from Prometheus
- Provides dashboards for application and system metrics
- Runs as a `systemd` service

---

## Metrics Endpoints

| Component        | Port | Purpose                     |
|------------------|------|-----------------------------|
| Flask App        | 8080 | Application metrics         |
| Node Exporter    | 9100 | Host/system metrics         |
| Prometheus       | 9090 | Prometheus UI               |
| Grafana          | 3000 | Grafana UI                  |

---

## Network Flow

- Prometheus → App EC2 :8080 (application metrics)
- Prometheus → App EC2 :9100 (node exporter metrics)
- Browser → Grafana EC2 :3000
- Browser → Prometheus EC2 :9090 (optional)

Ports 8080 and 9100 should only allow inbound traffic from the Prometheus EC2.

---

## Repository Structure

```text
monitoring-stack/
├── app/
│   ├── app.py
│   └── requirements.txt
├── prometheus/
│   ├── prometheus.yml
|   └── prometheus.service
├── docs/
│   ├── architecture.md
│   ├── network-flow.md
│   └── setup.md
└── README.md
```
---

## Implemented Features

✔ Flask application running  
✔ Prometheus scraping metrics  
✔ Node Exporter providing host metrics  
✔ Grafana visualizing Prometheus data  

---

## Notes

- Update private IP addresses in `prometheus/prometheus.yml` to match your EC2 instances
- No containers or orchestration tools are used
- All services are managed using `systemd`
- Secrets, credentials, and runtime data are excluded from the repository

---

## Planned Enhancements

- Centralized logging using Loki
- Log shipping using Grafana Alloy
- Distributed tracing using OpenTelemetry

