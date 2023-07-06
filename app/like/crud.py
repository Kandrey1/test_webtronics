from sqlalchemy.orm import Session
from .. import base_crud
from ..exceptions import LikeDenied
from ..post.models import Post
from .models import LikePost


async def set_vote_post(db: Session, user_id: int, data: dict):
    """
    Устанавливает голос (like/dislike).
    """
    post = await base_crud.get_record(db=db,
                                      table=Post,
                                      record_id=data['post_id'])

    if post.user_id == user_id:
        raise LikeDenied

    like = db.query(LikePost).filter(LikePost.user_id == user_id,
                                     LikePost.post_id == data['post_id']).first()

    data.update({"user_id": user_id})

    if not like:
        vote_like = await base_crud.create_record(db=db,
                                                  table=LikePost,
                                                  data=data)
    else:
        vote_like = await base_crud.update_record(db=db,
                                                  table=LikePost,
                                                  record_id=like.id,
                                                  data=data)

    return vote_like
