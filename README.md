# 🤖 DeepSeek AI 炒股平台

一个使用 DeepSeek AI 帮助筛选 A股股票的智能平台。通过自然语言描述筛选条件，AI 会从数千只股票中为您挑选出最符合要求的股票。

## ✨ 功能特点

- **智能筛选**：用自然语言描述需求，AI 自动分析并筛选股票
- **实时数据**：基于 akshare 获取 A股实时行情数据
- **专业分析**：AI 提供详细的选股理由和风险提示
- **简洁界面**：直观的 Web 界面，易于使用
- **灵活配置**：可自定义筛选条件和返回结果数量

## 🏗️ 技术架构

- **后端**：Python + FastAPI
- **AI引擎**：DeepSeek API
- **数据源**：akshare（A股数据）
- **前端**：HTML + CSS + JavaScript

## 📋 系统要求

- Python 3.8+
- DeepSeek API Key
- 网络连接（获取股票数据）

## 🚀 快速开始

### 1. 获取 DeepSeek API Key

访问 [DeepSeek 官网](https://platform.deepseek.com/) 注册并获取 API Key。

### 2. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 3. 配置环境变量

复制环境变量模板：

```bash
cd backend
cp .env.example .env
```

编辑 `.env` 文件，填入您的 DeepSeek API Key：

```env
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=True
```

### 4. 启动后端服务

```bash
cd backend
python run.py
```

服务将在 `http://localhost:8000` 启动。

### 5. 访问前端界面

在浏览器中打开：

```
frontend/index.html
```

或者使用简单的 HTTP 服务器：

```bash
cd frontend
python -m http.server 3000
```

然后访问 `http://localhost:3000`

## 📖 使用说明

### AI 智能筛选

1. 在筛选条件框中用自然语言描述您的需求，例如：
   - "帮我找市盈率低于20，市净率低于3的科技股"
   - "筛选最近一个月涨幅在5%-15%之间的医药股"
   - "找出换手率高于5%，市值在100-500亿之间的成长股"

2. 设置返回结果数量和分析的股票总数

3. 点击"开始筛选"，等待 AI 分析

4. 查看筛选结果，包括：
   - 每只股票的评分（0-100分）
   - 详细的选择理由
   - 整体分析总结
   - 风险提示

### 市场概览

点击"加载股票列表"可以查看当前市场上的股票列表，包括实时价格、涨跌幅等信息。

## 🔧 API 接口

### 获取股票列表

```http
GET /api/stocks?limit=100
```

### AI 筛选股票

```http
POST /api/screen
Content-Type: application/json

{
  "criteria": "筛选条件",
  "max_results": 10,
  "max_stocks_to_analyze": 100
}
```

### 股票问答

```http
POST /api/chat
Content-Type: application/json

{
  "stock_code": "000001",
  "question": "这只股票怎么样？"
}
```

### 健康检查

```http
GET /api/health
```

## 📁 项目结构

```
.
├── backend/                # 后端服务
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py        # FastAPI 主应用
│   │   ├── config.py      # 配置管理
│   │   ├── stock_data.py  # 股票数据获取
│   │   └── ai_screener.py # AI 筛选逻辑
│   ├── requirements.txt   # Python 依赖
│   ├── .env.example       # 环境变量模板
│   └── run.py            # 启动脚本
├── frontend/              # 前端界面
│   ├── index.html        # 主页面
│   └── src/
│       ├── style.css     # 样式
│       └── app.js        # 交互逻辑
└── README.md
```

## 🎯 使用示例

### 示例 1：找价值股

筛选条件：
```
帮我找市盈率低于15，市净率低于2，ROE大于10%的价值股
```

### 示例 2：找成长股

筛选条件：
```
筛选最近一年营收增长超过30%，且市值在50-300亿之间的成长股
```

### 示例 3：找活跃股

筛选条件：
```
找出换手率高于8%，成交额超过10亿，且最近涨幅在5%-20%之间的活跃股
```

## ⚠️ 重要提示

1. **免责声明**：本平台仅供学习和研究使用，AI 分析结果仅供参考，不构成投资建议。投资有风险，入市需谨慎。

2. **数据准确性**：股票数据来自第三方数据源（akshare），可能存在延迟或误差。

3. **API 限制**：DeepSeek API 可能有调用频率限制，请合理使用。

4. **网络要求**：需要稳定的网络连接来获取股票数据和调用 AI 服务。

## 🔮 未来规划

- [ ] 添加历史回测功能
- [ ] 支持自定义筛选指标
- [ ] 添加股票详情页面
- [ ] 实现策略保存和分享
- [ ] 添加用户认证系统
- [ ] 支持港股、美股市场
- [ ] 移动端适配
- [ ] 实时推送功能

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 📧 联系方式

如有问题或建议，欢迎提 Issue。

---

**再次提醒**：投资有风险，入市需谨慎。本平台不承担任何投资损失责任。