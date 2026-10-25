import os

from dotenv import load_dotenv

from agent.prompts import sub_agents_content


load_dotenv()
backend = os.getenv("KNOWLEDGE_BACKEND", "ragflow").strip().lower()

if backend == "docpilot":
    from tools.docpilot_tool import ask_knowledge_base, list_knowledge_bases

    tools = [list_knowledge_bases, ask_knowledge_base]
elif backend == "ragflow":
    from tools.ragflow_tools import create_ask_delete, get_assistant_list

    tools = [get_assistant_list, create_ask_delete]
else:
    raise ValueError("KNOWLEDGE_BACKEND 只支持 docpilot 或 ragflow")

knowledge_base_agent = {
    "name": sub_agents_content[backend]["name"],
    "description": sub_agents_content[backend]["description"],
    "system_prompt": sub_agents_content[backend]["system_prompt"],
    "tools": tools,
}
