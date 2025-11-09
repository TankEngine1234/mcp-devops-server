# MCP Challenge: The "Code Red" DevOps Assistant

[![Language](https://img.shields.io/badge/Language-Python-blue.svg)](https://www.python.org)
[![Framework](https://img.shields.io/badge/Framework-FastAPI-green.svg)](https://fastapi.tiangolo.com/)
[![Showcase](https://img.shields.io/badge/Showcase-Streamlit-red.svg)](https://streamlit.io/)

When production fails, the on-call engineer is in a panic. The only question that matters is **"What changed?"**

The "Code Red" Assistant is a Model Context Protocol (MCP) server built to answer that question in seconds. It acts as a "smart context engine" that finds the "needle in the haystack" by correlating production alerts with the exact code deployments and feature flags that caused them.

---

## The Demo: Before vs. After

The easiest way to see the project's value is to run the interactive Streamlit showcase. It demonstrates the "dumb" AI (before) vs. the "smart" AI (after) powered by our MCP server.



### How to Run the Demo:
1.  **Terminal 1 (Backend):** Start the MCP server.
    ```bash
    # (Activate your venv first: source venv/bin/activate)
    uvicorn main:app --reload
    ```
2.  **Terminal 2 (Frontend):** Run the Streamlit showcase.
    ```bash
    # (Activate your venv first: source venv/bin/activate)
    streamlit run showcase.py
    ```

---

## The "Smart Context" Core

This project is a perfect example of the judging criteria: **Contextual Intelligence**, **Clever Integration**, and **Efficiency (Signal vs. Noise)**.

### The Problem (The "Dumb" AI)

Without our server, an AI is useless in an outage.

* **Query:** "Why is the 'auth-service' failing?"
* **AI Response:** "I'm sorry, I don't have access to your live system status or deployment logs."

### The Solution (The "Smart" AI)

Our MCP server intercepts the query and performs its "smart context" retrieval:

1.  **(Infer Context):** The server's **Correlation Engine** infers that the user needs the *cause* of the failure.
2.  **(Combine Sources):** It fetches the alert time from **Datadog**, then searches **GitHub** and **LaunchDarkly** for any events that happened in the 15 minutes leading up to the alert.
3.  **(Clever Integration):** The "magic" is the **correlation**. The server finds the direct link between the alert and the specific deployment that caused it.
4.  **(High-Signal Context):** It assembles a **high-signal, low-noise** context package, filtering out thousands of irrelevant logs to provide only the critical information.

The server then injects this "context package" into the prompt, unlocking the AI's true potential:

**Final Prompt Sent to the AI:**
**AI Response:** "The outage on 'auth-service' started at 2:10 PM. This directly correlates with a deployment by 'jane.doe' and a feature flag toggle. I recommend investigating that commit or rolling back the flag."

---

## Technology Stack

* **Language:** **Python**
* **Backend:** **FastAPI** (for the high-speed, asynchronous MCP server)
* **Frontend:** **Streamlit** (for the interactive showcase)
* **Server:** **Uvicorn**
* **Data Validation:** **Pydantic**
* **HTTP Client:** **httpx**
* **Data Sources (APIs):** **GitHub** (Live), **Datadog** (Simulated), **LaunchDarkly** (Simulated)

---

## How to Run It (Full Setup)

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/TankEngine1234/mcp-devops-server.git](https://github.com/TankEngine1234/mcp-devops-server.git)
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

4.  **Set up API Keys (Optional):**
    The project runs out-of-the-box with `USE_MOCK=True` in the `.env` file. No keys are needed to run the demo.
    
    If you want to add your own keys, copy `.env.example` to `.env` and set `USE_MOCK=False`.

5.  **Run the Backend & Frontend:**
    * **Terminal 1 (Backend):** `uvicorn main:app --reload`
    * **Terminal 2 (Frontend):** `streamlit run showcase.py`

---

## Testing the API Endpoint (Manual)

If you want to bypass the UI and test the `curl` endpoint directly:

```bash
curl -X POST "[http://127.0.0.1:8000/analyze](http://127.0.0.1:8000/analyze)" \
-H "Content-Type: application/json" \
-d '{"query": "Why is 'auth-service' failing?"}'