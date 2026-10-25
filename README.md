<p align="center">
  <h1 align="center">🤖 Deep Search Pro</h1>
  <p align="center"><b>一个轻量的多智能体协作系统 —— Agent 开发入门实战项目</b></p>
  <p align="center"><a href="README.en.md">English README</a></p>
  <p align="center">
    <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python">
    <img src="https://img.shields.io/badge/FastAPI-0.129.2-green.svg" alt="FastAPI">
    <img src="https://img.shields.io/badge/LangChain-1.2.10-orange.svg" alt="LangChain">
    <img src="https://img.shields.io/badge/deepagents-0.4.3-purple.svg" alt="deepagents">
    <img src="https://img.shields.io/badge/适合-学习练手-brightgreen.svg" alt="learning">
  </p>
</p>

---

## 🎯 这个项目是什么

这是一个面向学习的 AI Agent 实战项目。它用尽量少的工程噪音，展示如何基于 LangChain / deepagents 构建一个**多智能体协作系统**：一个"主智能体"像团队负责人一样，调度三个"子智能体"（网络搜索、数据库查询、知识库检索）协同完成复杂任务。

项目现在也带了一个可直接使用的 Web 控制台：

- `/`：深色聊天工作台，支持附件上传、会话历史、Markdown 答案和生成文件下载
- `/trace`：运行追踪与诊断页，支持流程图、角色状态、事件列表、最终报告、原始数据和节点详情抽屉
- `run_id` 级轨迹：每次任务都有独立运行 ID，可以通过 HTTP 和 WebSocket 恢复事件流

**如果你是以下人群，这个项目就是为你准备的 👇**

- 正在学习 LangChain / LangGraph，想找一个**完整的、能跑起来的**实战项目
- 对"多智能体编排"感兴趣，但不想一上来就看复杂的 AutoGPT / CrewAI 源码
- 想理解 **FastAPI + WebSocket + Agent + 前端控制台** 怎么组合成真实可用的系统
- 面试前需要一个 AI Agent 项目来充实简历，并且能讲清楚每个设计决策

---

## 🧠 你能从这个项目中学到什么

| 知识点 | 具体体现在项目哪里 |
|--------|------------------|
| **Orchestrator 多智能体模式** | `agent/main_agent.py` — 主智能体如何调度 3 个子智能体 |
| **Prompt Engineering 实战** | `prompt/prompts.yml` — 如何用 system_prompt 约束 Agent 行为 |
| **LangChain @tool 自定义工具** | `tools/` 目录 — 工具函数的完整写法 |
| **FastAPI 异步 + 后台任务** | `api/server.py` — `asyncio.create_task` 非阻塞执行 |
| **WebSocket 实时推送** | `api/monitor.py` — 运行事件实时推送到前端 |
| **run 级 Trace 协议** | `api/trace_router.py` / `api/trace_store.py` — 查询、恢复、分页与断点续传 |
| **ContextVar 协程级数据隔离** | `api/context.py` — 多用户并发时不串台 |
| **前端状态与会话恢复** | `web/session.js` / `web/run-client.js` — 本地会话、恢复、重连和去重 |
| **聊天交互细节** | `web/chat-interactions.js` — Enter 发送、IME 保护、滚动跟随 |
| **Trace 可视化** | `web/visualizer.js` — 节点状态、连线拓扑、缩放和曲线路径 |
| **Agent 文件操作安全** | `utils/path_utils.py` — 12 种路径场景的防护 |
| **RAG 知识库对接** | `tools/ragflow_tools.py` — RAGFlow SDK 实战 |
| **数据库自然语言查询** | `tools/db_tools.py` — Agent 自动写 SQL 并执行 |

---

## ✨ 已有功能

### 智能体能力

- 主智能体自动判断任务需要哪些信息源
- 网络搜索子智能体：调用阿里云百炼 Qwen 内置联网搜索获取外部资料
- 数据库查询子智能体：查看 MySQL 表结构、生成 SQL、执行查询
- 知识库检索子智能体：可接入桌面已有 DocPilot RAG，或切回 RAGFlow
- Markdown 报告生成与 PDF 转换工具
- 上传文件读取工具，任务可以结合用户提供的参考资料

### Web 聊天工作台

- 深色高级简约聊天界面，包含侧边栏、会话列表、顶部状态栏和底部 composer
- 支持先上传多个附件，再提交同一个 `thread_id` 下的任务
- Enter 发送，Shift+Enter 换行
- 中文输入法组合态保护，并兼容 WebKit `keyCode=229`
- 运行中禁用提交与上传按钮，并显示发送按钮 spinner
- 自动跟随最新回复；用户向上阅读时不会被强制拉到底部
- 有新内容时显示"回到最新消息"按钮
- Markdown 答案安全渲染，支持表格、代码块、链接和生成文件下载
- 本地保存最近会话，支持搜索与切换
- 对过期的内存 Trace 做降级处理，避免页面切换时反复弹旧运行错误

### Trace 运行诊断页

- 独立 `/trace` 页面，用来查看一次 Agent 运行的完整过程
- 支持输入问题、上传文件、重新运行检索
- 展示 6 个运行指标：耗时、事件、活跃角色、工具调用、生成文件、连接状态
- 展示 5 个角色摘要：Main Agent、Network Search、Database Query、Knowledge Base、Report / Files
- 保留 8 个流程节点和 11 条拓扑连线，连线使用柔和曲线
- 支持流程图缩放、适应窗口、节点选择和状态高亮
- Inspector 抽屉可查看节点或事件的概览、输入、输出、原始事件和错误
- 下方运行记录包含事件、最终报告、生成文件、原始数据四个 tab
- 事件列表支持搜索和按状态筛选
- WebSocket 支持 `after_sequence` 断点恢复，前端按 `event_id` 去重

---

## 🏗️ 架构一览

整个项目的核心链路非常直接，适合按模块阅读：

```
用户输入
  ├── 浏览器聊天页 /
  └── Trace 诊断页 /trace
        │
        ▼
api/server.py
  ├── POST /api/upload       上传参考文件
  ├── POST /api/task         创建任务，返回 thread_id + run_id
  ├── GET /api/threads/...   查询某个 thread 的运行列表
  ├── GET /api/runs/...      查询某个 run 的 Trace 事件
  └── WS /ws/{thread_id}     推送实时运行事件
        │
        ▼
agent/main_agent.py
  ├── 子智能体 1：网络搜索       tools/aliyun_search_tool.py
  ├── 子智能体 2：数据库查询     tools/db_tools.py
  ├── 子智能体 3：知识库         tools/docpilot_tool.py 或 tools/ragflow_tools.py
  └── 主智能体工具：Markdown / PDF / 上传文件读取
        │
        ▼
api/monitor.py + api/trace_store.py
  └── 记录事件、广播 WebSocket、支持页面恢复和断点续传
```

### 数据流说明

1. 用户在聊天页或 Trace 页提交一个自然语言请求
2. 前端先上传附件，再调用 `POST /api/task`
3. 后端为本次任务创建独立 `run_id`，并立即预留 Trace 记录
4. 主智能体分析需求，决定调用哪些子智能体
5. 子智能体各司其职，去搜网络 / 查数据库 / 翻知识库 / 读取上传文件
6. 主智能体汇总信息，生成最终 Markdown 报告，必要时生成文件
7. 整个过程通过 WebSocket 实时推送到前端，同时写入进程内 Trace store
8. 页面刷新或重连时，前端通过 `run_id + after_sequence` 恢复事件

---

## 🚀 5 分钟跑起来

### 环境要求

- Python 3.10+
- 阿里云百炼 API Key 和对应工作空间的 API Host

> 📌 数据库和知识库服务是可选信息源；使用对应子智能体前，需要先配置并启动该服务。

如果使用桌面已有的 DocPilot 项目，在 `.env` 中设置 `KNOWLEDGE_BACKEND=docpilot`、`DOCPILOT_BASE_URL=http://127.0.0.1:8000`，并填写 DocPilot 登录账号与密码。DocPilot 后端需要单独运行。这个账号的文档权限决定知识库助手能检索哪些资料；DocPilot 内部的 DeepSeek 配置与本项目的百炼配置彼此独立。要切回 RAGFlow，设置 `KNOWLEDGE_BACKEND=ragflow` 并配置 `RAGFLOW_API_URL`、`RAGFLOW_API_KEY`。

### 第一步：克隆 + 装依赖

```bash
git clone https://github.com/你的用户名/deep-search-pro.git
cd deep-search-pro
pip install -r requirements.txt
```

### 第二步：配环境变量

```bash
cp .env.example .env
```

编辑 `.env`。主模型和子 Agent 使用 DeepSeek 官网凭证；联网搜索继续单独使用百炼凭证：

```env
# DeepSeek 官网：主模型和子 Agent
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxx
LLM_MAIN_MODEL=deepseek-v4-pro
SUBAGENT_MODEL=deepseek-flash
LLM_ENABLE_THINKING=false

# 阿里云百炼：仅用于内置联网搜索
OPENAI_BASE_URL=https://你的WorkspaceId.cn-beijing.maas.aliyuncs.com/compatible-mode/v1
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx

ALIYUN_SEARCH_MODEL=qwen-flash
# 可选：联网搜索策略，turbo 较快，max 更深入
ALIYUN_SEARCH_STRATEGY=turbo

# 以下可选，不填就只影响对应功能
# RAGFLOW_API_URL=...
# MYSQL_USER=...
```

### 第三步：启动

```bash
python api/server.py
```

默认访问：

- `http://localhost:8000/`：Deep Search 聊天工作台
- `http://localhost:8000/trace`：运行追踪与诊断页
- `http://localhost:8000/docs`：Swagger API 文档

如果你想指定端口，例如本地调试常用的 8002：

```bash
uvicorn api.server:app --host 127.0.0.1 --port 8002
```

然后访问 `http://127.0.0.1:8002/` 和 `http://127.0.0.1:8002/trace`。

### 第四步：试一试

```bash
curl -X POST http://localhost:8000/api/task \
  -H "Content-Type: application/json" \
  -d '{"query": "搜索一下最近 AI Agent 领域的最新进展"}'
```

返回值会包含 `thread_id` 和 `run_id`：

```json
{
  "status": "started",
  "thread_id": "conversation-id",
  "run_id": "unique-run-id"
}
```

浏览器里打开 `/trace?thread_id=conversation-id&run_id=unique-run-id`，就能看到这次运行的实时轨迹。

---

## 📖 推荐阅读顺序

如果你是第一次接触 AI Agent 项目，建议按这个顺序读代码：

| 顺序 | 文件 | 重点看什么 |
|------|------|-----------|
| 1️⃣ | `agent/llm.py` | 看 LLM 怎么初始化，如何适配 OpenAI 兼容协议 |
| 2️⃣ | `prompt/prompts.yml` | 看系统提示词怎么写，怎么约束 Agent 行为 |
| 3️⃣ | `agent/subagents/network_search_agent.py` | 最简单的子智能体，理解"子智能体 = 字典配置" |
| 4️⃣ | `tools/aliyun_search_tool.py` | 百炼内置联网搜索工具和埋点怎么写 |
| 5️⃣ | `agent/main_agent.py` | **核心**：主智能体怎么创建、怎么 orchestrate、怎么流式执行 |
| 6️⃣ | `api/server.py` | FastAPI 怎么和 Agent 结合，异步任务怎么触发 |
| 7️⃣ | `api/monitor.py` | WebSocket 实时推送，事件循环归属判断 |
| 8️⃣ | `api/trace_store.py` | run 级 Trace 如何存储、分页、淘汰 |
| 9️⃣ | `api/context.py` | ContextVar 为什么比全局变量好 |
| 🔟 | `web/run-client.js` | 前端如何上传文件、启动任务、恢复 Trace 和重连 |
| 1️⃣1️⃣ | `web/chat.js` / `web/app.js` | 聊天页和 Trace 页如何消费同一套运行状态 |
| 1️⃣2️⃣ | `utils/path_utils.py` | Agent 文件安全——边界场景大全 |

---

## 📁 项目文件速查

```
deep_search_pro/
│
├── agent/                          # 🤖 智能体层（核心）
│   ├── llm.py                      # 模型初始化
│   ├── prompts.py                  # YAML 提示词加载
│   ├── main_agent.py               # ★ 主智能体 + 异步执行引擎
│   └── subagents/                  # 子智能体（每个就是一个字典）
│       ├── network_search_agent.py
│       ├── database_query_agent.py
│       └── knowledge_base_agent.py
│
├── api/                            # 🌐 Web 接口层
│   ├── server.py                   # FastAPI 入口、上传、任务、WebSocket
│   ├── context.py                  # ContextVar 协程隔离（带详细注释）
│   ├── monitor.py                  # 监控埋点 + WebSocket 连接池
│   ├── trace_models.py             # Trace 事件、状态、响应模型
│   ├── trace_router.py             # Trace HTTP 查询 API
│   ├── trace_serializer.py         # Trace 输出清洗与错误规范化
│   └── trace_store.py              # 进程内 run 级轨迹存储
│
├── web/                            # 🖥 原生前端，无打包步骤
│   ├── index.html                  # 聊天页
│   ├── trace.html                  # Trace 诊断页
│   ├── styles.css                  # 共享深色视觉系统
│   ├── trace.css                   # Trace 页面样式
│   ├── api.js                      # HTTP / WebSocket API 封装
│   ├── run-client.js               # 上传、启动、恢复、重连生命周期
│   ├── session.js                  # 本地会话、URL 构造与恢复选择
│   ├── state.js                    # 前端运行状态与角色推导
│   ├── chat.js                     # 聊天页渲染和交互
│   ├── chat-interactions.js        # 输入、滚动、渲染批次纯逻辑
│   ├── visualizer.js               # Trace 流程图节点和连线
│   └── markdown.js                 # 安全 Markdown 渲染
│
├── tools/                          # 🔧 工具函数（@tool）
│   ├── aliyun_search_tool.py        # 百炼 Qwen 内置联网搜索
│   ├── tavily_tool.py               # 旧导入路径兼容层
│   ├── db_tools.py                 # 数据库查询 3 件套
│   ├── ragflow_tools.py            # RAGFlow 知识库检索
│   ├── markdown_tools.py           # 生成 Markdown
│   ├── pdf_tools.py                # Markdown → PDF
│   └── upload_file_read_tool.py    # 读取上传文件
│
├── tests/                          # 🧪 Python + Node 前端测试
│   ├── test_trace_*.py             # Trace API / store / monitor 测试
│   ├── test_web_frontend.py        # Web 页面与静态资源合同测试
│   └── frontend_*.test.mjs         # 原生 ES module 前端单元测试
│
├── utils/                          # 🛠 工具层
│   ├── path_utils.py               # 路径安全解析（12 种场景）
│   └── word_converter.py           # Word COM 引擎
│
├── rawflow/                        # 📚 RAGFlow SDK 独立示例
├── prompt/prompts.yml              # 提示词配置
├── requirements.txt                # 依赖清单（版本锁定）
└── .env.example                    # 环境变量模板
```

---

## 📡 Trace API

`POST /api/task` 会为每次调用创建独立的 `run_id`：

```json
{
  "status": "started",
  "thread_id": "conversation-id",
  "run_id": "unique-run-id"
}
```

`thread_id` 表示可复用的会话，`run_id` 表示该会话中的一次任务运行。即使复用 `thread_id`，每次请求也会获得新的 `run_id`。

历史查询：

```text
GET /api/runs/{run_id}/trace?after_sequence=12&limit=100
GET /api/threads/{thread_id}/runs
```

`after_sequence` 是排他的，只返回 sequence 大于该值的事件。WebSocket 连接可以使用同样的断点恢复语义：

```text
ws://localhost:8000/ws/{thread_id}?run_id={run_id}&after_sequence=12
```

Trace 事件会包含 `event_id`、`sequence`、`thread_id`、`run_id`、`event`、`node_type`、`status`、`input`、`output`、`error` 等字段。前端会按 `event_id` 去重，并用 `sequence` 做恢复游标。

需要注意：轨迹存储目前是**单进程内存存储**，服务重启后会丢失；多 worker 或多实例之间暂不共享轨迹。浏览器本地会保留 `thread_id`，但不会把已经过期的 `run_id` 强行恢复成报错弹窗。

兼容字段 `type="monitor_event"` 和 `data` 在 1.x 协议期间保留，2.0 协议可能移除。

---

## 🧠 三层记忆与续聊

系统使用 `data/memory.db` 保存聊天历史和应用层记忆，使用 `data/checkpoints.db` 保存 LangGraph 图状态；两个数据库都在服务重启后保留。前端重新打开同一个 `thread_id` 后，新问题会沿用该线程的 checkpoint：

1. **最近对话**：应用层默认保留最近 8 轮原文，便于旧会话首次迁移到 checkpoint 时理解“它”“上一份文档”等上下文。
2. **会话摘要**：应用层将更早内容折叠为最多 800 个字符的滚动摘要；已建立 checkpoint 的会话由 DeepAgents/LangGraph 保留和整理图内消息，不会每轮重复注入应用层历史。
3. **长期记忆**：跨会话保存用户明确要求记住的稳定偏好和项目配置，每次最多注入 5 条相关内容。

长期记忆采用明确授权：系统不会自动把普通聊天推断成用户事实。可以直接在聊天中使用：

```text
记住：以后优先使用中文回答
你记得我什么？
忘记：中文回答
```

密码、API Key 和访问令牌会被拒绝写入长期记忆。完整聊天记录保存在应用层 SQLite 中；已有 checkpoint 的会话只更新相关长期记忆，不重复注入应用层历史。新建 checkpoint 前，旧会话迁移上下文受以下参数限制：

```dotenv
MEMORY_DB_PATH=data/memory.db
MEMORY_RECENT_TURNS=8
MEMORY_SUMMARY_MAX_CHARS=800
MEMORY_LONG_TERM_MAX_ITEMS=5
CHECKPOINT_DB_PATH=data/checkpoints.db
```

续聊时要保留原 `thread_id`（例如打开 `/?thread_id=...`）；点击“新对话”会生成新 ID。清空会话会同时删除聊天记录和 LangGraph checkpoint，但不会删除跨会话长期记忆。运行轨迹仍保存在进程内，重启后可能无法查看旧 Trace；这不影响已持久化的对话和续聊。

记忆接口：

```text
GET    /api/memory/threads/{thread_id}   获取持久化对话
DELETE /api/memory/threads/{thread_id}   清空某个会话记忆
GET    /api/memories                     查看长期记忆
DELETE /api/memories/{memory_id}         删除指定长期记忆
```

---

## 🧪 测试

Python 测试：

```bash
pytest -q
```

前端 ES module 测试：

```bash
node --test tests/frontend_*.test.mjs
```

常用聚焦测试：

```bash
pytest tests/test_web_frontend.py tests/test_trace_api.py -q
node --test tests/frontend_session.test.mjs tests/frontend_chat_interactions.test.mjs
```

如果本地 Python 环境自动加载了第三方 pytest 插件并导致无关依赖报错，可以临时禁用插件自动加载：

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 pytest -q
```

Windows PowerShell：

```powershell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'
pytest -q
```

---

## 🧪 练手建议：你可以这样改造

项目的设计刻意保持简洁，给你留了很多动手空间。以下是一些建议的改造方向，难度递进：

### 入门级（加深理解）

- [ ] **换个模型**：把通义千问换成 DeepSeek 或 GPT，改 `.env` 一行就行
- [ ] **加一个子智能体**：比如"天气查询助手"或"代码执行助手"，体验一下加子智能体要多改几行代码
- [ ] **改 system_prompt**：把"空调公司"改成你自己的业务场景，看看 Agent 行为怎么变化
- [ ] **加一个 Trace 事件类型**：从 model 到前端 tab，完整走一遍协议链路

### 进阶级（工程能力）

- [x] **加入 SQLite 三层记忆**：最近对话、滚动摘要和长期记忆在重启后仍可恢复
- [ ] **把 Trace store 持久化**：用 SQLite 或 Redis 保存 `run_id` 轨迹
- [ ] **给 Trace 事件加导出**：把某次运行导出成 JSON / Markdown 调试报告
- [ ] **给子智能体加"反思"机制**：让子智能体执行完后再自我检查一遍，提高准确性
- [ ] **加 JWT 认证**：给 `/api/task`、`/api/upload` 和 `/trace` 加上登录校验

### 挑战级（深入学习）

- [ ] **把 Word COM 换成 WeasyPrint**：摆脱 Windows 依赖，让 PDF 转换在 Linux 上跑
- [ ] **用 LangGraph 的 checkpointer 实现"人工审批节点"**：敏感操作需要用户确认才执行
- [ ] **给子智能体之间加"通信"**：让数据库子智能体和网络搜索子智能体能互相交换信息
- [ ] **Docker 化**：写 Dockerfile + docker-compose，一键启动所有依赖
- [ ] **多用户部署**：把内存态、上传目录、WebSocket 连接和 Trace 存储都改成可横向扩展

---

## 🔧 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| Agent 框架 | **deepagents** (LangChain 官方) | 多智能体编排，本项目核心依赖 |
| LLM 接入 | LangChain + OpenAI 兼容协议 | 一套代码适配多种模型 |
| Web 框架 | FastAPI + Uvicorn | 异步 HTTP + 原生 WebSocket |
| 前端 | HTML + CSS + 原生 ES Modules | 无构建步骤，适合学习和调试 |
| Trace | 进程内 run 级事件存储 | 支持分页、断点恢复和前端去重 |
| 搜索引擎 | 阿里云百炼 Qwen 内置搜索 | 与主模型共用 API Key，无需 Tavily |
| 知识库 | RAGFlow | 开源的 RAG 引擎，可以本地部署 |
| 数据库 | MySQL | 关系型数据库，Agent 自动写 SQL |
| 文档生成 | markdown + pywin32 | MD 生成 + Word COM 转 PDF |
| 测试 | pytest + Node test runner | Python 后端测试 + 前端纯函数测试 |

---

## ❓ FAQ

### Q: 为什么选 deepagents 而不是自己写编排逻辑？

**A:** 自己写编排要处理状态管理、tool_call 路由、流式输出、错误恢复等一堆事。`deepagents` 把这些都封装好了，你只需要定义子智能体的 name / description / tools，框架帮你调度。对学习来说，先理解"用框架能做什么"，之后再看源码理解"框架怎么做的"。

### Q: 没有 RAGFlow 和 MySQL，项目还能跑吗?

**A:** 能。主智能体会根据 system_prompt 判断只有“网络搜索”可用，自动跳过另外两个子智能体。只配置百炼 API Key、API Host 和模型名，就能使用主模型与内置联网搜索。当然功能会受限——这就是刻意设计的“优雅降级”。

### Q: 为什么用 ContextVar 而不是全局变量？

**A:** FastAPI 下多个请求跑在同一个线程的不同协程里。如果用全局变量，用户 A 的数据会被用户 B 覆盖（串台）。ContextVar 是 Python 为 asyncio 设计的协程级变量，每个请求链路互不干扰。`api/context.py` 里有详细注释解释这个问题。

### Q: 为什么 Trace 会丢失？

**A:** 当前 Trace store 是进程内存存储。它适合学习、调试和单机演示，但服务重启、测试清空、超过容量上限都会让旧 `run_id` 失效。浏览器会保留会话入口，但不会保证旧运行永久可恢复。如果要生产化，建议把 `api/trace_store.py` 换成 SQLite、PostgreSQL 或 Redis。

### Q: 为什么前端不用 React / Vue？

**A:** 故意的。这个项目的重点是 Agent、Trace 协议和异步链路，而不是前端框架。原生 HTML / CSS / ES Modules 没有构建步骤，打开文件就能读懂数据流，也方便用 Node 直接测试纯函数。

### Q: 项目为什么保持轻量？

**A:** 这是给学习用的项目，不是给生产用的。每个模块只做一件事，代码量和依赖都尽量克制。如果你能把这些核心模块都读明白，多智能体 Agent 的主要概念就掌握了。

---

## 📄 License

MIT License —— 随便用，改，分叉。如果你基于这个项目做了有趣的东西，欢迎提 PR 或者告诉我 😄
