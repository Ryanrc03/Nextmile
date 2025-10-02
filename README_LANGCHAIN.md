# Nextmile LangChain RAG Chatbot 🤖

基于 LangChain 的智能简历问答系统，支持对话记忆和语义检索。

## 🎯 系统架构

```
┌─────────────────────────────────────────────────────┐
│                  API Layer (FastAPI)                │
│                 api_server_langchain.py             │
└─────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────┐
│              RAG Adapter (rag_langchain.py)         │
│             适配器层 - 连接 API 和 RAG 系统          │
└─────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────┐
│           Chatbot Layer (chatbot.py)                │
│          对话管理 + 记忆 (ConversationBufferMemory) │
└─────────────────────────────────────────────────────┘
                         ↓
        ┌────────────────┴────────────────┐
        ↓                                  ↓
┌──────────────────┐            ┌──────────────────┐
│  Retrieval Layer │            │ Generation Layer │
│  (retreival.py)  │            │ (generation.py)  │
│                  │            │                  │
│  • ChromaDB      │            │  • DeepSeek-V3.1 │
│  • Embeddings    │            │  • Prompt Build  │
└──────────────────┘            └──────────────────┘
```

## 🚀 快速开始

### 方式 1: 使用 Docker (推荐)

```bash
# 1. 确保 Docker 和 Docker Compose 已安装

# 2. 启动服务
./start_langchain.sh
# 选择选项 2 (后台启动)

# 3. 访问 API
# API 地址: http://localhost:8000
# API 文档: http://localhost:8000/docs
```

### 方式 2: 本地运行

```bash
# 1. 安装依赖
cd chatbot
pip install -r requirements.txt

# 2. 确保 MongoDB 正在运行
# 或者使用 Docker:
docker run -d -p 27017:27017 --name mongodb mongo:6.0

# 3. 启动 API 服务
python api_server_langchain.py
```

## 📡 API 端点

### 1. 健康检查
```bash
GET /health
```

响应示例：
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": 1704154800.0,
  "rag_system": "healthy",
  "system_info": {
    "system": "LangChain RAG",
    "components": {
      "chunking": "RecursiveCharacterTextSplitter",
      "embedding": "sentence-transformers/all-MiniLM-L6-v2",
      "vectorstore": "ChromaDB",
      "llm": "deepseek-ai/DeepSeek-V3.1",
      "memory": "ConversationBufferMemory"
    }
  }
}
```

### 2. 聊天接口
```bash
POST /chat
Content-Type: application/json

{
  "text": "What are the candidate's main skills?",
  "session_id": "optional-session-id",
  "user_id": "optional-user-id"
}
```

响应示例：
```json
{
  "reply": "I have strong experience in machine learning and deep learning...",
  "session_id": "abc-123",
  "conversation_id": "conv-456",
  "response_time": 1.234,
  "retrieved_count": 5,
  "success": true
}
```

### 3. 对话历史
```bash
GET /history/{session_id}?limit=10
```

### 4. 清除历史
```bash
POST /clear_history/{session_id}
```

## 🧪 测试 API

```bash
# 健康检查
curl http://localhost:8000/health

# 发送聊天消息
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"text": "What are your skills?"}'

# 获取对话历史
curl http://localhost:8000/history/your-session-id
```

## 🐳 Docker 命令

```bash
# 启动服务
docker-compose -f docker-compose.langchain.yml up -d

# 查看日志
docker-compose -f docker-compose.langchain.yml logs -f

# 停止服务
docker-compose -f docker-compose.langchain.yml down

# 重新构建
docker-compose -f docker-compose.langchain.yml up --build -d

# 查看服务状态
docker-compose -f docker-compose.langchain.yml ps
```

## 📂 项目结构

```
Nextmile/
├── chatbot/                      # API 服务代码
│   ├── api_server_langchain.py  # 新的 LangChain API 服务器
│   ├── rag_langchain.py         # LangChain RAG 适配器
│   ├── config.py                # 配置文件
│   ├── db_config.py             # 数据库配置
│   └── requirements.txt         # Python 依赖
├── RAG_algotirhm/
│   └── rag_core/
│       └── LangChainRag/        # LangChain RAG 核心代码
│           ├── chatbot.py       # 对话管理
│           ├── retreival.py     # 检索模块
│           ├── generation.py    # 生成模块
│           ├── chucking.py      # 数据处理
│           └── docs/
│               └── chroma/      # ChromaDB 向量数据库
├── Dockerfile.langchain         # Docker 构建文件
├── docker-compose.langchain.yml # Docker Compose 配置
├── start_langchain.sh           # 启动脚本
└── README_LANGCHAIN.md          # 本文档
```

## 🔧 配置

编辑 `chatbot/config.py` 修改配置：

```python
API_CONFIG = {
    "host": "0.0.0.0",
    "port": 8000,
    "cors_origins": ["*"],
    # ...
}
```

## 📊 技术栈

- **Framework**: FastAPI + Uvicorn
- **RAG System**: LangChain
- **Vector Store**: ChromaDB
- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2)
- **LLM**: DeepSeek-V3.1 (via ModelScope)
- **Memory**: ConversationBufferMemory
- **Database**: MongoDB
- **Containerization**: Docker + Docker Compose

## 🎨 特性

✅ 基于 LangChain 的模块化 RAG 架构  
✅ ChromaDB 向量存储和语义检索  
✅ 对话记忆管理（支持上下文理解）  
✅ RESTful API 接口  
✅ Docker 容器化部署  
✅ MongoDB 对话历史持久化  
✅ 健康检查和监控  
✅ 完整的 API 文档 (Swagger UI)  

## 🐛 故障排除

### 问题 1: Docker 构建失败
```bash
# 清理 Docker 缓存
docker system prune -a
docker-compose -f docker-compose.langchain.yml build --no-cache
```

### 问题 2: 端口被占用
```bash
# 检查端口占用
lsof -i :8000
lsof -i :27017

# 或者修改 docker-compose.langchain.yml 中的端口映射
```

### 问题 3: ChromaDB 数据未加载
```bash
# 确保 ChromaDB 数据目录存在
ls -la RAG_algotirhm/rag_core/LangChainRag/docs/chroma/

# 重新生成数据（如果需要）
cd RAG_algotirhm/rag_core/LangChainRag
python chucking.py
```

## 📝 更新日志

### v3.0.0 (2025-01-02)
- 🎉 集成 LangChain RAG 系统
- ✨ 添加对话记忆功能
- 🚀 Docker 容器化部署
- 📚 完整的 API 文档

## 📧 联系

如有问题，请联系开发团队或查看项目文档。

---

**Happy Coding! 🚀**
