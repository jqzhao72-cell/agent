# 目标： 创建网络搜索子智能体
# 方式1： dict -> deepagents  方式： compiledSubAgent -> langchain langgraph
from agent.prompts import sub_agents_content
from tools.aliyun_search_tool import internet_search


network_search_agent = {
    "name":sub_agents_content['network']['name'],
    "description":sub_agents_content['network']['description'],
    "system_prompt":sub_agents_content['network']['system_prompt'],
    "tools":[internet_search]
}
