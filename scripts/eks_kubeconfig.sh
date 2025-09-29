#!/usr/bin/env bash
set -euo pipefail
aws eks update-kubeconfig --name "$EKS_CLUSTER" --region "$AWS_REGION"
