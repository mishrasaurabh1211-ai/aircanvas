from pathlib import Path

import yaml

from aircanvas.common.config import BaseConfig, load_config


def test_load_config_default_values(tmp_path: Path) -> None:
    config_data = {
        "resolution": {"width": 1280, "height": 720},
        "fps": 30,
        "mirror_webcam": True
    }
    config_file = tmp_path / "test_config.yaml"
    with open(config_file, "w", encoding='utf-8') as f:
        yaml.dump(config_data, f)
        
    config = load_config(config_file, BaseConfig)
    
    assert config.resolution.width == 1280
    assert config.resolution.height == 720
    assert config.fps == 30
    assert config.mirror_webcam is True