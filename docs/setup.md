# Setup Guide

This document provides a step-by-step setup of a **metrics-only monitoring stack**
on AWS EC2 using **Prometheus**, **Grafana**, **Node Exporter**, and a Python Flask application.

The setup follows a **VM-based observability model** and uses Linux services where appropriate.
Application process management is intentionally kept manual.

---

## Prerequisites

- AWS EC2 instances running Ubuntu
- Basic Linux and networking knowledge
- Security Groups configured for required ports

---

## EC2 Instances Overview

| EC2 Name       | Purpose |
|---------------|---------|
| App EC2        | Flask application + Node Exporter |
| Prometheus EC2 | Metrics scraping and storage |
| Grafana EC2    | Metrics visualization |

---

## Security Group Configuration

### App EC2
- 22 (SSH)
- 8080 (Flask metrics) — allow **only from Prometheus EC2**
- 9100 (Node Exporter) — allow **only from Prometheus EC2**

### Prometheus EC2
- 22 (SSH)
- 9090 (Prometheus UI)

### Grafana EC2
- 22 (SSH)
- 3000 (Grafana UI)

---

## App EC2 Setup

### 1. System Preparation

```bash
sudo apt update
sudo apt install -y python3-full python3-venv
```

---

### 2. Application Setup

```bash
mkdir ~/app
cd ~/app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

- Application exposes `/metrics` using `prometheus-client`
- Logs are written to `/var/log/demo-app/app.log`

---

### 3. Application Execution

The application is started manually:

```bash
source venv/bin/activate
python app.py
```
---

### 4. Node Exporter Installation

```bash
cd /opt
sudo curl -LO https://github.com/prometheus/node_exporter/releases/download/v1.8.1/node_exporter-1.8.1.linux-amd64.tar.gz
sudo tar xvf node_exporter-1.8.1.linux-amd64.tar.gz
sudo useradd --no-create-home --shell /bin/false node_exporter
sudo mv node_exporter-1.8.1.linux-amd64/node_exporter /usr/local/bin/
sudo chown node_exporter:node_exporter /usr/local/bin/node_exporter
```

Node Exporter is started as a system service on the host.

---

## Prometheus EC2 Setup

### 1. Install Prometheus

```bash
wget https://github.com/prometheus/prometheus/releases/download/v3.9.1/prometheus-3.9.1.linux-amd64.tar.gz
tar -xvzf prometheus-3.9.1.linux-amd64.tar.gz
sudo useradd --no-create-home --shell /bin/false prometheus
sudo mkdir /etc/prometheus /var/lib/prometheus
sudo chown prometheus:prometheus /etc/prometheus /var/lib/prometheus
sudo mv prometheus-*/prometheus /usr/local/bin/
sudo mv prometheus-*/promtool /usr/local/bin/
sudo chown prometheus:prometheus /usr/local/bin/prometheus /usr/local/bin/promtool
```

---

### 2. Prometheus Configuration

- `prometheus.yml` is located in the `prometheus/` directory of this repository
- Scrape targets include:
  - Prometheus itself
  - Flask application
  - Node Exporter

> Private IPs must be updated to match your App EC2.

---

### 3. Prometheus Service

The `prometheus.service` file is **available in the `prometheus/` directory**.

Steps:
1. Copy it to `/etc/systemd/system/`
2. Reload systemd
3. Enable and start Prometheus

---

## Grafana EC2 Setup

### 1. Install Grafana

```bash
sudo apt update
sudo apt install -y wget gpg
sudo mkdir -p /etc/apt/keyrings
wget -q -O - https://apt.grafana.com/gpg.key | gpg --dearmor | sudo tee /etc/apt/keyrings/grafana.gpg > /dev/null
echo "deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main" | sudo tee /etc/apt/sources.list.d/grafana.list
sudo apt update
sudo apt install -y grafana-enterprise
sudo systemctl enable --now grafana-server
```

---

### 2. Grafana Configuration

- Access Grafana at `http://<grafana-ec2>:3000`
- Add **Prometheus** as a data source
- Create dashboards for:
  - Application metrics
  - Node Exporter system metrics

---

## Validation Checklist

- `http://<app-ec2>:8080/metrics` reachable
- `http://<app-ec2>:9100/metrics` reachable
- Prometheus targets show **UP**
- Grafana dashboards display live data

---

## Notes

- Update private IPs in `prometheus.yml`
