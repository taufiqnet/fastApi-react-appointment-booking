from fastapi import Form
from pydantic import BaseModel
import json

def form_body(cls: type[BaseModel]):
    def dependency(data: str = Form(...)) -> BaseModel:
        return cls(**json.loads(data))
    return dependency
