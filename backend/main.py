from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler

from get.me import routes as me_routes
from get.price import routes as price_routes
from get.news import routes as news_routes
from get.usernews import routes as usernews_routes
from post.login import routes as login_routes
from post.summary import routes as summary_routes
from post.search import routes as search_routes
from post.register import routes as register_routes
from post.upvote import routes as upvote_routes
from database import Base, engine, bgs, SessionLocal
from NewsService import NewsService
from models import NewsArticle

# 建立資料表
Base.metadata.create_all(bind=engine)

# 建立 FastAPI app
app = FastAPI()

# include 各路由
app.include_router(me_routes)
app.include_router(price_routes)
app.include_router(news_routes)
app.include_router(usernews_routes)
app.include_router(login_routes)
app.include_router(summary_routes)
app.include_router(search_routes)
app.include_router(register_routes)
app.include_router(upvote_routes)


@app.on_event("startup")
def start_scheduler():
    db = SessionLocal()
    news_service = NewsService(db_session=db, ai_api_key="xxx")  # 建立實例

    # 如果資料庫沒新聞，先抓一次
    if db.query(NewsArticle).count() == 0:
        news_service.get_new()  # 用實例方法呼叫

    # 排程每 100 分鐘抓新聞
    bgs.add_job(news_service.get_new, "interval", minutes=100)
    bgs.start()
    db.close()

@app.on_event("shutdown")
def shutdown_scheduler():
    bgs.shutdown()
