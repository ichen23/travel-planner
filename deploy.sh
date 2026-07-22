#!/bin/bash
# Railway 部署辅助脚本

echo "🚄 Railway 部署辅助脚本"
echo "======================="
echo ""

# 检查是否在正确的目录
if [ ! -f "package.json" ] || [ ! -f "Dockerfile" ]; then
    echo "❌ 请在 travel-planner 目录下运行此脚本"
    exit 1
fi

echo "📁 当前目录: $(pwd)"
echo ""

# 检查 Git
if [ ! -d ".git" ]; then
    echo "⚠️  未检测到 Git 仓库，正在初始化..."
    git init
    git add .
    git commit -m "Initial commit: Travel Planner for Railway deployment"
    echo "✅ Git 仓库初始化完成"
else
    echo "✅ Git 仓库已存在"
fi

echo ""

# 检查 Railway CLI
if command -v railway &> /dev/null; then
    echo "✅ Railway CLI 已安装"
    echo ""
    echo "📝 下一步："
    echo "1. 运行 'railway login' 登录"
    echo "2. 运行 'railway init' 初始化项目"
    echo "3. 运行以下命令配置环境变量："
    echo "   railway variables set AMAP_KEY=你的高德地图Key"
    echo "   railway variables set JUHE_API_KEY=你的聚合一创Key"
    echo "4. 运行 'railway up' 部署"
else
    echo "⚠️  未检测到 Railway CLI"
    echo ""
    echo "📝 安装 CLI:"
    echo "   npm install -g @railway/cli"
    echo ""
    echo "🌐 或者通过网页部署:"
    echo "   https://railway.app/new"
    echo ""
    echo "📝 步骤:"
    echo "1. 创建 GitHub 仓库并推送代码："
    echo "   git remote add origin https://github.com/你的用户名/仓库名.git"
    echo "   git push -u origin main"
    echo "2. 访问 https://railway.app/new"
    echo "3. 选择 GitHub 仓库进行部署"
    echo "4. 在 Railway 控制台添加环境变量"
fi

echo ""
echo "📖 详细文档请查看 DEPLOYMENT.md"
