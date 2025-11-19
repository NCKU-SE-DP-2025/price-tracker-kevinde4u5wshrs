from database import NewsSumaryRequestSchema
from Loginverification import Loginverification


from fastapi import APIRouter,Depends
from openai import OpenAI
import json

routes=APIRouter()
@routes.post("/api/v1/news/news_summary")
async def news_summary(
        payload: NewsSumaryRequestSchema, u=Depends(Loginverification.authenticate_user_token)
):
    response = {}
    messages = [
        {
            "role": "system",
            "content": "你是一個新聞摘要生成機器人，請統整新聞中提及的影響及主要原因 (影響、原因各50個字，請以json格式回答 {'影響': '...', '原因': '...'})",
        },
        {
            "role": "user", 
            "content": f"{payload.content}"
        },
    ]

    completion = OpenAI(api_key="xxx").chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    result = completion.choices[0].message.content
    if result:
        result = json.loads(result)
        response["summary"] = result["影響"]
        response["reason"] = result["原因"]
    return response