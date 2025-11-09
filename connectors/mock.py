import asyncio
from datetime import datetime, timedelta
from core.models import DatadogAlert, GitHubDeployment, GitHubCommit
from typing import Optional 

# --- Mock Datadog ---
class MockDatadogConnector:
    async def get_active_alert(self, service_tag: str) -> Optional[DatadogAlert]: 
        print(f"MOCK DATADOG: Checking alerts for {service_tag}")
        await asyncio.sleep(0.1) # Simulate network lag
        
        # --- THIS IS THE FIX ---
        if service_tag == "service:auth-service": # <--- IT NOW MATCHES THE ENGINE
            return DatadogAlert(
                id="12345",
                name="High 5xx Error Rate",
                service_tag=service_tag,
                start_time=datetime.utcnow() - timedelta(minutes=5) 
            )
        return None

# --- Mock GitHub ---
class MockGitHubConnector:
    async def get_deployments_in_window(self, repo: str, start: datetime, end: datetime) -> list[GitHubDeployment]:
        print(f"MOCK GITHUB: Searching for deployments in {repo}...")
        await asyncio.sleep(0.2) # Simulate network lag
        
        deploy_time = datetime.utcnow() - timedelta(minutes=7) 
        
        return [
            GitHubDeployment(
                id="dep_abc123",
                commit=GitHubCommit(
                    sha="a1b2c3d4",
                    message="fix: resolve login edge case",
                    author="jane.doe"
                ),
                actor="jane.doe",
                finish_time=deploy_time
            )
        ]