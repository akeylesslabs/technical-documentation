---
title: Getting a Secret with a Kubernetes Container Quickstart
excerpt: Harrison needs to review all of this still.
deprecated: false
hidden: false
metadata:
  robots: index
---
# Getting a Secret with a Kubernetes Container Quickstart

This Quickstart shows how to **inject a secret from Akeyless into a Kubernetes container** using the **Akeyless Kubernetes Secrets Injector**. Your application will read the secret from a file inside the container’s filesystem; the injector handles authentication and secret retrieval.

---

## Prerequisites

You will need:

- A running Kubernetes cluster (v1.21 or later recommended)
- `kubectl` configured
- An Akeyless Gateway reachable from the cluster
- A Static Secret in Akeyless (e.g., `/QuickStart/QuickSecret`)
- The Akeyless Kubernetes Secrets Injector installed and configured

---

## Step 1: Confirm the Akeyless Secrets Injector is Running

```bash
kubectl get pods -n akeyless
```

---

## Step 2: Create a Namespace for the Demo

```bash
kubectl create namespace akeyless-demo
kubectl label namespace akeyless-demo name=akeyless
```

---

## Step 3: Verify the Secret Exists in Akeyless

Ensure a static secret exists at `/QuickStart/QuickSecret`.

---

## Step 4: Create a Demo Deployment

Create `akeyless-secret-demo.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: akeyless-secret-demo
  namespace: akeyless-demo
spec:
  replicas: 1
  selector:
    matchLabels:
      app: akeyless-secret-demo
  template:
    metadata:
      labels:
        app: akeyless-secret-demo
      annotations:
        akeyless/enabled: "true"
        akeyless/inject_file: "/QuickStart/QuickSecret"
    spec:
      containers:
      - name: demo
        image: alpine:3.19
        command:
          - "sh"
          - "-c"
          - |
            echo "Reading secret from file..."
            cat /akeyless/secrets/QuickStart/QuickSecret || echo "Secret file not found"
            sleep 3600
```

Apply it:

```bash
kubectl apply -f akeyless-secret-demo.yaml
```

---

## Step 5: Verify the Pod Started

```bash
kubectl get pods -n akeyless-demo
```

If issues arise:

```bash
kubectl describe pod -n akeyless-demo <pod-name>
kubectl logs -n akeyless-demo <pod-name> -c akeyless-init
```

---

## Step 6: Read the Secret from the Container

```bash
kubectl logs -n akeyless-demo deploy/akeyless-secret-demo
```

Or exec:

```bash
POD_NAME=$(kubectl get pods -n akeyless-demo -l app=akeyless-secret-demo -o jsonpath='{.items[0].metadata.name}')
kubectl exec -it -n akeyless-demo "$POD_NAME" -- sh
cat /akeyless/secrets/QuickStart/QuickSecret
```

---

## Step 7: Clean Up

```bash
kubectl delete -f akeyless-secret-demo.yaml
kubectl delete namespace akeyless-demo
```

---

## Summary

You have successfully:

1. Enabled secret injection with the Akeyless Kubernetes Secrets Injector  
2. Created a demo deployment using annotation-based secret retrieval  
3. Retrieved an Akeyless secret directly inside a container  
