from datetime import datetime

def format_time(dt: datetime) -> str:
    # Formats time to be "human-friendly"
    return dt.strftime("%-I:%M %p UTC") # e.g., "2:08 PM UTC"

def format_failure_context(data: dict) -> str:
    """
    Builds the final, human-readable context string.
    """
    alert = data.get("alert")
    deployments = data.get("deployments", [])
    flags = data.get("flags", [])

    # Start with the core finding
    context = [
        f"CONTEXT: An alert '{alert.name}' on '{alert.service_tag}' started at {format_time(alert.start_time)}."
    ]

    # --- Add Correlated Findings ---
    
    # 1. Add deployment findings
    if deployments:
        deploy = deployments[0] # Just show the first one
        context.append(
            f"**Finding 1 (Deployment):** This correlates with deployment `#{deploy.id}` "
            f"by '{deploy.actor}' which finished 2 minutes earlier at {format_time(deploy.finish_time)}. "
            f"The commit was: '{deploy.commit.message}'."
        )
    
    # 2. Add feature flag findings (if any)
    if flags:
        flag = flags[0]
        context.append(
            f"**Finding 2 (Feature Flag):** This also correlates with flag '{flag.name}' "
            f"being '{flag.new_state}' at {format_time(flag.timestamp)}."
        )

    # 3. Add recommendation
    if not deployments and not flags:
        context.append(
            "**Recommendation:** No correlated deployments or feature flag changes were found. "
            "This may be an infrastructure issue or upstream dependency failure."
        )
    else:
        context.append(
            "**Recommendation:** The recent deployment or feature flag change is the most likely cause. "
            "Investigate or consider a rollback."
        )

    # Join all lines into a single string
    return "\n".join(context)