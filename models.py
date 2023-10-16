from pydantic import BaseModel

class InputData(BaseModel):
    metrics: list
    users: list
