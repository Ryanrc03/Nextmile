# Nextmile RAG 系统重构指南

## 📋 概述

我已经将原来混合在一起的RAG算法和API代码进行了重构，现在你可以独立地调试和优化RAG算法，而不需要启动整个API服务。

## 📁 新的文件结构

```
chatbot/
├── config.py           # 统一配置管理
├── rag_core.py         # RAG核心算法 (独立)
├── rag_debugger.py     # 本地调试工具
├── api_server.py       # 清洁的API服务器
├── quick_start.py      # 快速开始指南
├── README_REFACTOR.md  # 本文档
└── [原始文件保留...]
```

## 🚀 快速开始

### 1. 本地调试RAG算法

最简单的方式是使用调试器：

```bash
# 交互式调试模式
python rag_debugger.py

# 批量测试模式
python rag_debugger.py batch

# 使用自定义Excel文件
python rag_debugger.py file your_resume.xlsx
```

### 2. 在Python代码中使用RAG核心

```python
from rag_core import ResumeRAGCore

# 基本使用
rag = ResumeRAGCore()
result = rag.query("What experience do you have with machine learning?")
print(result['answer'])

# 使用自定义配置
config = {
    "rag": {
        "similarity_top_k": 3,
        "keyword_weight": 0.7
    },
    "model": {
        "temperature": 0.5,
        "max_tokens": 1500
    }
}
rag = ResumeRAGCore(config=config)
```

### 3. 启动API服务器

```bash
python api_server.py
```

API文档: http://localhost:8000/docs

## 🔧 核心组件说明

### 1. `rag_core.py` - RAG核心算法

**特点:**
- 纯算法实现，与API解耦
- 可配置的检索和生成参数
- 详细的日志和性能统计
- 支持自定义Excel文件

**主要类:**
- `ResumeRAGCore`: 主要的RAG系统类

**核心方法:**
- `retrieve(query)`: 文档检索
- `generate_prompt()`: 提示生成
- `generate_response()`: AI回答生成
- `query()`: 完整查询流程

### 2. `rag_debugger.py` - 调试工具

**功能:**
- 交互式查询调试
- 分步骤显示RAG流程
- 实时配置调整
- 批量测试
- 性能分析

**调试模式:**
- 显示检索到的文档和相似度分数
- 展示生成的Prompt内容
- 分析响应时间和检索效果
- 配置参数实时调整

### 3. `api_server.py` - API服务器

**改进:**
- 清洁的API代码，只负责HTTP处理
- 通过`rag_core`调用算法
- 完整的错误处理和日志
- 结构化的响应格式

### 4. `config.py` - 配置管理

**集中管理:**
- 模型配置
- RAG算法参数
- API服务配置
- 日志配置

## 🎯 主要优势

### 1. 算法独立调试
```python
# 直接测试算法，无需启动API
from rag_core import ResumeRAGCore

rag = ResumeRAGCore()
result = rag.query("测试问题")

# 检查检索效果
docs = rag.retrieve("测试问题")
for doc in docs:
    print(f"相似度: {doc['score']:.3f}")
    print(f"内容: {doc['data']['context'][:100]}...")
```

### 2. 灵活的配置调整
```python
# 运行时调整参数
rag.update_config({
    "rag": {
        "similarity_top_k": 3,
        "keyword_weight": 0.8
    }
})

# 立即测试效果
result = rag.query("同样的问题")
```

### 3. 详细的调试信息
- 每个检索文档的相似度分数
- Prompt生成的详细过程
- AI响应时间分析
- 配置参数影响分析

## 📊 使用调试器优化算法

### 1. 启动调试器
```bash
python rag_debugger.py
```

### 2. 测试不同查询
输入各种问题，观察：
- 检索到的文档是否相关
- 相似度分数是否合理
- AI回答的质量

### 3. 调整配置参数
在调试器中输入 `config`，可以实时调整：
- `similarity_top_k`: 检索文档数量
- `keyword_weight`: 关键词匹配权重
- `exact_match_weight`: 精确匹配权重
- `min_score_threshold`: 最低相似度阈值

### 4. 批量测试
```bash
python rag_debugger.py batch
```
自动测试多个预设问题，比较性能。

## 🔍 调试示例

### 检索效果分析
当你输入问题后，调试器会显示：
```
📝 步骤1: 检索相关文档
✅ 找到 3 个相关文档:
   1. Baidu Inc. - AI/ML Engineer (相似度: 0.852)
   2. Apple Inc. - Data Scientist (相似度: 0.734)
   3. Michelin - IT Intern (相似度: 0.621)
```

### 配置优化建议
- **相似度分数太低**: 降低 `min_score_threshold`
- **检索文档不相关**: 调整权重参数
- **回答太长/太短**: 修改 `max_tokens`
- **回答太保守/太创意**: 调整 `temperature`

## 📈 性能优化建议

### 1. 检索优化
- 调整 `keyword_weight` 和 `exact_match_weight` 的比例
- 根据数据特点调整 `similarity_top_k`
- 设置合适的 `min_score_threshold`

### 2. 生成优化
- 根据需求调整 `temperature` (0.0-1.0)
- 设置合适的 `max_tokens`
- 优化Prompt模板

### 3. 数据优化
- 确保Excel文件格式正确
- 检查数据质量和完整性
- 考虑添加更多上下文信息

## 🚀 开发工作流

### 1. 算法开发
```bash
# 启动调试器
python rag_debugger.py

# 测试和调整参数
# 在调试器中实时查看效果
```

### 2. 批量验证
```bash
# 运行批量测试
python rag_debugger.py batch

# 分析结果和性能指标
```

### 3. 集成测试
```bash
# 启动API服务器
python api_server.py

# 测试API端点
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"text": "测试问题"}'
```

## 📞 故障排除

### 常见问题

1. **导入错误**: 确保安装了所需依赖
   ```bash
   pip install openai pandas numpy fastapi uvicorn
   ```

2. **API密钥错误**: 检查 `config.py` 中的API密钥配置

3. **Excel文件读取失败**: 确保文件路径正确且格式为Excel

4. **数据库连接失败**: 检查MongoDB连接配置

### 调试技巧

1. **使用日志**: 设置日志级别为DEBUG查看详细信息
2. **分步调试**: 使用调试器的详细模式
3. **配置备份**: 记录有效的配置参数组合

## 🎉 总结

现在你有了一个完全独立的RAG算法调试环境！你可以：

- ✅ 独立调试和优化RAG算法
- ✅ 实时调整配置参数
- ✅ 详细分析检索和生成效果
- ✅ 批量测试不同场景
- ✅ 保持API服务的简洁性

开始使用：
```bash
python quick_start.py
```

祝你调试愉快！🚀