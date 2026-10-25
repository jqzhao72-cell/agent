# Agent｜多智能体研究与知识库助手

一个可在本地运行的 AI Agent 项目：由主智能体理解任务并调度联网搜索、数据库查询和知识库检索子智能体，再整合结果生成回答或报告。项目提供 Web 对话界面、运行轨迹，以及基于 SQLite 和 LangGraph checkpoint 的会话续聊。

> 本仓库基于 [waseens/deep-search-pro](https://github.com/waseens/deep-search-pro) 二次开发。这里记录的是当前仓库的功能与改造方向；原项目版权及 MIT 许可见 [LICENSE](LICENSE)。

## 项目亮点

| 能力 | 当前实现 |
| --- | --- |
| 多智能体协作 | 基于 DeepAgents 构建主智能体，按任务需要调用联网搜索、MySQL 查询、知识库检索三个子智能体 |
| 灵活接入模型 | 主智能体与子智能体分别配置模型；联网搜索单独使用阿里云百炼 Qwen 内置搜索，避免混用密钥 |
| 接入已有 RAG | 知识库子智能体可调用独立部署的 DocPilot，也保留 RAGFlow 接入方式 |
| 持久化续聊 | SQLite 保存聊天记录和记忆，LangGraph SQLite checkpointer 保存图状态；重启后可使用原 `thread_id` 继续对话 |
| 可观察性 | WebSocket 推送执行事件，`/trace` 页面展示角色、工具调用与运行过程 |
| Web 工作台 | 支持历史会话、附件上传、Markdown 回答和生成文件下载 |

### 我在这个版本重点做的改造

- 将模型配置拆分为主模型、子智能体模型和联网搜索模型，便于分别控制调用成本。
- 将原有知识库入口对接到独立的 DocPilot RAG 服务，并保留 RAGFlow 选项。
- 增加应用层对话记忆、摘要与显式长期记忆；接入 LangGraph 持久化 checkpoint，让同一会话在服务重启后仍可续聊。
- 完善历史会话恢复、运行状态展示及运行轨迹查询，便于定位 Agent 调用问题。

## 系统架构

```text
浏览器聊天页 / Trace 诊断页
          │ HTTP + WebSocket
          ▼
       FastAPI
          │
          ▼
   主智能体（DeepAgents）
      ├─ 联网搜索子智能体 → 阿里云百炼 Qwen 内置搜索
      ├─ 数据库子智能体   → MySQL（可选）
      └─ 知识库子智能体   → DocPilot 或 RAGFlow（可选）
          │
          ├─ SQLite：聊天记录、长期记忆、LangGraph checkpoint
          └─ Trace Store：当前进程的运行事件 → WebSocket /trace
```

主智能体负责判断何时调用子智能体。简单问题可能直接回答，不一定触发搜索或 RAG；要核实是否调用，可以查看 `/trace` 中的工具与角色事件。

## 技术栈

Python、FastAPI、DeepAgents、LangChain、LangGraph、SQLite、WebSocket、原生 HTML/CSS/JavaScript；可选对接 DeepSeek、阿里云百炼、DocPilot、RAGFlow 和 MySQL。

## 本地启动（Windows PowerShell）

需要 Python 3.10+。模型与外部服务需要各自有效的账号、权限和额度；仅填写配置不保证对应服务可调用。

```powershell
git clone https://github.com/jqzhao72-cell/agent.git
cd agent
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

在 `.env` 中填写自己的配置，不要提交真实密钥。下面仅列出主要配置项；完整模板见 [.env.example](.env.example)。模型名称必须以你所用服务实际支持的名称为准。

```dotenv
# 主智能体与子智能体使用 DeepSeek 兼容接口
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_API_KEY=在此填写你自己的密钥
LLM_MAIN_MODEL=填写实际可用的主模型名称
SUBAGENT_MODEL=填写实际可用的子模型名称

# 联网搜索使用阿里云百炼，凭据与上面分开
OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
OPENAI_API_KEY=在此填写你自己的百炼密钥
ALIYUN_SEARCH_MODEL=qwen-flash
ALIYUN_SEARCH_STRATEGY=turbo

# 可选：对接单独运行的 DocPilot
KNOWLEDGE_BACKEND=docpilot
DOCPILOT_BASE_URL=http://127.0.0.1:8000
DOCPILOT_USERNAME=你的DocPilot账号
DOCPILOT_PASSWORD=你的DocPilot密码
```

如需改用 RAGFlow，将 `KNOWLEDGE_BACKEND` 改为 `ragflow`，并配置 `RAGFLOW_API_URL` 和 `RAGFLOW_API_KEY`。MySQL 子智能体需要单独配置 `MYSQL_*` 项，建议使用只读、最小权限账号。未配置的外部服务不会提供对应的检索能力。

安装完成后运行：

```powershell
.\start.ps1
```

启动脚本使用项目内 `.venv`，在 `127.0.0.1:8002` 提供服务。打开 [聊天页](http://127.0.0.1:8002/) 或 [运行轨迹页](http://127.0.0.1:8002/trace)。如需其他端口，可自行运行：

```powershell
.\.venv\Scripts\python.exe -m uvicorn api.server:app --host 127.0.0.1 --port 8003
```

## 如何验证功能

1. 在聊天页提问一般问题，确认主模型能正常回答。
2. 提问一个需要最新资料的问题，再到 `/trace` 确认联网搜索子智能体是否真正被调用。
3. 在 DocPilot 中准备好可检索文档并启动其服务，提问文档内的具体内容；在 `/trace` 查看知识库工具调用。
4. 在同一会话继续追问“刚才那份文档的第二点是什么”，刷新页面或重启本服务后再打开原会话，验证续聊。

同一会话依赖 `thread_id`。点击“新对话”会创建新会话；页面地址中的 `?thread_id=...` 可以用于恢复指定会话。`data/memory.db` 和 `data/checkpoints.db` 保存应用记忆与 LangGraph 状态，默认不会提交到 Git。

## 主要代码位置

| 目录或文件 | 作用 |
| --- | --- |
| `agent/main_agent.py` | 主智能体、子智能体装配及运行流程 |
| `agent/checkpoint_store.py` | LangGraph SQLite checkpoint |
| `agent/llm.py` | 主模型和子智能体模型初始化 |
| `agent/subagents/` | 搜索、数据库、知识库子智能体定义 |
| `tools/aliyun_search_tool.py`、`tools/docpilot_tool.py` | 外部搜索与已有 RAG 对接 |
| `api/server.py`、`api/memory_store.py` | API、任务运行、对话与长期记忆 |
| `api/trace_store.py`、`api/monitor.py` | 运行事件记录与实时推送 |
| `web/` | 聊天工作台和 Trace 页面 |

## 当前边界

- `Trace Store` 保存在进程内，服务重启后旧运行轨迹可能消失；这不影响 SQLite 中的聊天记录和 checkpoint。
- 当前没有完整的人工审批 / Human-in-the-Loop 中断恢复流程，也没有面向公网的用户认证与权限控制。建议仅在可信本地环境运行。
- 主智能体会自主选择是否调用工具，因此不能保证每个问题都触发所有子智能体。
- PDF 转换等部分文件能力依赖 Windows 环境；运行费用和响应时间受模型、网络、工具调用次数及外部服务状态影响。

## 测试

```powershell
.\.venv\Scripts\python.exe -m pytest -q
node --test tests/frontend_*.test.mjs
```

前端测试需要另行安装 Node.js。测试不应使用真实密钥或生产数据库。

## 开源说明

本仓库在原项目基础上进行二次开发，保留原作者的 MIT 许可与版权声明。原项目：[waseens/deep-search-pro](https://github.com/waseens/deep-search-pro)；本仓库：[jqzhao72-cell/agent](https://github.com/jqzhao72-cell/agent)。
