"""使用阿里云百炼 Qwen 内置联网搜索的 Agent 工具。"""

import os
from typing import Literal

from dotenv import load_dotenv
from langchain_core.tools import tool
from openai import OpenAI

from api.monitor import monitor


load_dotenv()


def _get_client() -> OpenAI:
    """延迟创建客户端，避免未配置密钥时项目无法启动。"""
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    base_url = os.getenv("OPENAI_BASE_URL", "").strip()
    if not api_key or not base_url:
        raise ValueError(
            "联网搜索尚未配置：请在 .env 中填写 OPENAI_API_KEY 和 "
            "OPENAI_BASE_URL（从阿里云百炼工作空间复制 API Host）。"
        )
    return OpenAI(api_key=api_key, base_url=base_url)


@tool
@monitor.traced_tool("百炼联网搜索工具")
def internet_search(
    query: str,
    topic: Literal["news", "finance", "general"] = "general",
    max_results: int = 5,
) -> dict:
    """使用阿里云百炼 Qwen 的内置联网搜索查询公开互联网信息。

    Args:
        query: 需要检索的问题，建议包含时间、地区和对象等限定词。
        topic: 信息类型，可选 news、finance 或 general。
        max_results: 希望参考的来源数量，仅用于指导模型整理结果。
    """
    # 搜索模型与主模型分开配置，避免每次联网都使用昂贵的旗舰模型。
    model = os.getenv("ALIYUN_SEARCH_MODEL", "qwen-flash").strip() or "qwen-flash"
    strategy = os.getenv("ALIYUN_SEARCH_STRATEGY", "turbo").strip().lower()
    if strategy not in {"turbo", "max"}:
        strategy = "turbo"

    response = _get_client().chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "你是网络研究助手。必须使用联网搜索获取最新公开信息；"
                    "清楚区分事实与推断，并在答案中保留来源名称和链接。"
                ),
            },
            {
                "role": "user",
                "content": (
                    f"检索主题类型：{topic}\n"
                    f"请优先参考不超过 {max(1, min(max_results, 10))} 个高质量来源。\n"
                    f"问题：{query}"
                ),
            },
        ],
        extra_body={
            "enable_search": True,
            "search_options": {
                "forced_search": True,
                "enable_source": True,
                "search_strategy": strategy,
            },
        },
    )

    message = response.choices[0].message
    result = {
        "query": query,
        "answer": message.content or "",
        "model": model,
        "search_strategy": strategy,
    }

    # 百炼可能在扩展字段中返回结构化搜索来源；存在时一并交给 Agent。
    response_data = response.model_dump()
    for key in ("search_info", "search_results", "sources"):
        if response_data.get(key):
            result[key] = response_data[key]
    return result
