"""
A股数据获取模块
使用 akshare 获取A股市场数据，如果不可用则使用模拟数据
"""
import pandas as pd
from typing import List, Dict, Optional
from datetime import datetime
import random

# 尝试导入 akshare，如果失败则使用模拟数据
try:
    import akshare as ak
    AKSHARE_AVAILABLE = True
except ImportError:
    AKSHARE_AVAILABLE = False
    print("⚠️  akshare 未安装，将使用模拟数据进行演示")


class StockDataFetcher:
    """A股数据获取器"""

    @staticmethod
    def _get_mock_stocks() -> pd.DataFrame:
        """
        生成模拟股票数据（用于演示）
        """
        mock_data = {
            '代码': ['600519', '000858', '600036', '601318', '000001', '002594', '600276', '000333', '601398', '601166'],
            '名称': ['贵州茅台', '五粮液', '招商银行', '中国平安', '平安银行', '比亚迪', '恒瑞医药', '美的集团', '工商银行', '兴业银行'],
            '最新价': [1680.5, 128.3, 35.6, 42.8, 12.5, 252.8, 56.7, 68.9, 5.2, 18.3],
            '涨跌幅': [2.5, -1.3, 0.8, 1.2, -0.5, 3.8, 0.2, -0.8, 0.1, 1.5],
            '成交量': [1234567, 2345678, 3456789, 4567890, 5678901, 6789012, 7890123, 8901234, 9012345, 1023456],
            '成交额': [207654321, 300123456, 123456789, 195678901, 71012345, 1709876543, 448901234, 617890123, 46789012, 18890123],
            '换手率': [0.5, 1.2, 2.3, 1.8, 3.5, 2.1, 0.8, 1.5, 4.2, 2.8],
            '市盈率-动态': [35.2, 25.8, 8.5, 12.3, 6.8, 45.6, 32.1, 15.4, 5.2, 7.8],
            '市净率': [12.5, 8.3, 1.2, 1.8, 0.8, 5.6, 4.5, 3.2, 0.7, 0.9],
            '总市值': [21000000000, 5000000000, 9500000000, 10800000000, 2400000000, 7300000000, 4500000000, 4800000000, 18500000000, 4700000000],
        }
        return pd.DataFrame(mock_data)

    @staticmethod
    def get_all_stocks() -> pd.DataFrame:
        """
        获取所有A股股票列表
        Returns:
            DataFrame with columns: 代码, 名称, 等
        """
        if not AKSHARE_AVAILABLE:
            return StockDataFetcher._get_mock_stocks()

        try:
            # 获取沪深A股列表
            stock_list = ak.stock_zh_a_spot_em()
            return stock_list
        except Exception as e:
            print(f"获取股票列表失败: {e}，使用模拟数据")
            return StockDataFetcher._get_mock_stocks()

    @staticmethod
    def get_stock_info(stock_code: str) -> Optional[Dict]:
        """
        获取单个股票的详细信息
        Args:
            stock_code: 股票代码
        Returns:
            股票信息字典
        """
        try:
            # 获取个股信息
            stock_individual = ak.stock_individual_info_em(symbol=stock_code)
            return stock_individual.to_dict() if not stock_individual.empty else None
        except Exception as e:
            print(f"获取股票 {stock_code} 信息失败: {e}")
            return None

    @staticmethod
    def get_stock_financial_analysis(stock_code: str) -> Optional[pd.DataFrame]:
        """
        获取股票财务分析数据
        Args:
            stock_code: 股票代码
        Returns:
            财务分析数据
        """
        try:
            # 获取财务分析数据
            financial_data = ak.stock_financial_analysis_indicator(symbol=stock_code)
            return financial_data
        except Exception as e:
            print(f"获取股票 {stock_code} 财务数据失败: {e}")
            return None

    @staticmethod
    def format_stock_for_ai(stock_row: pd.Series) -> str:
        """
        将股票数据格式化为AI可读的文本
        Args:
            stock_row: 股票数据行
        Returns:
            格式化的文本
        """
        try:
            return f"""
股票代码: {stock_row.get('代码', 'N/A')}
股票名称: {stock_row.get('名称', 'N/A')}
最新价: {stock_row.get('最新价', 'N/A')}
涨跌幅: {stock_row.get('涨跌幅', 'N/A')}%
涨跌额: {stock_row.get('涨跌额', 'N/A')}
成交量: {stock_row.get('成交量', 'N/A')}
成交额: {stock_row.get('成交额', 'N/A')}
振幅: {stock_row.get('振幅', 'N/A')}%
换手率: {stock_row.get('换手率', 'N/A')}%
市盈率动态: {stock_row.get('市盈率-动态', 'N/A')}
市净率: {stock_row.get('市净率', 'N/A')}
总市值: {stock_row.get('总市值', 'N/A')}
流通市值: {stock_row.get('流通市值', 'N/A')}
"""
        except Exception as e:
            print(f"格式化股票数据失败: {e}")
            return "数据格式化失败"

    @staticmethod
    def get_stocks_summary(max_count: int = 100) -> List[Dict]:
        """
        获取股票摘要信息（用于AI筛选）
        Args:
            max_count: 最多返回的股票数量
        Returns:
            股票摘要列表
        """
        try:
            df = StockDataFetcher.get_all_stocks()
            if df.empty:
                return []

            # 限制数量
            df = df.head(max_count)

            # 转换为字典列表
            stocks = []
            for _, row in df.iterrows():
                stock_dict = {
                    "code": str(row.get('代码', '')),
                    "name": str(row.get('名称', '')),
                    "price": float(row.get('最新价', 0)) if pd.notna(row.get('最新价')) else 0,
                    "change_pct": float(row.get('涨跌幅', 0)) if pd.notna(row.get('涨跌幅')) else 0,
                    "volume": float(row.get('成交量', 0)) if pd.notna(row.get('成交量')) else 0,
                    "amount": float(row.get('成交额', 0)) if pd.notna(row.get('成交额')) else 0,
                    "turnover_rate": float(row.get('换手率', 0)) if pd.notna(row.get('换手率')) else 0,
                    "pe_dynamic": float(row.get('市盈率-动态', 0)) if pd.notna(row.get('市盈率-动态')) else 0,
                    "pb": float(row.get('市净率', 0)) if pd.notna(row.get('市净率')) else 0,
                    "market_cap": float(row.get('总市值', 0)) if pd.notna(row.get('总市值')) else 0,
                }
                stocks.append(stock_dict)

            return stocks
        except Exception as e:
            print(f"获取股票摘要失败: {e}")
            return []
