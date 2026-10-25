from pathlib import Path

import pytest

from api.memory_store import MemoryStore


def test_three_layer_memory_survives_reopen_and_bounds_prompt(monkeypatch, tmp_path: Path):
    monkeypatch.setenv("MEMORY_RECENT_TURNS", "2")
    monkeypatch.setenv("MEMORY_SUMMARY_MAX_CHARS", "300")
    monkeypatch.setenv("MEMORY_LONG_TERM_MAX_ITEMS", "2")
    db_path = tmp_path / "memory.db"
    store = MemoryStore(db_path)

    for index in range(3):
        run_id = f"run-{index}"
        store.add_message("thread-1", "user", f"问题 {index}", run_id=run_id)
        store.add_message("thread-1", "assistant", f"回答 {index}", run_id=run_id)

    summary = store.update_summary_if_needed("thread-1")
    assert "问题 0" in summary
    assert len(store.get_messages("thread-1", limit=4)) == 4

    remembered = store.remember(
        "知识库使用 DocPilot",
        category="project_config",
        source_thread_id="thread-1",
    )
    context = store.build_prompt_context("thread-1", "查询我的知识库配置")
    assert "较早对话摘要" in context
    assert "最近对话" in context
    assert "知识库使用 DocPilot" in context

    reopened = MemoryStore(db_path)
    assert len(reopened.get_messages("thread-1")) == 6
    assert reopened.get_summary("thread-1") == summary
    assert reopened.list_memories(limit=10)[0].id == remembered.id


def test_long_term_memory_is_deduplicated_forgettable_and_rejects_secrets(tmp_path: Path):
    store = MemoryStore(tmp_path / "memory.db")
    first = store.remember("偏好中文回答", category="preference")
    duplicate = store.remember("偏好中文回答", category="preference")

    assert first.id == duplicate.id
    assert len(store.list_memories(limit=10)) == 1
    assert store.forget("中文") == 1
    assert store.list_memories(limit=10) == []

    with pytest.raises(ValueError, match="不能把密码"):
        store.remember("API_KEY=sk-example-secret-value")


def test_clear_conversation_does_not_delete_long_term_memory(tmp_path: Path):
    store = MemoryStore(tmp_path / "memory.db")
    store.add_message("thread-1", "user", "你好", run_id="run-1")
    store.remember("主模型使用 Qwen", source_thread_id="thread-1")

    assert store.clear_conversation("thread-1") is True
    assert store.get_messages("thread-1") == []
    assert [item.content for item in store.list_memories(limit=10)] == ["主模型使用 Qwen"]


def test_explicit_memory_commands_are_deterministic(tmp_path: Path):
    store = MemoryStore(tmp_path / "memory.db")

    saved = store.handle_explicit_command("请记住：以后优先使用中文", "thread-1")
    assert "已可靠写入" in saved
    assert store.list_memories(limit=10)[0].content == "以后优先使用中文"

    listed = store.handle_explicit_command("你记得我什么？", "thread-1")
    assert "以后优先使用中文" in listed

    forgotten = store.handle_explicit_command("忘记：中文", "thread-1")
    assert "删除 1 条" in forgotten
    assert store.list_memories(limit=10) == []
