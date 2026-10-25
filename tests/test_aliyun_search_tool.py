from types import SimpleNamespace

import tools.aliyun_search_tool as search_module


class _FakeResponse:
    choices = [SimpleNamespace(message=SimpleNamespace(content="带来源的搜索答案"))]

    def model_dump(self):
        return {"search_info": {"search_results": [{"title": "示例来源"}]}}


class _FakeCompletions:
    def __init__(self):
        self.kwargs = None

    def create(self, **kwargs):
        self.kwargs = kwargs
        return _FakeResponse()


def test_internet_search_uses_bailian_built_in_search(monkeypatch):
    completions = _FakeCompletions()
    fake_client = SimpleNamespace(
        chat=SimpleNamespace(completions=completions),
    )
    monkeypatch.setattr(search_module, "_get_client", lambda: fake_client)
    monkeypatch.setenv("ALIYUN_SEARCH_MODEL", "qwen-flash")
    monkeypatch.setenv("ALIYUN_SEARCH_STRATEGY", "turbo")

    result = search_module.internet_search.invoke(
        {"query": "今天的人工智能新闻", "topic": "news", "max_results": 3}
    )

    assert result["answer"] == "带来源的搜索答案"
    assert result["search_info"]["search_results"][0]["title"] == "示例来源"
    assert completions.kwargs["model"] == "qwen-flash"
    assert completions.kwargs["extra_body"] == {
        "enable_search": True,
        "search_options": {
            "forced_search": True,
            "enable_source": True,
            "search_strategy": "turbo",
        },
    }
