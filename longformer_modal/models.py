from pydantic import BaseModel


class ParseArgument(BaseModel):
    text: str
    api_key: str
