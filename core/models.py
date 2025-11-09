from pydantic import BaseModel
from datetime import datetime
# We don't need 'typing' here since these are just class definitions

# --- DataDog Models ---
class DatadogAlert(BaseModel):
    id: str
    name: str
    service_tag: str
    start_time: datetime

# --- GitHub Models ---
class GitHubCommit(BaseModel):
    sha: str
    message: str
    author: str

class GitHubDeployment(BaseModel):
    id: str
    commit: GitHubCommit # This nests the commit model inside the deployment
    actor: str
    finish_time: datetime