---
title: Setup Kubernetes Quickstart
excerpt: Harrison to test this out.
deprecated: false
hidden: false
metadata:
  robots: index
next:
  pages:
    - slug: gateway-k8s-quickstart
      title: Akeyless Gateway with Kubernetes Quickstart
      type: basic
---
This Quickstart helps you prepare a local Kubernetes environment using **Docker Desktop** so that you can deploy the Akeyless Gateway with the main Akeyless Gateway with Kubernetes Quickstart.

By the end of this guide, you will have:

* Kubernetes enabled in Docker Desktop
* `kubectl` pointing at the Docker Desktop cluster
* Helm installed and working
* Kubernetes Metrics Server installed
* Basic resource and network checks completed

This environment is intended for **development and testing only**, not production use.

## Prerequisites

You will need:

* Docker Desktop installed ([Windows](https://docs.docker.com/desktop/setup/install/windows-install/), <Anchor label="macOS" target="_blank" href="https://docs.docker.com/desktop/setup/install/mac-install/">macOS</Anchor>, or <Anchor label="Linux" target="_blank" href="https://docs.docker.com/desktop/setup/install/linux/">Linux</Anchor>)
* Permissions to change Docker Desktop settings
* Internet access from your machine

## Step 1: Enable Kubernetes in Docker Desktop

1. Open **Docker Desktop**.
2. Open Docker Desktop's setting, select the **Kubernetes** options, and **Enable Kubernetes**. This guide was tested with the `Kubeadm` setting.
3. Apply the change and allow Docker Desktop to install or restart Kubernetes if prompted.
4. Wait until Docker Desktop shows that **Kubernetes** is running.

## Step 2: Verify kubectl and Context

1. <br />
2. Ensure `kubectl` is installed:

```bash
kubectl version --client
```

2. Verify that your current context points to the Docker Desktop cluster:

```bash
kubectl config get-contexts
kubectl config use-context docker-desktop
```

Check that the cluster responds:

```bash
kubectl get nodes
```

## Step 3: Install and Verify Helm

Verify Helm:

```bash
helm version
```

List repos:

```bash
helm repo list
```

## Step 4: Configure Docker Desktop Resources

Configure Docker Desktop with at least:

* 2 CPUs
* 4 GB RAM

Adjust these in **Settings → Resources**.

## Step 5: Verify Network Connectivity to Akeyless

Run:

```bash
kubectl run curl-test --image=curlimages/curl --restart=Never --command --   curl -I https://console.akeyless.io
```

Check logs:

```bash
kubectl logs curl-test
```

Delete the pod:

```bash
kubectl delete pod curl-test
```

## Step 6: Install Kubernetes Metrics Server

Install:

```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

## Step 7: Verify Metrics Server

Check deployment:

```bash
kubectl get deployment metrics-server -n kube-system
```

Check metrics:

```bash
kubectl top nodes
```

***

_You have now prepared a Docker Desktop Kubernetes environment suitable for deploying the Akeyless Gateway._
