---
title: 'Beyond .env: Building a "Dynamic-Only" Secretless AI Agent with Google ADK'
deprecated: false
hidden: true
metadata:
  robots: index
---
<br />

Introduction

In AI development, we're obsessed with agent capabilities. But what about their security? An AI agent is a high-value target, holding keys to models (like Gemini) and, more critically, your data (like a MongoDB database).

The common solution, .env files or Kubernetes secrets, just moves the problem. You still have a static, long-lived password sitting on a server. If that's compromised, it's game over.

This post explores a more radical, secure architecture: a "dynamic-only" secretless agent. We'll walk through the code for a Google ADK agent that starts with zero credentials. It uses its native GCP cloud identity to fetch its Gemini API key, and for its database, it only accepts just-in-time, dynamic credentials.

<Image border={false} src="https://files.readme.io/f5c06bb7db757f742fa8959b6e0e705c800baeb66f72fc9b06283a60c37522a4-8630a779-57cb-4b0c-a9d4-65756bd93296.png" />

<br />

This architecture fundamentally changes how an app accesses resources.

1. Identity, Not Secrets: The only secret is the agent's built-in Google Cloud (GCP) IAM identity. It has no API keys, no tokens, and no password files.
2. Identity-Based Auth: At startup, the agent asks the local Akeyless CLI to authenticate using its GCP identity. Akeyless verifies this with GCP and issues a short-lived token.
3. Static Secret Fetch: The agent uses this token to fetch its static Gemini_API_Key from Akeyless and loads it into memory.
4. Dynamic Secret Generation: When it needs database access, it again uses its token to ask Akeyless: "Please create a new, temporary user for my MongoDB."
5. Just-in-Time Access: Akeyless generates a unique username/password with a 5-minute TTL, passes it back, and the agent builds its connection string in memory.
6. Ephemeral Use: The agent connects, runs its query, and disconnects. Minutes later, the database credentials it used automatically expire and are deleted.

The result: The agent's database credentials only exist for the few seconds they are needed. An attacker scanning the environment would find nothing to steal.

<br />

Code Deep Dive: The Secretless Engine

Let's break down the Python code that makes this possible.

Part 1: The Resilient Authentication Core

Before we can fetch any secret, we need a token. But that token can expire. This function, fetch_secret_from_akeyless, is a resilient engine that can get any static secret. It first tries optimistically, and if it fails, it performs a full re-authentication using its GCP identity.

```python Phyton
def fetch_secret_from_akeyless(secret_name: str) -> Optional[str]:
    """Fetch any secret from Akeyless CLI - no local storage"""
    try:
        print(f"Fetching {secret_name} from Akeyless CLI...")
        
        # First, try with any existing authentication
        result = subprocess.run([
            'akeyless', 'get-secret-value',
            '--name', secret_name
        ], capture_output=True, text=True, timeout=30)

        if result.returncode == 0:
            #... success ...
            return result.stdout.strip()
        
        # If that failed, auth has expired. Get a fresh token.
        print(f"Authentication expired, getting fresh token for {secret_name}...")
        
        # 1. Get the machine's GCP cloud identity
        cloud_id_result = subprocess.run([
            'akeyless', 'get-cloud-identity', '--cloud-provider', 'gcp'
        ], capture_output=True, text=True, timeout=30, env={**os.environ, 'GOOGLE_APPLICATION_CREDENTIALS': '/tmp/gcp-service-account.json'})
        
        cloud_id = cloud_id_result.stdout.strip()
        
        # 2. Use that identity to authenticate to Akeyless
        auth_result = subprocess.run([
            'akeyless', 'auth', '--access-type=gcp', '--access-id=p-example-id', f'--cloud-id={cloud_id}'
        ], capture_output=True, text=True, timeout=30)
        
        # 3. Extract the new, short-lived token
        token_line = [line for line in auth_result.stdout.split('\n') if 'Token:' in line]
        token = token_line[0].split('Token:')[1].strip()
        
        # 4. Retry fetching the secret with the new token
        result = subprocess.run([
            'akeyless', 'get-secret-value', '--name', secret_name, f'--token={token}'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            return result.stdout.strip()

    except Exception as e:
        print(f"Unexpected error fetching {secret_name}: {e}")
        return None

```

This function is our workhorse for static secrets, like the Gemini key:

<br />

```python Phyton
def fetch_api_key_from_akeyless():
    """Fetch Google API key from Akeyless CLI - no local storage"""
    return fetch_secret_from_akeyless('/Gemini_API_Key-V2')
```

<br />
