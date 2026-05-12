import os
import re
import requests
import json

def generate_text(prompt):
    """
    调用文字补全接口并返回内容（支持流式输出）
    """
    try:
        url = "http://localhost:8080/v1/completions"
        headers = {"Content-Type": "application/json"}
        data = {
            "model": "openllama",
            "prompt": prompt,
            "max_tokens": 1000,
            "temperature": 0.7,
            "stream": True
        }
        
        response = requests.post(url, headers=headers, json=data, stream=True)
        
        if response.status_code == 200:
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        try:
                            data_str = line[6:]  # 去掉 'data: '
                            if data_str.strip() == '[DONE]':
                                break
                            data = json.loads(data_str)
                            if 'choices' in data and len(data['choices']) > 0:
                                text = data['choices'][0].get('text', '')
                                if text:
                                    yield text
                        except json.JSONDecodeError:
                            continue
        else:
            yield f"Error: HTTP {response.status_code}"
            
    except Exception as e:
        yield f"Error: {str(e)}"

def generate_answer(current_file_text: str, content: str):
    """
    生成基于文件内容的问题
    """
    question = f"""Based on the following text content, please answer the question: {content}

Text content:
{current_file_text}

Please provide a detailed answer based on the given text."""
    return question

def generate_summary(current_file_text: str):
    """
    生成对文件内容进行归纳总结的提问
    """
    summary_prompt = f"""Please summarize the following text content:

{current_file_text}

Provide a concise summary of the main points."""
    return summary_prompt

def generate_question(current_file_text: str, content: str):
    """
    生成基于文件内容和用户问题的完整提问
    """
    question = f"""Based on the following text content, please answer the question: {content}

Text content:
{current_file_text}

Please provide a detailed answer based on the given text."""
    return question

if __name__ == "__main__":
    prompt = generate_question("Hello", "Who is Sun Wukong?")
    for chunk in generate_text(prompt):
        print(chunk, end='', flush=True)