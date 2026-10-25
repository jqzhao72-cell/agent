"""Tools that give the main agent explicit, user-controlled long-term memory."""

from langchain_core.tools import tool

from api.context import get_thread_context
from api.memory_store import memory_store
from api.monitor import monitor


@tool
@monitor.traced_tool("保存长期记忆")
def remember_user_memory(content: str, category: str = "general") -> dict:
    """仅当用户明确要求“记住”时，保存一条跨会话长期记忆。

    不得保存密码、API Key、访问令牌，或未经用户明确要求的推测信息。
    """
    item = memory_store.remember(
        content,
        category=category,
        source_thread_id=get_thread_context(),
    )
    return {"status": "saved", "id": item.id, "content": item.content}


@tool
@monitor.traced_tool("删除长期记忆")
def forget_user_memory(keyword: str) -> dict:
    """当用户明确要求忘记某项信息时，按关键词删除匹配的长期记忆。"""
    count = memory_store.forget(keyword)
    return {"status": "forgotten", "count": count, "keyword": keyword}


@tool
@monitor.traced_tool("查看长期记忆")
def list_user_memories() -> dict:
    """当用户询问系统记住了什么时，列出当前启用的长期记忆。"""
    items = memory_store.list_memories(limit=100)
    return {
        "count": len(items),
        "memories": [
            {"id": item.id, "category": item.category, "content": item.content}
            for item in items
        ],
    }
