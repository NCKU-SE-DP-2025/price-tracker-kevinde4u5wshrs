import json
from sqlalchemy.orm import Session
from .models import NewsArticle
from openai import OpenAI
from bs4 import BeautifulSoup
from urllib.parse import quote
import requests


class NewsService:
    def __init__(self, db_session: Session, ai_api_key: str):
        """
        db_session: SQLAlchemy Session
        ai_api_key: OpenAI API Key
        """
        self.db = db_session
        self.ai_key = ai_api_key
        self.ai_client = OpenAI(api_key=self.ai_key)

    def add_new(self,news_data):
        """
        add new to db
        :param news_data: news info
        :return:
        """
        self.db.add(NewsArticle(
            url=news_data["url"],
            title=news_data["title"],
            time=news_data["time"],
            content=" ".join(news_data["content"]),  # 將內容list轉換為字串
            summary=news_data["summary"],
            reason=news_data["reason"],
        ))
        self.db.commit()
        self.db.close()


    def get_new_info(self,search_term, is_initial=False):
        """
        get new

        :param search_term:
        :param is_initial:
        :return:
        """
        all_news_data = []
        # iterate pages to get more news data, not actually get all news data
        if is_initial:
            for page in range(1, 10):
                params = {
                    "page": page,
                    "id": f"search:{quote(search_term)}",
                    "channelId": 2,
                    "type": "searchword",
                }
                response = requests.get("https://udn.com/api/more", params=params)

                all_news_data.append(response.json()["lists"])
                
        else:
            params = {
                "page": 1,
                "id": f"search:{quote(search_term)}",
                "channelId": 2,
                "type": "searchword",
            }
            response = requests.get("https://udn.com/api/more", params=params)

            all_news_data = response.json()["lists"]

        return all_news_data

    def evaluate_relevance(self,title: str) -> str:
        """使用 OpenAI 評估新聞標題是否與主題有關"""
        messages = [
            {
                "role": "system",
                "content": (
                    "你是一個關聯度評估機器人，請評估新聞標題是否與「民生用品的價格變化」相關，"
                    "並給予'high'、'medium'、'low'評價。(僅需回答'high'、'medium'、'low'三個詞之一)"
                ),
            },
            {"role": "user", "content": title},
        ]

        ai = OpenAI(api_key="xxx").chat.completions.create(
            model="gpt-3.5-turbo", 
            messages=messages,
        )
        return ai.choices[0].message.content.strip().lower()
    def process_news_article(self,news):
        response = requests.get(news["titleLink"])
        soup = BeautifulSoup(response.text, "html.parser")
        # 標題
        title = soup.find("h1", class_="article-content__title").text
        time = soup.find("time", class_="article-content__time").text
        # 定位到包含文章内容的 <section>
        content_section = soup.find("section", class_="article-content__editor")

        paragraphs = [
            p.text
            for p in content_section.find_all("p")
            if p.text.strip() != "" and "▪" not in p.text
        ]
        detailed_news =  {
            "url": news["titleLink"],
            "title": title,
            "time": time,
            "content": paragraphs,
        }
        messages = [
            {
                "role": "system",
                "content": "你是一個新聞摘要生成機器人，請統整新聞中提及的影響及主要原因 (影響、原因各50個字，請以json格式回答 {'影響': '...', '原因': '...'})",
            },
            {
                "role": "user", 
                "content": " ".join(detailed_news["content"])
            },
        ]

        completion = OpenAI(api_key="xxx").chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )
        result = completion.choices[0].message.content
        result = json.loads(result)
        detailed_news["summary"] = result["影響"]
        detailed_news["reason"] = result["原因"]
        self.add_new(detailed_news)
    def get_new(self,is_initial=False):
        """
        get new info

        :param is_initial:
        :return:
        """
        news_data = self.get_new_info("價格", is_initial=is_initial)
        for news in news_data:
            relevance =self.evaluate_relevance(news["title"])
            if relevance == "high":
                self.process_news_article(news)