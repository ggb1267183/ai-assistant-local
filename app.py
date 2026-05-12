import gradio as gr
import os
import time
from chat import chat  # 导入chat函数
from bs4 import BeautifulSoup  
from search import search  # 导入search函数
from fetch import fetch  # 导入fetch函数
from image_generate import image_generate  # 导入图片生成函数
from mnist import image_classification  # 导入图片分类函数

# Chatbot demo with multimodal input (text, markdown, LaTeX, code blocks, image, audio, & video). Plus shows support for streaming text.
messages = []
current_file_text = None
is_image_generation = False  # 标记是否为图片生成请求
is_image_classification = False  # 标记是否为图片分类请求
current_uploaded_file = None  # 存储当前上传的文件


def add_text(history, text):
    """
    处理用户输入的文本，支持搜索指令、图片生成指令和文件问答指令
    """
    global is_image_generation
    is_image_generation = False  # 重置标记
    
    history = history + [(text, None)]
    
    # 处理 /image 指令
    if text.startswith("/image "):
        # 提取图片描述内容
        content = text[7:]  
        
        # 设置图片生成标记
        is_image_generation = True  

        # 记录用户请求到 messages
        messages.append({"role": "user", "content": text})
        
    # 处理 /fetch 指令
    elif text.startswith("/fetch "):
        url = text[7:]
        # 调用 fetch 提取 p 标签内容
        page_content = fetch(url)
        # 构造符合文档要求的 prompt
        question = f"Act as a summarizer. Please summarize {url}. The following is the content:\n\n{page_content}"
        messages.append({"role": "user", "content": question})
        
    # 处理 /search 指令
    elif text.startswith("/search "):
        # 提取搜索内容
        search_content = text[8:]  
        
        # 调用search函数获取处理后的查询
        processed_query = search(search_content)
        
        # 更新messages用于传递给语言模型（使用处理后的查询）
        messages.append({"role": "user", "content": processed_query})
        
    # 处理 /file 指令
    elif text.startswith("/file "):
        # 记录用户请求到 messages
        messages.append({"role": "user", "content": text})
        
    else:
        # 普通文本，直接添加到messages
        messages.append({"role": "user", "content": text})
    
    return history, gr.update(value="", interactive=False)


def add_file(history, file):
    """
    处理文件上传，支持PNG图片分类和TXT文件处理
    """
    global is_image_classification, current_uploaded_file, current_file_text, messages
    
    filename = file.name
    
    # 检查是否为PNG图片
    if filename.lower().endswith('.png'):
        # 设置图片分类标记
        is_image_classification = True
        current_uploaded_file = file
        
        # 更新messages，用户内容为"Please classify {filename}"
        filename = os.path.basename(file.name)
        messages.append({"role": "user", "content": f"Please classify {filename}"})
        
        # 在history中显示上传的图片
        history = history + [((file.name,), None)]
        
    # 检查是否为TXT文件
    elif filename.lower().endswith('.txt'):
        try:
            with open(file.name, 'r', encoding='utf-8') as f:
                current_file_text = f.read()
        except Exception as e:
            current_file_text = None
            
        # 自动生成总结
        try:
            from pdf import generate_summary, generate_text
            # 生成总结型prompt
            summary_prompt = generate_summary(current_file_text or "")
            messages.append({"role": "user", "content": summary_prompt})
            
            # 获取总结内容（流式/非流式均可）
            summary_response = ""
            for chunk in generate_text(summary_prompt):
                summary_response += chunk
            messages.append({"role": "assistant", "content": summary_response})
            
            # 展示在界面上的history
            history = history + [(f"Uploaded and summarized: {os.path.basename(filename)}", summary_response)]
        except Exception as e:
            print(f"生成总结失败: {e}")
            history = history + [(f"Uploaded: {os.path.basename(filename)}", "文件上传成功，但生成总结时出现错误。")]
            
    else:
        # 其他文件类型默认展示文件名
        history = history + [((file.name,), None)]
    
    return history


def bot(history):
    """
    调用语言模型生成回复或处理图片生成/分类/文件问答
    """
    global is_image_generation, is_image_classification, current_uploaded_file, current_file_text, messages
    
    if not history:
        return history
        
    last_user_message = history[-1][0] if isinstance(history[-1], tuple) else None
    
    # 如果是图片生成请求
    if is_image_generation:
        # 获取最后一条用户消息，提取图片描述
        last_user_message = messages[-1]["content"]
        content = last_user_message[7:]  # 去掉 "/image " 前缀
        
        # 调用图片生成函数
        image_url = image_generate(content)
        
        if image_url:
            # 更新 history 显示图片
            history[-1][1] = f"![Generated Image]({image_url})" # 用元组格式总是报错，故改用markdown格式

            # 更新 messages 记录 AI 回复
            messages.append({"role": "assistant", "content": image_url})
        else:
            # 图片生成失败
            error_message = "抱歉，无法生成图片，请稍后重试。"
            history[-1][1] = error_message
            messages.append({"role": "assistant", "content": error_message})
        
        is_image_generation = False  # 重置图片生成标记
        yield history
        return history
    
    # 如果是图片分类请求
    elif is_image_classification:
        # 调用图片分类函数
        classification_result = image_classification(current_uploaded_file)
        
        # 更新 history 显示分类结果
        history[-1][1] = f"Classification result: {classification_result}"
        
        # 更新 messages 记录 AI 回复
        messages.append({"role": "assistant", "content": f"Classification result: {classification_result}"})
        
        # 重置标记和文件
        is_image_classification = False
        current_uploaded_file = None
        yield history
        return history
    
    # 检查是否是文件问答命令
    elif isinstance(last_user_message, str) and last_user_message.startswith('/file '):
        content = last_user_message[6:]
        if not current_file_text:
            response = "Please upload a text file first before using the /file command."
            history[-1] = (last_user_message, response)
            messages.append({"role": "assistant", "content": response})
            yield history
            return history
            
        try:
            from pdf import generate_question, generate_text
            # 生成基于文件内容和用户问题的prompt
            question = generate_question(current_file_text, content)
            if messages and messages[-1]["role"] == "user":
                messages[-1]["content"] = question
                
            # 获取AI回复
            response = ""
            for chunk in generate_text(question):
                response += chunk
            messages.append({"role": "assistant", "content": response})
            history[-1] = (last_user_message, response)
            yield history
            return history
        except Exception as e:
            error_response = f"处理文件问答时出现错误: {e}"
            history[-1] = (last_user_message, error_response)
            messages.append({"role": "assistant", "content": error_response})
            yield history
            return history
    
    # 普通聊天请求，调用语言模型
    else:
        # 调用chat函数获取流式生成器
        stream_generator = chat(messages)
        
        full_response = ""
        # 逐次获取流式输出内容，更新history
        for chunk in stream_generator:
            full_response += chunk
            history[-1][1] = full_response
            yield history  # 每次yield更新后的history，实现前端流式显示
        
        # 全部内容获取完后，更新messages记录AI回复
        messages.append({"role": "assistant", "content": full_response})
        return history

def clear_chat():
    """
    清空聊天记录
    """
    global is_image_generation, is_image_classification, current_uploaded_file, current_file_text
    is_image_generation = False  # 重置图片生成标记
    is_image_classification = False  # 重置图片分类标记
    current_uploaded_file = None  # 重置上传文件
    current_file_text = None  # 重置文件文本
    messages.clear()  # 清空messages
    return []         # 清空chatbot显示

with gr.Blocks() as demo:
    chatbot = gr.Chatbot(
        [],
        elem_id="chatbot",
        avatar_images=(None, (os.path.join(os.path.dirname(__file__), "avatar.png"))),
    )

    with gr.Row():
        txt = gr.Textbox(
            scale=4,
            show_label=False,
            placeholder="Enter text and press enter, or upload files. Commands: /search [query] for web search, /image [description] for image generation, /file [question] for file Q&A. Upload: TXT files for summarization, PNG images for digit classification.",
            container=False,
        )
        clear_btn = gr.Button('Clear')
        btn = gr.UploadButton("📁", file_types=["image", "video", "audio", "text"])

    txt_msg = txt.submit(add_text, [chatbot, txt], [chatbot, txt], queue=False).then(
        bot, chatbot, chatbot
    )
    txt_msg.then(lambda: gr.update(interactive=True), None, [txt], queue=False)
    file_msg = btn.upload(add_file, [chatbot, btn], [chatbot], queue=False).then(
        bot, chatbot, chatbot
    )
    clear_btn.click(clear_chat, None, chatbot, queue=False)

demo.queue()
demo.launch()
