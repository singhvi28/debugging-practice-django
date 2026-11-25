"""Deploy credential resolver."""

from dataclasses import dataclass

PRODUCTION_SECRET = "prod-deploy-key"
STAGING_SECRET = "staging-deploy-key"


@dataclass
class BuildContext:
    is_pull_request: bool
    is_fork: bool
    target_branch: str


def get_deploy_secret(context: BuildContext) -> str:
    if context.target_branch == "main":
        return PRODUCTION_SECRET
    return STAGING_SECRET
