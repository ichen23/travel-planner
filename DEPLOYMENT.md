# Railway 部署指南

## 前置条件

1. 注册 [Railway](https://railway.app/) 账号
2. 安装 [Railway CLI](https://docs.railway.app/develop/cli) (可选，推荐)
3. 将代码推送到 GitHub 仓库

## 部署步骤

### 方式一：通过 Railway 网站部署（推荐）

1. **登录 Railway 并创建项目**
   - 访问 https://railway.app/new
   - 选择 "Deploy from GitHub repo"
   - 点击 "Create New Project"

2. **选择仓库**
   - 在 "Connected Apps" 区域点击 "+"
   - 选择你的 GitHub 仓库
   - Railway 会自动检测 Dockerfile

3. **配置环境变量**
   
   在项目设置的 "Variables" 标签页，添加以下变量：
   
   ```
   # 必填：高德地图 Web 服务 API Key
   AMAP_KEY=你的高德地图Key
   
   # 必填：聚合一创 12306 API Key
   JUHE_API_KEY=你的聚合一创Key
   
   # 可选：高德地图安全密钥
   AMAP_SECRET=你的安全密钥（如果开启了安全密钥验证）
   ```
   
   获取方式：
   - 高德地图：https://console.amap.com/
   - 聚合一创：https://www.juhe.cn/docs/api/id/46

4. **部署**
   - 点击 "Deploy" 按钮
   - 等待构建完成（约 3-5 分钟）
   - 部署成功后会显示服务 URL

### 方式二：通过 Railway CLI 部署

1. **安装 CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **登录**
   ```bash
   railway login
   ```

3. **初始化项目（只需一次）**
   ```bash
   cd travel-planner
   railway init
   ```

4. **配置环境变量**
   ```bash
   railway variables set AMAP_KEY=你的高德地图Key
   railway variables set JUHE_API_KEY=你的聚合一创Key
   ```

5. **部署**
   ```bash
   railway up
   ```

6. **查看服务 URL**
   ```bash
   railway status
   ```

## 环境变量说明

| 变量名 | 是否必填 | 说明 |
|--------|----------|------|
| `AMAP_KEY` | 是 | 高德地图 Web 服务 API Key，用于查询景点、餐厅等 |
| `JUHE_API_KEY` | 是 | 聚合一创 12306 API Key，用于查询真实火车票 |
| `AMAP_SECRET` | 否 | 高德地图安全密钥（如果在控制台开启了安全密钥验证） |
| `PORT` | 否 | 服务端口，Railway 会自动设置 |

## 架构说明

项目采用前后端分离架构，通过 Docker 多阶段构建打包：

```
├── 构建阶段 (Node.js 18)
│   ├── 安装 npm 依赖
│   └── 构建前端 → dist/
│
└── 运行阶段 (Python 3.11)
    ├── 安装 Python 依赖
    ├── 复制后端代码
    ├── 复制前端构建产物
    └── FastAPI + Uvicorn
```

**端口**: 8000 (Uvicorn)

## 健康检查

Railway 会定期检查 `/api/health` 端点：

```bash
curl https://your-app-url.up.railway.app/api/health
# 响应: {"status":"ok","version":"1.0.0","service":"travel-planner-api"}
```

## 常见问题

### Q: 部署失败，提示 API Key 无效？
A: 请检查环境变量名称是否正确（`AMAP_KEY` 不是 `AMAP_API_KEY`），并确保 Key 没有多余的空格。

### Q: 前端页面无法加载？
A: 健康检查返回 200 但前端 404？请确保 Docker 构建日志显示 `COPY ... dist/` 成功。

### Q: 高德地图提示"KEY 鉴权失败"？
A: 可能需要在高德控制台配置安全密钥，然后在 Railway 添加 `AMAP_SECRET` 变量。

### Q: 12306 API 返回"请求次数超限"？
A: 聚合一创有每日免费额度，超过后返回错误。建议升级套餐或添加错误处理。

### Q: 如何查看日志？
A: 在 Railway Dashboard 的 "Logs" 标签页，或使用 CLI：
```bash
railway logs
```

### Q: 如何更新部署？
A: 每次推送到 GitHub 主分支会自动触发重新部署。或使用 CLI：
```bash
git add .
git commit -m "Update"
git push
```

## 成本说明

- Railway 免费版提供 $5 每月的消费额度
- 基础运行成本：~$3-5/月
- 升级到 Pro：$5/月起

## 其他部署选项

- **Render**: 类似 Railway，支持 Docker 部署
- **Vercel**: 仅适合前端静态部署（不支持后端）
- **Netlify**: 仅支持前端静态部署

## 技术支持

如遇问题，请：
1. 查看 Railway 日志
2. 检查环境变量配置
3. 确认 API Key 是否有效
4. 访问 https://railway.app/docs 查看官方文档
