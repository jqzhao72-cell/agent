from types import SimpleNamespace

import tools.docpilot_tool as docpilot


class FakeSession:
    def __init__(self):
        self.headers = {}
        self.calls = []

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def request(self, method, url, **kwargs):
        self.calls.append((method, url, kwargs))
        if url.endswith("/login"):
            data = {"access_token": "temporary-token"}
        elif url.endswith("/conversations"):
            data = {"id": 12}
        elif url.endswith("/chat"):
            data = {"answer": "根据文件 [1]", "sources": [{"source": "手册.pdf", "page": 3}]}
        else:
            raise AssertionError(url)
        return SimpleNamespace(ok=True, json=lambda: data)


def test_docpilot_question_uses_authenticated_conversation(monkeypatch):
    session = FakeSession()
    monkeypatch.setattr(docpilot.requests, "Session", lambda: session)
    monkeypatch.setenv("DOCPILOT_BASE_URL", "http://127.0.0.1:8000")
    monkeypatch.setenv("DOCPILOT_USERNAME", "reader")
    monkeypatch.setenv("DOCPILOT_PASSWORD", "private-password")
    monkeypatch.delenv("DOCPILOT_ACCESS_TOKEN", raising=False)

    result = docpilot.ask_knowledge_base.invoke(
        {"question": "文档说了什么？", "knowledge_base": "paper"}
    )

    assert result["answer"] == "根据文件 [1]"
    assert result["sources"] == [{"source": "手册.pdf", "page": 3}]
    assert [call[1].rsplit("/", 1)[-1] for call in session.calls] == [
        "login", "conversations", "chat"
    ]
    assert session.calls[1][2]["json"]["knowledge_base"] == "paper"
    assert session.calls[2][2]["json"] == {"question": "文档说了什么？", "conversation_id": 12}
    assert session.headers["Authorization"] == "Bearer temporary-token"
