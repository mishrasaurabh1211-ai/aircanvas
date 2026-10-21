from pydantic import BaseModel


class ButtonConfig(BaseModel):
    id: str
    x: int
    y: int
    w: int
    h: int
    color: tuple[int, int, int]


class UIConfig(BaseModel):
    buttons: list[ButtonConfig]