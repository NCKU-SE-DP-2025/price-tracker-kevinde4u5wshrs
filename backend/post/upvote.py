from ..database import app
from ..Loginverification import Loginverification
from ..models import user_news_association_table

from fastapi import APIRouter, Depends
from sqlalchemy import delete, insert, select

routes=APIRouter()
@app.post("/api/v1/news/{id}/upvote")
def upvote_article(
        id,
        db=Depends(Loginverification.session_opener),
        u=Depends(Loginverification.authenticate_user_token),
):
    message = toggle_upvote(id, u.id, db)
    return {"message": message}

def toggle_upvote(n_id, u_id, db):
    existing_upvote = db.execute(
        select(user_news_association_table).where(
            user_news_association_table.c.news_articles_id == n_id,
            user_news_association_table.c.user_id == u_id,
        )
    ).scalar()

    if existing_upvote:
        delete_stmt = delete(user_news_association_table).where(
            user_news_association_table.c.news_articles_id == n_id,
            user_news_association_table.c.user_id == u_id,
        )
        db.execute(delete_stmt)
        db.commit()
        return "Upvote removed"
    else:
        insert_stmt = insert(user_news_association_table).values(
            news_articles_id=n_id,
            user_id=u_id
        )
        db.execute(insert_stmt)
        db.commit()
        return "Article upvoted"