"""
FastAPI 主应用
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from .config import get_settings
from .stock_data import StockDataFetcher
from .ai_screener import AIStockScreener

# 创建FastAPI应用
app = FastAPI(
    title="DeepSeek AI 炒股平台",
    description="使用DeepSeek AI帮助筛选A股股票",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化
settings = get_settings()
stock_fetcher = StockDataFetcher()
ai_screener = AIStockScreener()


# 数据模型
class ScreenRequest(BaseModel):
    """股票筛选请求"""
    criteria: str
    max_results: int = 10
    max_stocks_to_analyze: int = 100


class ChatRequest(BaseModel):
    """股票问答请求"""
    stock_code: str
    question: str


# API 路由
@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "欢迎使用 DeepSeek AI 炒股平台",
        "version": "1.0.0",
        "endpoints": {
            "股票列表": "/api/stocks",
            "AI筛选": "/api/screen",
            "股票问答": "/api/chat"
        }
    }


@app.get("/api/stocks")
async def get_stocks(limit: int = 100):
    """
    获取A股股票列表
    """
    try:
        stocks = stock_fetcher.get_stocks_summary(max_count=limit)
        return {
            "success": True,
            "count": len(stocks),
            "stocks": stocks
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取股票列表失败: {str(e)}")


@app.post("/api/screen")
async def screen_stocks(request: ScreenRequest):
    """
    AI 股票筛选
    """
    try:
        # 获取股票数据
        stocks = stock_fetcher.get_stocks_summary(max_count=request.max_stocks_to_analyze)

        if not stocks:
            raise HTTPException(status_code=500, detail="获取股票数据失败")

        # AI筛选
        result = ai_screener.screen_stocks(
            stocks=stocks,
            criteria=request.criteria,
            max_results=request.max_results
        )

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"筛选失败: {str(e)}")


@app.post("/api/chat")
async def chat_about_stock(request: ChatRequest):
    """
    关于股票的问答
    """
    try:
        answer = ai_screener.chat_about_stock(
            stock_code=request.stock_code,
            question=request.question
        )
        return {
            "success": True,
            "stock_code": request.stock_code,
            "question": request.question,
            "answer": answer
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"问答失败: {str(e)}")


@app.get("/api/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "api_configured": bool(settings.deepseek_api_key)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.debug
    )
