# Setup Guide

This document provides a high-level overview of how the monitoring stack is set up.
Detailed command-by-command instructions are intentionally omitted.

---

## Prerequisites

- AWS EC2 instances running Ubuntu
- Basic Linux and systemd knowledge
- Security Groups configured for required ports

---

## App EC2 Setup

- Python Flask application installed in a virtual environment
- Application exposes `/metrics` using `prometheus-client`
- Application runs as a `systemd` service
- Node Exporter installed and running as a `systemd` service

---

## Prometheus EC2 Setup

- Prometheus binary installed manually
- Custom `prometheus.yml` configured
- Scrape targets include:
  - Prometheus itself
  - Flask application
  - Node Exporter
- Prometheus runs as a `systemd` service

---

## Grafana EC2 Setup

- Grafana installed via APT repository
- Grafana runs as a `systemd` service
- Prometheus added as a data source
- Dashboards created for:
  - Application metrics
  - System metrics

---

## Validation Checklist

- Application reachable on port 8080
- Node Exporter reachable on port 9100
- Prometheus shows all targets as `UP`
- Grafana dashboards display live data

---

## Notes

- Private IPs must be updated in `prometheus.yml`
- This setup focuses on VM-based monitoring, not containers

