# MCP Challenge: The "Code Red" DevOps Assistant

This is a Model Context Protocol (MCP) server built for the Build-Your-Own-MCP Challenge. It acts as a "smart context engine" for an on-call developer to find the cause of a production outage instantly.

When a service is down, the most important question is **"What changed?"** This server finds the answer by correlating alerts, code deployments, and feature flag changes.

---

##  Purpose

* **Query:** "Why is the 'auth-service' failing?"
* **MCP Server Action:**
    1.  Connects to **Datadog** (dummy) to confirm the active alert.
    2.  Connects to **GitHub** (live) to find any code deployments that happened just before the alert.
    3.  Connects to **LaunchDarkly** (dummy) to find any feature flags that were toggled at the same time.
* **AI Response:** "The outage on 'auth-service' correlates with a deployment by 'jane.doe' and a feature flag toggle for 'new-signup-flow'. You should investigate the commit or roll back the flag."

## 🔌 Data Sources

* **Datadog:** (Simulated) For production monitoring alerts.
* **GitHub:** (Live) For code deployment and commit history.
* **LaunchDarkly:** (Simulated) For feature flag changes.

---

##  How to Run It

1.  **Clone the repository:**
    ```bash
    git clone [your-repo-link]
    cd mcp-devops-server
    ```

2.  **Create a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip3 install -r requirements.txt
    ```

4.  **Set up API Keys:**
    Create a `.env` file and add your API keys. (You can run the app in `USE_MOCK=True` mode without any keys).
    ```
    # Set to 'False' to use live (dummy) connectors
    USE_MOCK=False

    # --- Real API Keys ---
    GITHUB_TOKEN=ghp_...
    DATADOG_API_KEY=
    LAUNCHDARKLY_API_KEY=ld-api-...
    ```

5.  **Run the server:**
    ```bash
    uvicorn main:app --reload
    ```

6.  **Test the endpoint:**
    Open a new terminal and run the test command:
    ```bash
    curl -X POST "[http://127.0.0.1:8000/analyze](http://127.0.0.1:8000/analyze)" \
    -H "Content-Type: application/json" \
    -d '{"query": "Why is 'auth-service' failing?"}'
    ```

##  Example Prompts

* **Query:** `{"query": "Why is 'auth-service' failing?"}`
* **Result (Full Correlation):**
    ```json
    {
      "original_query": "Why is 'auth-service' failing?",
      "context_package": "CONTEXT: An alert 'Fake High Error Rate' on 'service:auth-service' started at [time].\n**Finding 1 (Deployment):** This correlates with deployment `#real_deploy_999` by 'real-user'...\n**Recommendation:** The recent deployment or feature flag change is the most likely cause."
    }
    ```