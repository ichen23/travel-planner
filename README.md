# 高铁旅行规划系统

基于高铁出行的智能旅行规划平台，提供票务查询、行程规划、AI推荐等功能。

## 技术栈
- 前端：React 18 + Ant Design 5 + Vite
- 后端：Python 3.11 + FastAPI
- 部署：Docker + Railway

## 本地开发
```bash
# 后端
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# 前端
npm install
npm run dev
```

## Railway 部署

### 环境变量配置
部署前需要在 Railway 设置以下环境变量：

| 变量名 | 说明 |
|--------|------|
| `AMAP_KEY` | 高德地图 API Key |
| `AMAP_SECRET` | 高德地图 Secret |
| `JUHE_API_KEY` | 聚合数据 API Key |

### 部署步骤
1. 将代码推送到 GitHub
2. 在 Railway 创建新项目，选择 GitHub Repository
3. 配置环境变量
4. Railway 会自动识别 Dockerfile 并部署

### 服务说明
- Railway 会自动注入 `PORT` 环境变量
- Dockerfile 使用 `sh -c` 来动态读取端口
- 应用默认监听 `0.0.0.0`
