import streamlit as st
import httpx
import json

# --- Page Config ---
st.set_page_config(
    page_title="Code Red MCP Demo",
    layout="wide"
)

# --- App Title ---
st.title("🤖 'Code Red' DevOps Assistant")
st.markdown("This demo shows how an MCP server (your backend) injects real-time context to help an AI.")

# --- The "Magic" ---
# This is the function that calls your FastAPI server
def get_context_package(query):
    """Calls your FastAPI MCP server's /analyze endpoint."""
    url = "http://127.0.0.1:8000/analyze"
    try:
        response = httpx.post(url, json={"query": query})
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error from MCP Server: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Failed to connect to MCP Server. Is it running? \n{e}")
        return None

# --- UI Layout ---
col1, col2 = st.columns(2)

# --- COLUMN 1: The "Dumb" AI (Before) ---
with col1:
    st.header("1. The 'Dumb' AI (Before)")
    st.markdown("Without your MCP server, the AI has no context.")
    
    query = "Why is 'auth-service' failing?"
    
    st.text_input("User Query:", value=query, disabled=True)
    st.markdown("---")
    
    st.subheader("Final AI Prompt (No Context)")
    st.code(f"""
User: {query}
Assistant:
    """, language="text")

    st.subheader("AI Response (Useless)")
    st.error("I'm sorry, I don't have access to your live system status or deployment logs. I cannot tell you why 'auth-service' is failing.")

# --- COLUMN 2: The "Smart" AI (After) ---
with col2:
    st.header("2. The 'Smart' AI (After)")
    st.markdown("Your MCP server intercepts the query and injects context.")
    
    st.text_input("User Query (MCP Intercepts):", value=query, disabled=True, key="query2")
    st.markdown("---")

    # The button to run your demo
    if st.button("🚨 Run 'Code Red' Analysis"):
        with st.spinner("MCP Server is correlating events..."):
            # This is where you call your FastAPI backend!
            data = get_context_package(query)
            
            if data:
                context_package = data.get("context_package", "Error: No context package found.")
                
                st.subheader("Final AI Prompt (WITH Context)")
                st.code(f"""
{context_package}

User: {query}
Assistant:
                """, language="text")

                st.subheader("AI Response (Helpful!)")
                st.success(
                    "The 'auth-service' alert started at 2:28 PM. "
                    "This seems to be caused by deployment `#dep_abc123` by 'jane.doe', "
                    "which finished just 2 minutes earlier. I recommend investigating that commit."
                )