#!/usr/bin/env python3
"""
简单的API筛选测试
"""
import requests
import json

def test_screen():
    url = "http://localhost:8000/api/screen"
    payload = {
        "criteria": "帮我找市盈率低于20的银行股",
        "max_results": 3,
        "max_stocks_to_analyze": 10
    }

    print("=" * 50)
    print("测试 AI 股票筛选功能")
    print("=" * 50)
    print(f"\n筛选条件: {payload['criteria']}")
    print(f"最多返回: {payload['max_results']} 只股票")
    print(f"分析数量: {payload['max_stocks_to_analyze']} 只股票\n")
    print("发送请求中...")

    try:
        response = requests.post(url, json=payload, timeout=30)
        print(f"\n响应状态: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print("\n" + "=" * 50)
            print("筛选结果")
            print("=" * 50)

            if data.get('success'):
                print(f"\n✅ 成功找到 {len(data.get('stocks', []))} 只股票\n")

                for i, stock in enumerate(data.get('stocks', []), 1):
                    print(f"{i}. {stock.get('name')} ({stock.get('code')})")
                    print(f"   评分: {stock.get('score')}/100")
                    print(f"   理由: {stock.get('reason')}\n")

                print("分析总结:")
                print(data.get('analysis', ''))
                print("\n风险提示:")
                print(data.get('risk_warning', ''))
            else:
                print(f"\n❌ 筛选失败: {data.get('error', '未知错误')}")
                print(f"\n返回信息: {data.get('analysis', '')}")
        else:
            print(f"❌ 请求失败: {response.text}")

    except Exception as e:
        print(f"❌ 发生错误: {e}")
        print("\n注意: 此功能需要配置有效的 DeepSeek API Key")

if __name__ == "__main__":
    test_screen()
