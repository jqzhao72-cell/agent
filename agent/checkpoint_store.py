"""Persistent LangGraph checkpoints for conversation threads."""

import os
from contextlib import asynccontextmanager
from pathlib import Path

import aiosqlite
from dotenv import find_dotenv, load_dotenv
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver


load_dotenv(find_dotenv())

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def checkpoint_db_path() -> Path:
    configured = Path(os.getenv("CHECKPOINT_DB_PATH", "data/checkpoints.db"))
    path = configured if configured.is_absolute() else PROJECT_ROOT / configured
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


@asynccontextmanager
async def open_checkpointer():
    # Restrict checkpoint deserialization to LangGraph's safe message types.
    serializer = JsonPlusSerializer(allowed_msgpack_modules=None)
    async with aiosqlite.connect(str(checkpoint_db_path())) as connection:
        saver = AsyncSqliteSaver(connection, serde=serializer)
        yield saver


async def delete_thread_checkpoint(thread_id: str) -> None:
    async with open_checkpointer() as saver:
        # A chat may predate checkpointing, so the database can still be empty.
        await saver.setup()
        await saver.adelete_thread(thread_id)
