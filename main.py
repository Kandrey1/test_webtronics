from app import create_app

from app.auth import router as auth_router
from app.post import router as post_router
from app.like import router as like_router


app = create_app()


app.include_router(auth_router.router)
app.include_router(post_router.router)
app.include_router(like_router.router)


@app.get("/", tags=['Home page'])
async def home():
    return {"message": "Welcome Home page Testing task"}
