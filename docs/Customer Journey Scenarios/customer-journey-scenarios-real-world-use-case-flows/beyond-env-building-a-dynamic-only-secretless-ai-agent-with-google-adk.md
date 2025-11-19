---
title: Akeyless Secretless AI Agent with Google ADK
deprecated: false
hidden: true
metadata:
  robots: index
---
### Introduction

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

### Code Deep Dive: The Secretless Engine

Let's break down the Python code that makes this possible.

#### Part 1: The Resilient Authentication Core

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

```python Phyton
def fetch_api_key_from_akeyless():
    """Fetch Google API key from Akeyless CLI - no local storage"""
    return fetch_secret_from_akeyless('/Gemini_API_Key-V2')
```

<br />

#### Part 2: The "Dynamic-Only" Database Access

This is the most critical part of the new code. This function's job is to get MongoDB credentials. It does not look for static connection strings. It only attempts to fetch dynamic, just-in-time credentials. If it can't, it fails which is exactly the behavior we want.

```python Phyton
def fetch_mongodb_credentials_from_akeyless() -> Optional[Dict[str, str]]:
    """Fetch MongoDB credentials from Akeyless CLI dynamic secret - no local storage"""
    
    dynamic_secret_names = [
        '/MongoDB_Dynamic_Secret',
        '/MongoDB_Dynamic_Credentials',
        '/MongoDB_User_Password'
    ]
    
    for secret_name in dynamic_secret_names:
        try:
            print(f"Fetching dynamic secret {secret_name}...")
            
            # Note the different command: 'dynamic-secret get-value'
            # This COMMANDS Akeyless to CREATE credentials
            result = subprocess.run([
                'akeyless', 'dynamic-secret', 'get-value',
                '--name', secret_name
            ], capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                # Akeyless returns JSON with the new username and password
                secret_data = json.loads(result.stdout.strip())
                print(f"Found MongoDB dynamic secret in {secret_name}")
                
                username = secret_data.get('username', secret_data.get('user'))
                password = secret_data.get('password', secret_data.get('pass'))
                
                if not username or not password:
                    continue # Malformed secret, try the next name

                # Build the connection string IN MEMORY.
                # This credential never touches disk.
                connection_string = f"mongodb+srv://{username}:{password}@cluster0.tqb6hbu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
                
                return {
                    "connection_string": connection_string, 
                    "secret_name": secret_name,
                    "username": username,
                    "is_dynamic": True
                }
            
            # If it failed, it attempts the same GCP IAM re-auth flow
            # (Re-auth logic omitted for brevity, it's the same as Part 1)
            ...
            
        except Exception as e:
            print(f"Error fetching dynamic secret {secret_name}: {e}")
            continue
    
    # If the loop finishes without returning, no dynamic secret was found.
    print("No MongoDB dynamic secrets found in Akeyless")
    return None

```

#### Part 3: Bootstrapping the "Secretless" Agent

Finally, we wrap this logic into an initialization function that the Google ADK agent calls when it's created.

```python Phyton
import os
import json
import subprocess
import google.generativeai as genai  
from typing import Optional, Dict
from akeyless_adk_module.akeyless_fetch import (  
    fetch_api_key_from_akeyless, 
    fetch_mongodb_credentials_from_akeyless
)

# Credentials only exist as global variables in memory
api_key = None
mongodb_credentials = None

def initialize_credentials():
    """Initialize credentials when the agent is actually used"""
    global api_key, mongodb_credentials
    
    try:
        # 1. Fetch and configure the Gemini API Key
        if api_key is None:
            print("Initializing API key from Akeyless...")
            api_key = fetch_api_key_from_akeyless()  # Sets the global variable
            if not api_key:
                print("Failed to fetch Gemini API key.")
                return False
            
            # 2. Load it directly into the Google client configuration
            #    This avoids using an environment variable.
            genai.configure(api_key=api_key)
            print(f"Google AI client configured in memory: {api_key[:20]}...")
        
        # 3. Fetch the DYNAMIC MongoDB credentials
        if mongodb_credentials is None:
            print("Initializing MongoDB credentials from Akeyless...")
            mongodb_credentials = fetch_mongodb_credentials_from_akeyless()
            if mongodb_credentials:
                print("MongoDB credentials loaded in memory")
            else:
                # Note: MongoDB features will be disabled
                print("MongoDB dynamic secret not available - MongoDB features disabled")
        
        return True
    except Exception as e:
        print(f"Error during credential initialization: {e}")
        return False
```

<br />

This code initializes an AI agent's credentials securely by fetching them directly from Akeyless at runtime, rather than storing them in files.

When the agent starts, the initialize_credentials function is called. It:

1. Fetches the Gemini API key and immediately configures the Google AI library with it using genai.configure(api_key=...).
2. Fetches dynamic, just-in-time MongoDB credentials and stores them in a global variable named mongodb_credentials.

The result is that no secrets ever touch the disk. The API key and database credentials exist only in the application's memory, where they are used directly by the agent's tools. This "secretless" approach significantly enhances security by eliminating static, stored credentials.

```python Phyton
def create_agent():
    """Create the agent with proper credential handling"""
    try:
        # Call the ignition sequence
        if not initialize_credentials():
            print("Failed to initialize credentials.")
        
        root_agent = Agent(
            model='gemini-2.5-flash',
            name='secretless_agent',
            instruction="""You are a helpful assistant...
            All credentials are fetched dynamically from Akeyless CLI.
            MongoDB credentials are from dynamic secrets (preferred).""",
            tools=[
                get_current_time, 
                query_mongodb_database, # Uses the dynamic creds
                list_mongodb_collections, # Uses the dynamic creds
                refresh_mongodb_credentials # Flushes and gets NEW dynamic creds
            ],
        )
        print("Agent created successfully!")
        return root_agent
    ...

```

### Example: The Agent in Action

With the secretless_agent now running, it can use the tools defined in its create_agent function. These tools, like list_mongodb_collections, transparently use the dynamic, in-memory MongoDB credentials that were fetched during initialization.

Here is an example of that exact interaction:

<Image border={false} src="https://files.readme.io/823f5394e1c484e67422caa038a06011ee7db9c2a24d70cda7486c715bb612a5-ba532c6c-403e-4f73-8425-313c6f7f7439.png" />

<br />

### Conclusion: The Future is Ephemeral

The architecture we've explored isn't just a theoretical workaround; it's a practical, robust solution to the security risks inherent in powerful AI agents. Traditional methods leave static, long-lived credentials like database passwords and API keys as ticking time bombs on a server. If compromised, it's game over.

By contrast, the "dynamic-only" model empowers the agent to start with zero secrets. It leverages its native cloud identity (GCP IAM) to prove who it is. Based on this identity, it fetches its Gemini API key and loads it directly into the Google client's configuration in memory, bypassing environment variables entirely. More critically, it dynamically generates database credentials that are valid for only a few minutes.

This means the agent's most sensitive secrets, its database access simply do not exist until the exact moment of execution and are gone before an attacker can find them. This shift from protecting static secrets to eliminating them entirely results in a far more resilient and auditable system.

The benefits of this approach are profound:

* Zero Trust for Secrets: The application trusts nothing at startup. It proves its identity to fetch what it needs.
* No Static Database Passwords: This is the biggest win. There is no long-lived database password to steal. You can't leak what doesn't exist.
* Dramatically Reduced Attack Surface: An attacker who compromises the machine finds no keys, no .env files, and no credentials. By the time they start scanning, any in-memory credentials have already expired.
* Fully Auditable: Every time the agent fetches a key or generates a credential, it creates an audit log in Akeyless. You have a complete, real-time record of all secret access.

By building our agents this way, we move from a defensive security model (protecting secrets) to a proactive one (eliminating them entirely).