from sqlalchemy import Column, Boolean, Integer, String, ForeignKey

from ..database import Base


class Post(Base):
    """
    Модель данных статьи.

    title: Заголовок статьи.
    text: Текст статьи.
    user_id: id автора.
    """
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    text = Column(String,  nullable=False)
    visible = Column(Boolean, default=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    def __str__(self):
        return f"{self.id} - {self.title}"
