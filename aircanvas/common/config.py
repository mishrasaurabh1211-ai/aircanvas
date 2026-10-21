from pathlib import Path
from typing import TypeVar

import yaml
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

class ResolutionConfig(BaseModel):
    width: int
    height: int

class BaseConfig(BaseModel):
    resolution: ResolutionConfig
    fps: int
    mirror_webcam: bool

def load_config(path: str | Path, model_cls: type[T]) -> T:
    with open(path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return model_cls(**data)