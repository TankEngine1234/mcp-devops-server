import asyncio
from datetime import datetime, timedelta

# Import our config and models
from core.config import Settings, get_settings
from core.models import DatadogAlert, GitHubDeployment
from fastapi import Depends 

# Import the MOCKS
from connectors.mock import MockDatadogConnector, MockGitHubConnector
# Import the Formatter
from .formatter import format_failure_context

class CorrelationEngine:
    def __init__(self, datadog, github, launchdarkly): # <-- CHANGE 1: Added launchdarkly
        # The connectors are "injected"
        self.datadog = datadog
        self.github = github
        self.launchdarkly = launchdarkly # <-- CHANGE 1 (cont.)

    async def find_failure_cause(self, service_name: str) -> str:
        alert = await self.datadog.get_active_alert(f"service:{service_name}")
        
        if not alert:
            return f"CONTEXT: No active alerts found for '{service_name}'."
        
        window_start = alert.start_time - timedelta(minutes=15)
        window_end = alert.start_time + timedelta(minutes=5)
        
        print(f"ENGINE: Correlating events for '{service_name}' between {window_start} and {window_end}...")
        
        # --- CHANGE 2: Call all 3 connectors in parallel ---
        (deployments_results, flag_results) = await asyncio.gather(
            self.github.get_deployments_in_window(
                repo=f"my-org/{service_name}", 
                start=window_start, 
                end=window_end
            ),
            self.launchdarkly.get_flag_changes_in_window(
                project_key=f"{service_name}-project", # (Guessing a project key)
                start=window_start,
                end=window_end
            )
        )
        
        correlation_data = {
            "alert": alert,
            "deployments": deployments_results,
            "flags": flag_results # <-- Pass the flag results
        }
        
        return format_failure_context(correlation_data)


# --- Dependency Injection ---
def get_correlation_engine(settings: Settings = Depends(get_settings)):
    if settings.USE_MOCK:
        # We'd need to add a MockLaunchDarklyConnector to mock.py
        # For now, we'll just focus on the "real" path
        engine = CorrelationEngine(
            datadog=MockDatadogConnector(),
            github=MockGitHubConnector(),
            launchdarkly=None # (Mock not built yet)
        )
    else:
        # --- CHANGE 3: Load the real LaunchDarkly connector ---
        from connectors.datadog import DatadogConnector
        from connectors.github import GitHubConnector
        from connectors.launchdarkly import LaunchDarklyConnector # <-- Import it
        
        engine = CorrelationEngine(
            datadog=DatadogConnector(api_key=settings.DATADOG_API_KEY),
            github=GitHubConnector(token=settings.GITHUB_TOKEN),
            launchdarkly=LaunchDarklyConnector(api_key=settings.LAUNCHDARKLY_API_KEY) # <-- Init it
        )
    return engine