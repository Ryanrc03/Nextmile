# Nextmile Backend API

基于 Node.js + Express + MongoDB + TypeScript 的 Nextmile 后端 API。

## 功能特性

- 🚀 **RESTful API** - 完整的 CRUD 操作
- 📊 **MongoDB 数据库** - 使用 Mongoose ODM
- 🔒 **TypeScript** - 类型安全
- 🌐 **CORS 支持** - 前端跨域请求
- 📝 **数据验证** - Mongoose 模式验证
- 🔄 **热重载** - 开发时自动重启

## 项目结构

```
src/
├── config/          # 配置文件
├── controllers/     # 控制器
├── models/          # 数据模型
├── routes/          # 路由
├── middleware/      # 中间件
├── types/           # TypeScript 类型定义
├── app.ts           # Express 应用配置
├── server.ts        # 服务器启动文件
└── seedData.ts      # 数据种子文件
```

## API 端点

### 工作经验 (Experience)
- `GET /api/experience` - 获取所有工作经验
- `GET /api/experience/:id` - 获取单个工作经验
- `POST /api/experience` - 创建新的工作经验
- `PUT /api/experience/:id` - 更新工作经验
- `DELETE /api/experience/:id` - 删除工作经验

### 项目 (Projects)
- `GET /api/projects` - 获取所有项目
- `GET /api/projects?featured=true` - 获取精选项目
- `GET /api/projects?status=completed` - 按状态筛选项目
- `GET /api/projects/:id` - 获取单个项目
- `POST /api/projects` - 创建新项目
- `PUT /api/projects/:id` - 更新项目
- `DELETE /api/projects/:id` - 删除项目

### 健康检查
- `GET /api/health` - API 健康状态检查

## 快速开始

### 1. 安装依赖
```bash
npm install
```

### 2. 配置环境变量
创建 `.env` 文件并配置：
```env
PORT=5000
MONGODB_URI=mongodb://localhost:27017/portfolio
NODE_ENV=development
FRONTEND_URL=http://localhost:3000
```

### 3. 启动 MongoDB
确保 MongoDB 服务正在运行：
```bash
# macOS 使用 Homebrew
brew services start mongodb-community

# 或直接启动
mongod
```

### 4. 初始化数据（可选）
```bash
npx ts-node src/seedData.ts
```

### 5. 启动开发服务器
```bash
npm run dev
```

服务器将在 http://localhost:5000 启动

### 6. 构建生产版本
```bash
npm run build
npm start
```

## 数据模型

### Experience（工作经验）
```typescript
{
  company: string;           // 公司名称
  position: string;          // 职位
  duration: string;          // 工作时长
  description: string;       // 描述
  achievements: string[];    // 成就列表
  startDate: Date;          // 开始日期
  endDate?: Date;           // 结束日期
  isCurrentJob: boolean;    // 是否为当前工作
  location?: string;        // 工作地点
  companyLogo?: string;     // 公司图标
}
```

### Project（项目）
```typescript
{
  title: string;            // 项目标题
  description: string;      // 项目描述
  year: number;            // 年份
  url: string;             // 项目链接
  technologies: string[];   // 技术栈
  featured: boolean;       // 是否精选
  imageUrl?: string;       // 项目图片
  githubUrl?: string;      // GitHub 链接
  liveUrl?: string;        // 在线演示链接
  status: 'completed' | 'in-progress' | 'planned';  // 项目状态
}
```

## 开发脚本

- `npm run dev` - 启动开发服务器（热重载）
- `npm run build` - 构建生产版本
- `npm start` - 启动生产服务器
- `npx ts-node src/seedData.ts` - 初始化种子数据

## 技术栈

- **Node.js** - JavaScript 运行时
- **Express** - Web 框架
- **MongoDB** - 数据库
- **Mongoose** - MongoDB ODM
- **TypeScript** - 类型安全
- **CORS** - 跨域支持
- **Dotenv** - 环境变量管理

## 前端集成

前端可以通过以下方式调用 API：

```typescript
// 获取所有工作经验
const response = await fetch('http://localhost:5000/api/experience');
const data = await response.json();

// 获取所有项目
const response = await fetch('http://localhost:5000/api/projects');
const data = await response.json();
```

## 部署建议

1. **环境变量**: 在生产环境中设置正确的环境变量
2. **MongoDB**: 使用 MongoDB Atlas 或其他云数据库
3. **HTTPS**: 在生产环境中使用 HTTPS
4. **反向代理**: 使用 Nginx 作为反向代理
5. **进程管理**: 使用 PM2 管理 Node.js 进程

