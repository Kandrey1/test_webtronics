from pydantic import BaseModel


class BasePostSchema(BaseModel):
    title: str
    text: str
    visible: bool
    user_id: int


class InputDataPostSchema(BaseModel):
    title: str
    text: str


class UpdateDataPostSchema(BaseModel):
    title: str
    text: str


class PostCreateSchema(BaseModel):
    pass


class PostSchema(BasePostSchema):
    id: int

    class Config:
        orm_mode = True
