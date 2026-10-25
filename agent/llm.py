from dotenv import load_dotenv,find_dotenv
import os
from langchain.chat_models import init_chat_model

# 加载配置文件
# find_dotenv() 确保找到 .env文件 递归查询当前项目文件夹
load_dotenv(find_dotenv())


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _deepseek_credentials() -> dict[str, str]:
    # 不回退到 OPENAI_API_KEY：该变量保留给阿里云联网搜索，避免把百炼 Key
    # 发送到 DeepSeek 官方接口。
    return {
        "api_key": os.getenv("DEEPSEEK_API_KEY", "").strip()
        or "missing-deepseek-api-key",
        "base_url": os.getenv(
            "DEEPSEEK_BASE_URL", "https://api.deepseek.com"
        ).strip()
        or "https://api.deepseek.com",
    }


def _deepseek_thinking(enabled: bool) -> dict:
    return {"thinking": {"type": "enabled" if enabled else "disabled"}}

model = init_chat_model(
    model=os.getenv("LLM_MAIN_MODEL", "deepseek-v4-pro"),
    model_provider="openai",
    extra_body=_deepseek_thinking(_env_bool("LLM_ENABLE_THINKING", False)),
    **_deepseek_credentials(),
)

# 子 Agent 只负责检索与整理，默认使用更快、更便宜的模型。
fast_model = init_chat_model(
    model=os.getenv("SUBAGENT_MODEL")
    or os.getenv("ALIYUN_SUBAGENT_MODEL")
    or "deepseek-flash",
    model_provider="openai",
    extra_body=_deepseek_thinking(False),
    **_deepseek_credentials(),
)
