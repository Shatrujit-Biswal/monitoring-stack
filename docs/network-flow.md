# Network Flow

This document describes the network communication paths between EC2 instances
and services in the monitoring stack.

---

## Metrics Flow

### Application Metrics

- **Source:** Prometheus EC2
- **Destination:** App EC2
- **Port:** 8080
- **Endpoint:** `/metrics`

Purpose:
- Scrape application-level metrics exposed by the Flask app

---

### Host Metrics (Node Exporter)

- **Source:** Prometheus EC2
- **Destination:** App EC2
- **Port:** 9100
- **Endpoint:** `/metrics`

Purpose:
- Scrape system-level metrics (CPU, memory, disk, network)

---

### Prometheus Self-Metrics

- **Source:** Prometheus EC2
- **Destination:** Prometheus EC2
- **Port:** 9090

Purpose:
- Monitor Prometheus internal health and performance

---

## User Access

### Grafana UI

- **Source:** User Browser
- **Destination:** Grafana EC2
- **Port:** 3000

Purpose:
- View dashboards and explore metrics

---

### Prometheus UI (Optional)

- **Source:** User Browser
- **Destination:** Prometheus EC2
- **Port:** 9090

Purpose:
- Validate scrape targets and query raw metrics

---

## Security Notes

- Ports 8080 and 9100 should only allow access from the Prometheus EC2
- Grafana (3000) and Prometheus (9090) should be restricted to trusted IPs
- No service exposes credentials over the network

