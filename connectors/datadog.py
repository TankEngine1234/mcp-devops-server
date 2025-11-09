from datetime import datetime, timedelta
from typing import Optional
from core.models import DatadogAlert

class DatadogConnector:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        print("--- REAL DATADOG: Connector loaded (but is a dummy).")

    async def get_active_alert(self, service_tag: str) -> Optional[DatadogAlert]:
        
        print(f"--- REAL DATADOG: Searching for alerts (dummy).")
        
        # --- THIS IS THE CHANGE ---
        # We will now return a FAKE alert to trigger the rest of the engine.
        print("--- REAL DATADOG: FAKE ALERT FOUND! Triggering correlation...")
        return DatadogAlert(
            id="fake-alert-123",
            name="Fake High Error Rate",
            service_tag=service_tag,
            start_time=datetime.utcnow() - timedelta(minutes=5)
        )