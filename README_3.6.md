# 大作业 3.6 文件聊天功能实现说明

## 功能简介
本部分实现了基于上传文本文件（txt）的文件聊天功能。用户上传txt文件后，AI助手会自动对文件内容进行归纳总结，并支持后续基于该文件内容的问答。

## 主要功能点

1. **文件上传与内容读取**
   - 支持用户上传txt文件，自动读取文件内容并存储在`current_file_text`变量中。
   - 其他类型文件仅展示文件名，不做内容处理。

2. **自动归纳总结**
   - 上传txt文件后，自动调用`pdf.py`中的`generate_summary`函数生成总结型prompt。
   - 调用`generate_text`函数获取AI助手对文件内容的总结，并将结果展示在聊天界面。
   - 聊天记录（history）和API调用上下文（messages）均会同步更新。

3. **基于文件内容的问答**
   - 用户可通过输入`/file 问题内容`的指令，向AI助手提问与上传文件内容相关的问题。
   - 系统会自动调用`generate_question`生成基于文件内容和用户问题的prompt，并用`generate_text`获取AI回复。
   - 若未上传txt文件，AI助手会提示用户先上传文件。

4. **数据结构说明**
   - `history`：用于界面展示的聊天记录，格式为`[(user, assistant), ...]`。
   - `messages`：用于与大模型API交互的消息上下文，格式为OpenAI风格的字典列表。
   - `current_file_text`：存储当前上传txt文件的全部内容。

## 主要代码说明

- `add_file`：处理文件上传，自动读取txt内容并生成总结，更新history和messages。
- `bot`：处理用户输入，识别`/file`指令并基于文件内容生成AI回复。
- `pdf.py`：包含`generate_summary`、`generate_question`、`generate_text`等辅助函数，负责prompt生成和AI回复。

## 使用说明
1. 上传txt文件后，AI助手会自动总结文件内容。
2. 输入`/file 你的问题`，AI助手会基于上传的txt内容进行回答。
3. 若未上传txt文件，使用`/file`指令会收到提示。

## 详细功能实现说明

### 1. generate_text（pdf.py）
- 功能：
  - 该函数接收 summary_prompt 或 question 作为参数，调用本地大模型（如LocalAI）接口进行内容补全。
  - 支持流式输出（generator），即AI助手可以边生成边返回内容，提升交互体验。
- 实现要点：
  - 通过HTTP请求调用本地API，获取AI回复。
  - 若API不可用，返回模拟内容，保证流程完整。

### 2. generate_summary（pdf.py）
- 功能：
  - 该函数接收 current_file_text（上传txt文件的全部内容），生成归纳总结型的prompt（summary_prompt）。
  - prompt格式为“Please summarize the following text content: ... Provide a concise summary of the main points。”
- 实现要点：
  - 只需拼接字符串即可，便于后续直接传递给AI模型。

### 3. generate_question（pdf.py）
- 功能：
  - 该函数接收 current_file_text 和 content（用户问题），生成基于文件内容和用户问题的提问prompt（question）。
  - prompt格式为“Based on the following text content, please answer the question: ... Text content: ... Please provide a detailed answer based on the given text。”
- 实现要点：
  - 只需拼接字符串即可，便于后续直接传递给AI模型。

### 4. app.py 文件聊天主流程
- 上传txt文件时：
  1. 读取文件内容存入 current_file_text。
  2. 调用 generate_summary 生成 summary_prompt，并加入 messages。
  3. 调用 generate_text 获取AI总结内容，并加入 messages。
  4. 将上传和总结结果展示在 history 聊天界面。
- 用户输入 /file 问题时：
  1. 检查 current_file_text 是否存在。
  2. 调用 generate_question 生成 question，并更新 messages。
  3. 调用 generate_text 获取AI基于文件内容的回复，并加入 messages。
  4. 将问答结果展示在 history 聊天界面。
- 所有AI回复均支持流式输出。

---


