# DevOps CI/CD on AWS EKS (Staging → Production)

End‑to‑end demo showing how I design and implement a **GitHub Actions (or Jenkins) CI/CD pipeline** for a **microservices** app deployed to **Amazon EKS** with Docker, Kubernetes, and basic monitoring (Prometheus + Grafana).

>  Swap AWS for Azure/DigitalOcean easily—scripts and manifests are cloud‑agnostic except for ECR and EKS bits.

---

##  Architecture Overview

- Two services: `frontend` (Node/Express) and `backend` (Python/Flask + Prometheus metrics)
- Docker images pushed to **Amazon ECR**
- Kubernetes deployments on **Amazon EKS**
- **Environments**:
  - **staging** – auto-deploy from `main` on every push
  - **production** – manual approval via GitHub Environments (or via Jenkins input step)
- **Monitoring**:
  - Prometheus + Grafana (via Helm)
  - Backend exposes `/metrics` using `prometheus_client`

```text
Developer → GitHub → GitHub Actions → Build+Test → Push to ECR → kubectl apply (staging) → Promote → kubectl apply (prod)
```

---

##  Quick Start

### 0) Prerequisites
- An existing **EKS** cluster and kubectl configured
- **AWS Load Balancer Controller** installed (for Ingress) – optional if you use NodePort
- An **ECR** repo or permission to create one
- **Helm** installed (for Prometheus/Grafana)

### 1) AWS GitHub OIDC + Secrets
Setup GitHub OIDC for your repo and add these **Repository → Settings → Secrets and variables → Actions → Variables**:

- `AWS_REGION` (e.g. `us-east-1`)
- `AWS_ACCOUNT_ID`
- `EKS_CLUSTER` (your cluster name)
- `ECR_REPO` (e.g. `devops-portfolio` — the workflow creates it if missing)

Also create an **Environment** named `production` and enable **required reviewers** for manual approval.

> Alternative: use **Jenkinsfile** in `jenkins/` directory.

### 2) Build & Deploy
- Push to `main` ⟶ builds, tests, pushes to ECR, deploys **staging**
- Approve **production** job in Actions UI ⟶ deploys **production**

### 3) Install Monitoring (optional but recommended)

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

# kube-prometheus-stack installs Prometheus, Alertmanager, Grafana, exporters
helm upgrade --install monitoring prometheus-community/kube-prometheus-stack -n monitoring --create-namespace

# Add ServiceMonitor to scrape the backend
kubectl apply -f monitoring/servicemonitor-backend.yaml
```

Access Grafana via port-forward (or configure Ingress):
```bash
kubectl -n monitoring port-forward svc/monitoring-grafana 3000:80
# default creds (override via values): admin / prom-operator
```

---

## 🧪 Testing Locally

```bash
# backend
cd services/backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
FLASK_ENV=development python app.py

# frontend
cd ../frontend
npm install
node server.js
```

---

##  IAM Notes (high level)

- Actions workflow uses **OIDC** to assume a role allowing:
  - `ecr:*` (push/pull)
  - `eks:DescribeCluster`
  - `sts:AssumeRole`
- The workflow sets kubeconfig using cluster’s `certificateAuthority` and `endpoint` via `aws eks update-kubeconfig`.

---

##  Clean Up

- Delete ECR images / repos (optional)
- Uninstall Helm releases: `helm uninstall monitoring -n monitoring`
- (If created) remove AWS IAM role for GitHub OIDC

---

**Author:** Your Name — DevOps Engineer (AWS | Azure | DigitalOcean | K8s | Docker)
