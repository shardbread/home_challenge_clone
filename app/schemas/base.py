from pydantic import BaseModel


class BaseDBSchema(BaseModel):
    class Config:
        orm_mode = True
