#!/bin/bash

echo "======================================"
echo "DeepSeek AI 炒股平台 - 启动脚本"
echo "======================================"
echo ""

# 检查是否在backend目录中有.env文件
if [ ! -f "backend/.env" ]; then
    echo "⚠️  警告：未找到 backend/.env 文件"
    echo "请执行以下步骤："
    echo "1. cd backend"
    echo "2. cp .env.example .env"
    echo "3. 编辑 .env 文件，填入您的 DeepSeek API Key"
    echo ""
    read -p "是否现在创建 .env 文件？(y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cp backend/.env.example backend/.env
        echo "✅ 已创建 backend/.env 文件"
        echo "请编辑该文件并填入您的 API Key，然后重新运行此脚本"
        exit 0
    else
        echo "❌ 启动已取消"
        exit 1
    fi
fi

# 检查Python依赖
echo "检查Python依赖..."
if ! pip show fastapi > /dev/null 2>&1; then
    echo "⚠️  未安装依赖，正在安装..."
    cd backend
    pip install -r requirements.txt
    cd ..
    echo "✅ 依赖安装完成"
else
    echo "✅ 依赖已安装"
fi

echo ""
echo "======================================"
echo "启动后端服务..."
echo "======================================"
cd backend
python run.py &
BACKEND_PID=$!
cd ..

echo ""
echo "✅ 后端服务已启动 (PID: $BACKEND_PID)"
echo "   访问地址: http://localhost:8000"
echo ""

# 等待后端启动
sleep 3

echo "======================================"
echo "启动前端服务..."
echo "======================================"
cd frontend
python -m http.server 3000 &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ 前端服务已启动 (PID: $FRONTEND_PID)"
echo "   访问地址: http://localhost:3000"
echo ""
echo "======================================"
echo "🎉 启动完成！"
echo "======================================"
echo ""
echo "请在浏览器中打开: http://localhost:3000"
echo ""
echo "按 Ctrl+C 停止所有服务"
echo ""

# 等待用户中断
trap "echo ''; echo '正在停止服务...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo '✅ 服务已停止'; exit 0" INT

# 保持脚本运行
wait
