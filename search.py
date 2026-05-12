import requests
from bs4 import BeautifulSoup
from serpapi import GoogleSearch

def search(content: str):
    """
    使用SerpApi进行必应搜索，返回处理好的content+search results
    
    Args:
        content: 用户的搜索内容，如 "Who is Sun Wukong?"
        
    Returns:
        str: 组合后的提问，格式为 "Please answer {content} based on the search result:\n\n{search results}"
    """
    
    # 配置SerpApi参数
    params = {
        "engine": "bing",           # 使用必应搜索引擎
        "q": content,               # 搜索查询内容
        "api_key": "6278190df70111c77f4fb3b9827f5c23e3360fe79c74a3d149112bb55243f2d6"
    }
    
    try:
        # 调用SerpApi
        search_engine = GoogleSearch(params)
        results = search_engine.get_dict()
        
        # 提取第一条搜索结果的snippet
        search_results = ""
        if "organic_results" in results and len(results["organic_results"]) > 0:
            first_result = results["organic_results"][0]
            if "snippet" in first_result:
                search_results = first_result["snippet"]
            else:
                search_results = "No snippet available for the first search result."
        else:
            search_results = "No search results found."
        
        # 组合成有效的提问
        combined_question = f"Please answer {content} based on the search result:\n\n{search_results}"
        
        return combined_question
        
    except Exception as e:
        print(f"Search error: {e}")
        # 如果搜索失败，返回原始问题
        return f"I couldn't search for information, but I'll try to answer: {content}"


if __name__ == "__main__":
    # 测试函数
    result = search("Sun Wukong")
    print(result)