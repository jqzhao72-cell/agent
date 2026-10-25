"""向后兼容模块：网络搜索已改用阿里云百炼。"""

from tools.aliyun_search_tool import internet_search

__all__ = ["internet_search"]
