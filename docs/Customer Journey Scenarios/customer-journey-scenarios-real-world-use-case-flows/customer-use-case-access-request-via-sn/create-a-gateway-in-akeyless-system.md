---
title: Docker setup and configuration
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
To install and configure a standalone instance of Akeyless Gateway using Docker, follow these steps. It's important to note that all of these actions can be conveniently performed using Docker Desktop, a user-friendly interface for managing Docker applications.

# Installation Steps:

* Run Akeyless Gateway Container:
  * Open a terminal or command prompt on your machine.
  * Execute the following Docker command to install and run a standalone instance of the Akeyless Gateway:
  * This command downloads the Akeyless Gateway image from the Docker repository (if not already present) and runs it as a container named akeyless-gateway. It maps multiple ports to ensure full functionality of the Akeyless Gateway, including the management interface and various service endpoints.

```Text Yaml
docker run -d -p 8000:8000 -p 8200:8200 -p 18888:18888 -p 8080:8080 -p 8081:8081 -p 5696:5696 --name akeyless-gateway akeyless/base:latest-akeyless
```

* Confirm Container is Running:
  * Use the docker ps command to confirm the container is running. You should see akeyless-gateway listed among the active containers.
* Upgrading Akeyless Gateway:
  * To upgrade your Akeyless Gateway to the latest version, simply restart the container with the command:
  * Docker will ensure that the container uses the latest image version tagged latest-akeyless.

```Text Yaml
docker restart akeyless-gateway
```

# Initial Configuration:

* Accessing Akeyless Gateway:
  * Open your preferred web browser.
  * Navigate to http\://localhost:8000 or replace localhost with your Docker host's IP address if you're not running the browser on the same machine as Docker. This will take you to the Akeyless Gateway's login page.

# Logging In:

* Enter your credentials to log in. If this is your first time logging in and you haven't set up an authentication method during installation, the first credentials you use will be associated with the admin user for this gateway.
