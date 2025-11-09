"""
应用配置管理
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """应用配置"""

    # DeepSeek API
    deepseek_api_key: str = ""
    deepseek_base_url: str = "https://api.deepseek.com"

    # 应用设置
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    debug: bool = True

    # 股票筛选设置
    default_market: str = "A股"
    max_stocks_return: int = 50

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """获取配置单例"""
    return Settings()
