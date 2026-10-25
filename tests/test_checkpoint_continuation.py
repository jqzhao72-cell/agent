import asyncio

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.graph import MessagesState, StateGraph

from agent import main_agent
from agent.checkpoint_store import delete_thread_checkpoint, open_checkpointer
from api.memory_store import MemoryStore


def test_checkpoint_keeps_one_thread_across_graph_recreation(monkeypatch, tmp_path):
    monkeypatch.setenv("CHECKPOINT_DB_PATH", str(tmp_path / "checkpoints.db"))
    store = MemoryStore(tmp_path / "memory.db")
    store.add_message("old-thread", "user", "之前的提问")
    store.add_message("old-thread", "assistant", "之前的回答")
    store.remember("偏好中文回答")
    monkeypatch.setattr(main_agent, "memory_store", store)

    def answer(state):
        questions = [
            message.content
            for message in state["messages"]
            if isinstance(message, HumanMessage)
        ]
        return {"messages": [AIMessage(content=" | ".join(questions))]}

    builder = StateGraph(MessagesState)
    builder.add_node("answer", answer)
    builder.set_entry_point("answer")
    builder.set_finish_point("answer")
    monkeypatch.setattr(
        main_agent,
        "create_main_agent",
        lambda checkpointer: builder.compile(checkpointer=checkpointer),
    )

    async def run_once(query, thread_id, run_id):
        config = {"configurable": {"thread_id": thread_id}}
        chunks = [
            chunk async for chunk in main_agent.stream_conversation(
                query, thread_id, run_id, "", config
            )
        ]
        return chunks[-1]["answer"]["messages"][-1].content

    async def scenario():
        assert await run_once("第一问", "old-thread", "run-1") == "之前的提问 | 第一问"
        assert await run_once("第二问", "old-thread", "run-2") == (
            "之前的提问 | 第一问 | 第二问"
        )
        assert await run_once("别的会话", "other-thread", "run-3") == "别的会话"

        async with open_checkpointer() as saver:
            state = await saver.aget_tuple(
                {"configurable": {"thread_id": "old-thread"}}
            )
            assert state is not None
            messages = state.checkpoint["channel_values"]["messages"]
            memory_messages = [
                message for message in messages
                if isinstance(message, SystemMessage)
                and message.id == "application-memory-context"
            ]
            assert len(memory_messages) == 1
            assert "相关长期记忆" in memory_messages[0].content

        await delete_thread_checkpoint("old-thread")
        async with open_checkpointer() as saver:
            assert await saver.aget_tuple(
                {"configurable": {"thread_id": "old-thread"}}
            ) is None

    asyncio.run(scenario())


def test_real_deep_agent_compiles_with_sqlite_checkpointer(monkeypatch, tmp_path):
    monkeypatch.setenv("CHECKPOINT_DB_PATH", str(tmp_path / "compile.db"))

    async def scenario():
        async with open_checkpointer() as saver:
            graph = main_agent.create_main_agent(saver)
            assert graph.checkpointer is saver

    asyncio.run(scenario())
