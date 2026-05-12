# 基于LocalAI的多模态AI助手系统
清华大学软件学院程序设计实践课程大作业  
课程成绩：**A** | 4人小组项目

---

## 一、项目背景
在大模型应用快速发展的背景下，现有主流大模型服务大多依赖外部云平台，存在隐私泄露、网络依赖和使用成本高等问题。为解决这些痛点，本项目基于LocalAI构建了一套**完全本地化运行**的多模态AI助手系统，所有计算均在本地完成，无需依赖外部云服务，同时提供类似ChatGPT的交互体验。

---

## 二、技术栈
| 类别 | 技术/工具 |
| :--- | :--- |
| 核心框架 | Python 3.12 + Docker + LocalAI |
| 大模型接口 | OpenAI SDK（兼容LocalAI API） |
| 前端界面 | Gradio |
| 网络功能 | SerpApi（必应搜索）、Requests、BeautifulSoup |
| 视觉处理 | PyTorch、TorchVision、PIL |
| 部署方式 | 本地Docker容器化部署 |

---

## 三、核心功能模块
### 1. 基础对话功能
- 基于LocalAI部署的gpt-3.5-turbo兼容模型实现基础文本对话
- 完整维护对话历史记录，支持上下文理解与多轮连续对话
- 实现完善的异常捕获与错误处理机制，保证系统稳定性

### 2. 流式输出响应
- 实现模型边生成边输出的流式传输功能
- 将用户平均等待时间从8秒降低至2秒，大幅提升交互体验
- 所有功能模块（搜索、网页总结、文件聊天）均支持流式输出

### 3. 网络搜索增强
- 通过`/search [关键词]`指令触发实时网络搜索
- 调用SerpApi必应搜索接口获取最新信息
- 自动将搜索结果注入对话上下文，解决大模型知识时效性问题

### 4. 网页内容总结
- 通过`/fetch [网页URL]`指令触发网页内容解析与总结
- 使用BeautifulSoup过滤HTML标签，提取网页核心正文
- 自动生成结构化内容摘要，支持流式返回结果

### 5. 本地图片生成
- 通过`/image [生成描述]`指令触发图片生成
- 调用LocalAI集成的Stable Diffusion模型
- 直接生成并返回256×256分辨率图片，无需额外服务

### 6. 文件聊天功能（本人负责）
- 支持上传TXT文本文件，自动读取并归纳文件核心内容
- 实现基于文件内容的问答交互，通过`/file [问题]`指令提问
- 自动维护文件上下文，支持多轮连续问答，适配长文本场景

### 7. 手写数字识别（附加功能）
- 支持上传PNG格式手写数字图片
- 使用本地训练的改进LeNet模型进行分类识别
- 识别准确率达98%以上，支持0-9共10个数字

---

## 四、项目分工
| 成员 | 负责模块 |
| :--- | :--- |
| 郭毅博（本人） | 文件聊天功能设计与实现、项目文档汇总、大作业录屏展示 |
| 杨潘星 | 基础对话功能、网络搜索功能 |
| 于恩希 | 流式传输功能、网页内容总结功能 |
| 宗沈祺 | 图片生成功能、手写数字识别功能 |

---

## 五、运行步骤
### 1. 环境准备
- 安装 **Docker Desktop**（用于运行LocalAI服务）
- 安装 **Anaconda/Miniconda**（用于Python环境管理）
- 预留至少20GB磁盘空间，用于存储模型文件

### 2. 安装Python依赖
```bash
# 创建并激活虚拟环境
conda create -n ai-assistant python=3.12
conda activate ai-assistant

# 安装项目依赖
pip install -r requirements.txt
```

### 3. 启动LocalAI服务
```bash
# 克隆LocalAI官方仓库
git clone https://github.com/go-skynet/LocalAI.git
cd LocalAI

# 启动Docker容器（后台运行）
docker compose up -d

# 等待模型自动下载完成（首次启动耗时较长）
```

### 4. 运行AI助手应用
```bash
# 回到项目根目录
cd ..

# 启动Gradio应用
python app.py
```

### 5. 访问交互界面
打开浏览器，访问：`http://127.0.0.1:7860`，即可使用所有功能。

---

## 六、项目结构
```text
ai-assistant-local/
├── app.py              # 主应用入口，Gradio界面与路由逻辑
├── chat.py             # 基础对话功能实现
├── search.py           # 网络搜索功能实现
├── fetch.py            # 网页内容解析与总结功能
├── image_generate.py   # 图片生成功能实现
├── pdf.py              # 文件聊天功能实现（本人负责）
├── mnist.py            # 手写数字识别功能入口
├── lenet.py            # LeNet模型定义与训练脚本
├── requirements.txt    # 项目依赖包列表
└── README.md           # 项目说明文档
```

---

## 七、项目亮点
1. **完全本地化运行**：所有计算均在本地完成，无外部网络依赖，保护用户隐私数据。
2. **模块化架构设计**：功能模块独立封装，易于扩展维护，可快速新增AI能力。
3. **流畅用户体验**：全功能支持流式输出，大幅降低用户等待时间。
4. **多能力一站式集成**：同时提供对话、搜索、总结、生成、识别等多种AI能力。
5. **高稳定性保障**：全链路异常捕获与错误处理，避免因网络/接口问题导致服务崩溃。

---

## 八、项目截图
<img width="1134" height="363" alt="图片生成1" src="https://github.com/user-attachments/assets/168bb756-fce0-4f0b-861c-958bfde85cce" />
<img width="2211" height="694" alt="绘图" src="https://github.com/user-attachments/assets/bbd8893d-57e4-42ff-86b5-7062110d7b02" />
<img width="2205" height="685" alt="fetch" src="https://github.com/user-attachments/assets/5d034dd3-3a9e-4960-98d7-62315bb17de8" />
<img width="2209" height="708" alt="AI问答2" src="https://github.com/user-attachments/assets/4171d1a5-136e-452b-934e-818c6272b7f3" />
<img width="2233" height="687" alt="图片分类" src="https://github.com/user-attachments/assets/98871426-5af4-4174-a23f-2d9654e7b1d2" />
<img width="2208" height="619" alt="流式输出2" src="https://github.com/user-attachments/assets/c6f100b5-0eb2-4cd1-8d8f-09baeefc6b1a" />
<img width="2220" height="697" alt="流式输出" src="https://github.com/user-attachments/assets/5bf45de8-dec4-4f99-a04f-b65f9ebfe140" />
<img width="2218" height="678" alt="search" src="https://github.com/user-attachments/assets/6b1bf989-8ecd-4c74-92ae-cb2a4082ce9f" />
<img width="2226" height="687" alt="AI问答1" src="https://github.com/user-attachments/assets/e1878d80-331d-42ef-b71b-a880aa570707" />


---

## 许可证
本项目为课程学习项目，仅供学习和研究使用，请勿用于商业用途。
```

---
