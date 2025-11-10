// API 基础URL - 根据实际部署修改
const API_BASE_URL = 'http://localhost:8000';

// DOM 元素
const screenBtn = document.getElementById('screenBtn');
const loadStocksBtn = document.getElementById('loadStocksBtn');
const loading = document.getElementById('loading');
const results = document.getElementById('results');
const criteriaInput = document.getElementById('criteria');
const maxResultsInput = document.getElementById('maxResults');
const maxAnalyzeInput = document.getElementById('maxAnalyze');

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    checkAPIHealth();
    setupEventListeners();
});

// 设置事件监听
function setupEventListeners() {
    screenBtn.addEventListener('click', handleScreen);
    loadStocksBtn.addEventListener('click', handleLoadStocks);
}

// 检查API健康状态
async function checkAPIHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/health`);
        const data = await response.json();

        if (!data.api_configured) {
            showWarning('警告：DeepSeek API未配置，请先设置.env文件中的API密钥');
        }
    } catch (error) {
        showWarning('无法连接到后端服务，请确保后端已启动');
    }
}

// 处理股票筛选
async function handleScreen() {
    const criteria = criteriaInput.value.trim();

    if (!criteria) {
        alert('请输入筛选条件');
        return;
    }

    const maxResults = parseInt(maxResultsInput.value);
    const maxAnalyze = parseInt(maxAnalyzeInput.value);

    // 显示加载状态
    showLoading();
    hideResults();

    try {
        const response = await fetch(`${API_BASE_URL}/api/screen`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                criteria: criteria,
                max_results: maxResults,
                max_stocks_to_analyze: maxAnalyze
            })
        });

        const data = await response.json();

        if (data.success) {
            displayResults(data);
        } else {
            throw new Error(data.error || '筛选失败');
        }
    } catch (error) {
        alert(`筛选失败: ${error.message}`);
        console.error('Error:', error);
    } finally {
        hideLoading();
    }
}

// 处理加载股票列表
async function handleLoadStocks() {
    const tableDiv = document.getElementById('stocksTable');
    tableDiv.innerHTML = '<div class="loading"><div class="spinner"></div></div>';

    try {
        const response = await fetch(`${API_BASE_URL}/api/stocks?limit=50`);
        const data = await response.json();

        if (data.success && data.stocks.length > 0) {
            displayStocksTable(data.stocks);
        } else {
            tableDiv.innerHTML = '<p>暂无数据</p>';
        }
    } catch (error) {
        tableDiv.innerHTML = `<p>加载失败: ${error.message}</p>`;
        console.error('Error:', error);
    }
}

// 显示筛选结果
function displayResults(data) {
    // 显示分析总结
    const analysisDiv = document.getElementById('analysis');
    analysisDiv.innerHTML = `
        <h3>分析总结</h3>
        <p>${data.analysis}</p>
    `;

    // 显示股票列表
    const stockListDiv = document.getElementById('stockList');
    if (data.stocks && data.stocks.length > 0) {
        stockListDiv.innerHTML = data.stocks.map(stock => `
            <div class="stock-card">
                <div class="stock-header">
                    <div>
                        <span class="stock-title">${stock.name}</span>
                        <span class="stock-code">${stock.code}</span>
                    </div>
                    <div class="stock-score">${stock.score}分</div>
                </div>
                <div class="stock-reason">${stock.reason}</div>
            </div>
        `).join('');
    } else {
        stockListDiv.innerHTML = '<p>未找到符合条件的股票</p>';
    }

    // 显示风险提示
    const riskWarningDiv = document.getElementById('riskWarning');
    riskWarningDiv.innerHTML = `<strong>风险提示：</strong> ${data.risk_warning}`;

    // 显示结果区域
    showResults();
}

// 显示股票表格
function displayStocksTable(stocks) {
    const tableDiv = document.getElementById('stocksTable');

    const table = `
        <table>
            <thead>
                <tr>
                    <th>代码</th>
                    <th>名称</th>
                    <th>最新价</th>
                    <th>涨跌幅</th>
                    <th>换手率</th>
                    <th>市盈率</th>
                    <th>市净率</th>
                </tr>
            </thead>
            <tbody>
                ${stocks.map(stock => `
                    <tr>
                        <td>${stock.code}</td>
                        <td>${stock.name}</td>
                        <td>${formatNumber(stock.price)}</td>
                        <td class="${stock.change_pct >= 0 ? 'positive' : 'negative'}">
                            ${formatPercent(stock.change_pct)}
                        </td>
                        <td>${formatPercent(stock.turnover_rate)}</td>
                        <td>${formatNumber(stock.pe_dynamic)}</td>
                        <td>${formatNumber(stock.pb)}</td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;

    tableDiv.innerHTML = table;
}

// 工具函数
function showLoading() {
    loading.style.display = 'block';
}

function hideLoading() {
    loading.style.display = 'none';
}

function showResults() {
    results.style.display = 'block';
}

function hideResults() {
    results.style.display = 'none';
}

function showWarning(message) {
    const warning = document.createElement('div');
    warning.className = 'risk-warning';
    warning.textContent = message;
    warning.style.position = 'fixed';
    warning.style.top = '20px';
    warning.style.right = '20px';
    warning.style.maxWidth = '400px';
    warning.style.zIndex = '1000';
    document.body.appendChild(warning);

    setTimeout(() => {
        warning.remove();
    }, 5000);
}

function formatNumber(num) {
    if (num === null || num === undefined || num === 0) return '-';
    return num.toFixed(2);
}

function formatPercent(num) {
    if (num === null || num === undefined || num === 0) return '-';
    const formatted = num.toFixed(2);
    return num >= 0 ? `+${formatted}%` : `${formatted}%`;
}
