from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app import security
from logger_app import logger
from . import crud
from .schemas import SetLikeSchema
from ..auth.services import get_current_user
from ..database import get_db
from ..exceptions import AccessDenied, RecordNotExistDb, LikeDenied

router = APIRouter(prefix='/like',
                   tags=['Vote (Like / DisLike)'])


@router.post('/post')
async def set_vote_post(data_like: SetLikeSchema,
                        db: Session = Depends(get_db),
                        token: HTTPAuthorizationCredentials = Depends(security)):

    """
    Устанавливает like/dislike для статьи от текущего пользователя.

    vote : 1  (это like)

    vote : -1  (это dislike)
    """
    try:
        current_user = await get_current_user(db=db, token=token.credentials)
        data = dict(data_like)
        vote = await crud.set_vote_post(db=db,
                                        user_id=current_user.id,
                                        data=data)
    except LikeDenied:
        raise HTTPException(status_code=202,
                            detail='Вы не можете голосовать за свои статьи')

    except AccessDenied:
        raise HTTPException(status_code=403, detail='Доступ запрещен')

    except RecordNotExistDb:
        raise HTTPException(status_code=404, detail='Такой статьи нет')

    except SQLAlchemyError as e_db:
        logger.error(f'DB: {e_db}')
        raise HTTPException(status_code=500, detail='БД недоступна')

    except Exception as e:
        logger.error(f'Exception: {e}')
        raise HTTPException(status_code=500,
                            detail='Ошибка на сервере, '
                                   'обратитесь к администратору')

    return vote
