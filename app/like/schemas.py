from pydantic import BaseModel


class LikeSchema(BaseModel):
    id: int
    user_id: int
    post_id: int
    vote: int

    class Config:
        orm_mode = True


class SetLikeSchema(BaseModel):
    post_id: int
    vote: int = 1 or -1
