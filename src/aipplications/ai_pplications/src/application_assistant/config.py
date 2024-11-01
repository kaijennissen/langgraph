from pathlib import Path

import yaml


def load_config():
    config_path = (
        Path(__file__).parent.parent.parent / "config/application_assistant_config.yaml"
    )
    with open(config_path, "r") as file:
        return yaml.safe_load(file)


CONFIG = load_config()
