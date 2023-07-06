from sqlalchemy import Column, Integer, UniqueConstraint, ForeignKey

from ..database import Base


class LikePost(Base):
    """
    Модель данных для голосования(like/dislike).

    post_id: адрес ссылки.
    user_id: описание
    vote: категория к которой относится ссылка.
    """
    __tablename__ = "like_post"

    __table_args__ = (
        UniqueConstraint('post_id', 'user_id', name='vote_post_user'),
    )

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    vote = Column(Integer)

    def __str__(self):
        return f"{self.id}: {self.post_id} - {self.vote}({self.user_id})"
