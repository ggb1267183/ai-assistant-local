import os
import requests
import json


def image_generate(content: str):
    """
    调用 LocalAI 的 stable diffusion API 生成图片
    参数:
        content: 图片描述内容
    返回:
        生成的图片地址 URL
    """
    try:
        # LocalAI 图片生成接口地址
        url = "http://localhost:8080/v1/images/generations"
        
        # 请求参数
        payload = {
            "prompt": content,
            "size": "256x256",
            "n": 1  # 生成图片数量
        }
        
        # 发送请求
        headers = {
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        if response.status_code == 200:
            result = response.json()
            # 获取生成的图片 URL
            image_url = result["data"][0]["url"]
            return image_url
        else:
            print(f"图片生成失败，状态码: {response.status_code}")
            print(f"错误信息: {response.text}")
            return None
            
    except Exception as e:
        print(f"图片生成过程中出现错误: {e}")
        return None


if __name__ == "__main__":
    image_generate('A cute baby sea otter')