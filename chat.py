import os
from openai import OpenAI

def chat(messages):
    print(messages)
    
    # 配置OpenAI客户端连接到本地LocalAI
    client = OpenAI(
        base_url="http://localhost:8080/v1",  # LocalAI的API地址
        api_key="not-needed"  # 本地模型不需要真实的API key
    )
    
    try:
        # 调用chat completions接口
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # 使用LocalAI中配置的模型名
            messages=messages,      # 传入完整的对话历史
            temperature=0.7,        # 控制回复的随机性
            stream=True             #开启流式传输
        )
        
        def stream_generator():
            for chunk in response:
                content = chunk.choices[0].delta.content
                if content:  
                    yield content
        return stream_generator()
                    
        
        
        
    except Exception as e:
        print(f"Error calling chat model: {e}")
        return "Sorry, I encountered an error while processing your request."
