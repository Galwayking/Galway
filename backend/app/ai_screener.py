"""
DeepSeek AI 股票筛选模块
"""
from openai import OpenAI
from typing import List, Dict, Optional
import json
from .config import get_settings


class AIStockScreener:
    """AI股票筛选器"""

    def __init__(self):
        settings = get_settings()
        self.client = OpenAI(
            api_key=settings.deepseek_api_key,
            base_url=settings.deepseek_base_url
        )
        self.model = "deepseek-chat"

    def screen_stocks(
        self,
        stocks: List[Dict],
        criteria: str,
        max_results: int = 10
    ) -> Dict:
        """
        使用AI筛选股票
        Args:
            stocks: 股票列表
            criteria: 筛选条件（自然语言）
            max_results: 最多返回结果数
        Returns:
            筛选结果
        """
        try:
            # 构建系统提示
            system_prompt = self._build_system_prompt()

            # 构建用户提示
            user_prompt = self._build_user_prompt(stocks, criteria, max_results)

            # 调用DeepSeek API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=4000
            )

            # 解析响应
            result = self._parse_response(response.choices[0].message.content)
            return result

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "stocks": [],
                "analysis": "AI筛选失败，请检查API配置或稍后重试"
            }

    def _build_system_prompt(self) -> str:
        """构建系统提示"""
        return """你是一位专业的A股市场分析师，精通股票筛选和投资分析。

你的任务是根据用户提供的筛选条件，从股票列表中挑选出最符合条件的股票。

分析时请考虑以下因素：
1. 基本面指标：市盈率(PE)、市净率(PB)、市值等
2. 技术面指标：价格、涨跌幅、成交量、换手率等
3. 行业特征和市场环境
4. 风险收益比

请以JSON格式返回结果，格式如下：
{
    "stocks": [
        {
            "code": "股票代码",
            "name": "股票名称",
            "score": 评分(0-100),
            "reason": "选择理由"
        }
    ],
    "analysis": "整体分析总结",
    "risk_warning": "风险提示"
}

注意：
- 只返回JSON格式，不要有其他文字
- 评分要客观，不要都给高分
- 理由要具体，结合数据说明
- 必须包含风险提示
"""

    def _build_user_prompt(
        self,
        stocks: List[Dict],
        criteria: str,
        max_results: int
    ) -> str:
        """构建用户提示"""
        # 简化股票数据，只保留关键信息
        stocks_data = []
        for stock in stocks:
            stocks_data.append({
                "代码": stock.get("code"),
                "名称": stock.get("name"),
                "最新价": stock.get("price"),
                "涨跌幅": stock.get("change_pct"),
                "换手率": stock.get("turnover_rate"),
                "市盈率": stock.get("pe_dynamic"),
                "市净率": stock.get("pb"),
                "总市值": stock.get("market_cap"),
            })

        prompt = f"""
请根据以下条件筛选股票：

【筛选条件】
{criteria}

【股票数据】
共{len(stocks_data)}只股票
{json.dumps(stocks_data[:100], ensure_ascii=False, indent=2)}

【要求】
- 请从以上股票中选出最符合条件的 {max_results} 只股票
- 按匹配度排序，最符合的排在前面
- 给出评分和详细理由
- 提供整体分析和风险提示

请严格按照JSON格式返回结果。
"""
        return prompt

    def _parse_response(self, response_text: str) -> Dict:
        """解析AI响应"""
        try:
            # 尝试解析JSON
            # 清理可能的markdown代码块标记
            response_text = response_text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]

            result = json.loads(response_text.strip())

            return {
                "success": True,
                "stocks": result.get("stocks", []),
                "analysis": result.get("analysis", ""),
                "risk_warning": result.get("risk_warning", "投资有风险，入市需谨慎")
            }
        except json.JSONDecodeError:
            # 如果解析失败，返回原始文本
            return {
                "success": False,
                "error": "解析AI响应失败",
                "stocks": [],
                "analysis": response_text,
                "risk_warning": "投资有风险，入市需谨慎"
            }

    def chat_about_stock(self, stock_code: str, question: str) -> str:
        """
        关于特定股票的问答
        Args:
            stock_code: 股票代码
            question: 用户问题
        Returns:
            AI回答
        """
        try:
            prompt = f"""
用户问题：{question}
股票代码：{stock_code}

请基于专业知识回答用户关于该股票的问题。
注意：这只是分析参考，不构成投资建议。
"""
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一位专业的股票分析师"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"AI回答失败: {str(e)}"
