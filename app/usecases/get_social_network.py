import json
import re
from pathlib import Path


def get_social_networks():
    social_networks_file = Path("app") / "resources" / "social_networks.json"

    if not social_networks_file.exists():
        raise FileNotFoundError("File with social networks not found")

    social_networks = json.loads(social_networks_file.read_text())
    return social_networks


def get_social_network(url: str):
    domain = re.sub(r'^https?://', '', url)

    for social_network in get_social_networks():
        if domain.startswith(social_network):
            return social_network
    return None
