"""通过 DocPilot 的受保护 HTTP API 查询用户已有的知识库。"""

import os
from typing import Literal

import requests
from dotenv import load_dotenv
from langchain_core.tools import tool

from api.monitor import monitor


load_dotenv()


def _base_url() -> str:
    value = os.getenv("DOCPILOT_BASE_URL", "http://127.0.0.1:8000").strip().rstrip("/")
    if not value.startswith(("http://", "https://")):
        raise ValueError("DOCPILOT_BASE_URL 必须是 http:// 或 https:// 开头的地址")
    return value


def _request(session: requests.Session, method: str, path: str, **kwargs):
    response = session.request(method, _base_url() + path, timeout=90, **kwargs)
    if not response.ok:
        # 服务端详情可能包含敏感信息，工具只返回状态码和操作路径。
        raise RuntimeError(f"DocPilot {path} 返回 HTTP {response.status_code}")
    return response.json()


def _authenticated_session() -> requests.Session:
    session = requests.Session()
    token = os.getenv("DOCPILOT_ACCESS_TOKEN", "").strip()
    if not token:
        username = os.getenv("DOCPILOT_USERNAME", "").strip()
        password = os.getenv("DOCPILOT_PASSWORD", "")
        if not username or not password:
            raise ValueError(
                "请在 .env 中设置 DOCPILOT_USERNAME 和 DOCPILOT_PASSWORD，"
                "或设置临时的 DOCPILOT_ACCESS_TOKEN。"
            )
        login = _request(
            session, "POST", "/login",
            json={"username": username, "password": password},
        )
        token = login.get("access_token", "")
        if not token:
            raise RuntimeError("DocPilot 登录未返回 access_token")
    session.headers.update({"Authorization": f"Bearer {token}"})
    return session


@tool
@monitor.traced_tool("DocPilot 知识库列表")
def list_knowledge_bases() -> dict:
    """列出 DocPilot 的 company 和 paper 知识库中当前账号可见的文档。"""
    try:
        with _authenticated_session() as session:
            return {
                knowledge_base: _request(
                    session, "GET", "/documents", params={"knowledge_base": knowledge_base}
                )
                for knowledge_base in ("company", "paper")
            }
    except (requests.RequestException, RuntimeError, ValueError) as exc:
        return {"error": f"DocPilot 知识库查询失败：{exc}"}


@tool
@monitor.traced_tool("DocPilot 知识库问答")
def ask_knowledge_base(
    question: str,
    knowledge_base: Literal["company", "paper"] = "company",
) -> dict:
    """在 DocPilot 企业或论文知识库检索证据，并返回答案与引用来源。

    Args:
        question: 针对已有文档的具体问题。
        knowledge_base: company 为企业知识库，paper 为论文知识库。
    """
    try:
        with _authenticated_session() as session:
            conversation = _request(
                session, "POST", "/conversations",
                json={"title": "Deep Search Pro 知识库检索", "knowledge_base": knowledge_base},
            )
            result = _request(
                session, "POST", "/chat",
                json={"question": question, "conversation_id": conversation["id"]},
            )
            return {
                "knowledge_base": knowledge_base,
                "answer": result.get("answer", ""),
                "sources": result.get("sources", []),
            }
    except (requests.RequestException, RuntimeError, ValueError, KeyError) as exc:
        return {"error": f"DocPilot 知识库问答失败：{exc}"}
