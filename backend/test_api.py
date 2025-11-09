#!/usr/bin/env python3
"""
API 测试脚本
"""
import requests
import json

BASE_URL = "http://localhost:8000"


def test_health():
    """测试健康检查"""
    print("测试健康检查...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print(f"✅ 健康检查成功: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ 健康检查失败: {e}")
        return False


def test_get_stocks():
    """测试获取股票列表"""
    print("\n测试获取股票列表...")
    try:
        response = requests.get(f"{BASE_URL}/api/stocks?limit=10")
        data = response.json()
        print(f"✅ 获取股票列表成功，共 {data.get('count', 0)} 只股票")
        if data.get('stocks'):
            print(f"   示例：{data['stocks'][0].get('name')} ({data['stocks'][0].get('code')})")
        return True
    except Exception as e:
        print(f"❌ 获取股票列表失败: {e}")
        return False


def test_screen_stocks():
    """测试AI筛选"""
    print("\n测试AI筛选...")
    try:
        payload = {
            "criteria": "帮我找市盈率低于30的股票",
            "max_results": 5,
            "max_stocks_to_analyze": 50
        }
        response = requests.post(
            f"{BASE_URL}/api/screen",
            json=payload,
            timeout=60  # AI分析可能需要较长时间
        )
        data = response.json()

        if data.get('success'):
            print(f"✅ AI筛选成功，找到 {len(data.get('stocks', []))} 只股票")
            if data.get('stocks'):
                print(f"   最佳推荐：{data['stocks'][0].get('name')} - 评分 {data['stocks'][0].get('score')}")
            return True
        else:
            print(f"⚠️  AI筛选返回失败: {data.get('error', '未知错误')}")
            return False
    except Exception as e:
        print(f"❌ AI筛选失败: {e}")
        return False


def test_chat():
    """测试股票问答"""
    print("\n测试股票问答...")
    try:
        payload = {
            "stock_code": "000001",
            "question": "这只股票的基本情况如何？"
        }
        response = requests.post(
            f"{BASE_URL}/api/chat",
            json=payload,
            timeout=30
        )
        data = response.json()

        if data.get('success'):
            print(f"✅ 股票问答成功")
            print(f"   回答：{data.get('answer', '')[:100]}...")
            return True
        else:
            print(f"❌ 股票问答失败")
            return False
    except Exception as e:
        print(f"❌ 股票问答失败: {e}")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("DeepSeek AI 炒股平台 - API 测试")
    print("=" * 50)

    # 运行测试
    results = []
    results.append(("健康检查", test_health()))
    results.append(("获取股票列表", test_get_stocks()))

    # 提示：AI相关测试需要配置API Key
    print("\n" + "=" * 50)
    print("⚠️  以下测试需要配置 DeepSeek API Key")
    print("=" * 50)

    results.append(("AI筛选", test_screen_stocks()))
    results.append(("股票问答", test_chat()))

    # 总结
    print("\n" + "=" * 50)
    print("测试总结")
    print("=" * 50)

    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name}: {status}")

    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\n通过率: {passed}/{total} ({passed*100//total}%)")
