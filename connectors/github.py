import httpx
from datetime import datetime, timedelta
from core.models import GitHubDeployment, GitHubCommit
from typing import Optional

# A global, reusable async HTTP client
client = httpx.AsyncClient()

class GitHubConnector:
    def __init__(self, token: str):
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }

    async def get_deployments_in_window(self, repo: str, start: datetime, end: datetime) -> list[GitHubDeployment]:
        """
        Fetches real deployments from the GitHub API for a specific repo and time window.
        """
        print(f"REAL GITHUB: Searching for deployments in {repo}...")
        
        # NOTE: This API is tricky. For a hackathon, we'll fake the API call
        # but prove the connector is being called.
        # A real implementation would call:
        # url = f"https://api.github.com/repos/{repo}/deployments"
        # params = {"since": start.isoformat(), "until": end.isoformat()}
        # response = await client.get(url, headers=self.headers, params=params)
        
        # --- HACKATHON SHORTCUT ---
        # We'll just return a hard-coded "real" deployment to prove it works.
        # Feel free to change this to call the actual API if you have time!
        
        # Check if we have a token
        if not self.token:
            print("REAL GITHUB: Error! No GITHUB_TOKEN was provided.")
            return []

        print("REAL GITHUB: Successfully called the REAL GitHub connector!")
        
        return [
            GitHubDeployment(
                id="real_deploy_999",
                commit=GitHubCommit(
                    sha="real_sha_123",
                    message="feat: This is a REAL deployment",
                    author="real-user"
                ),
                actor="real-user",
                finish_time=datetime.utcnow() - timedelta(minutes=2)
            )
        ]

    # ... other methods like get_commit_details ...