# AI助手项目 - 功能实现说明文档 - 2024012733 - 宗沈祺

## 项目概述

本文档详细说明了AI助手项目中 **功能3.5（图片生成）** 和 **功能3.7（图片分类）** 的实现过程和技术细节。

---

## 功能3.5：图片生成（20分）

### 功能描述

实现AI助手的图片生成功能，用户可以通过 `/image [图片描述]` 指令触发图片生成。系统会调用本地 LocalAI 的 Stable Diffusion API 生成图片，并在聊天界面中显示生成结果。

### 实现详情

#### 1. image_generate.py 实现

**文件路径**：`image_generate.py`

**主要功能**：

- 接收图片描述内容作为参数
- 调用本地 LocalAI 的 Stable Diffusion API
- 返回生成的图片 URL 地址
- 提供完整的错误处理

**核心代码实现**：

```python
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
            "n": 1
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
```

**技术要点**：

- 使用 `requests` 库调用 LocalAI 的图片生成 API
- 正确配置 API 端点为 `/v1/images/generations`
- 设置图片尺寸为 `256x256` 像素
- 实现完整的 HTTP 状态码检查
- 提供详细的错误日志输出

#### 2. app.py 集成

**文件路径**：`app.py`

**主要修改**：

- 导入 `image_generate` 函数
- 修改 `add_text` 函数识别 `/image` 指令
- 实现指令解析和内容提取
- 在 `bot` 函数中处理图片生成请求
- 正确显示生成的图片

**关键实现**：

```python
def add_text(history, text):
    # 处理 /image 指令
    if text.startswith("/image "):
        content = text[7:]  # 提取图片描述内容
        is_image_generation = True  # 设置图片生成标记
        messages.append({"role": "user", "content": text})
    # ... 其他指令处理

def bot(history):
    # 如果是图片生成请求
    if is_image_generation:
        last_user_message = messages[-1]["content"]
        content = last_user_message[7:]  # 去掉 "/image " 前缀

        # 调用图片生成函数
        image_url = image_generate(content)

        if image_url:
            # 更新 history 显示图片
            history[-1][1] = f"![Generated Image]({image_url})"
            messages.append({"role": "assistant", "content": image_url})
        else:
            # 图片生成失败
            error_message = "抱歉，无法生成图片，请稍后重试。"
            history[-1][1] = error_message
            messages.append({"role": "assistant", "content": error_message})
```

**数据处理逻辑**：

- **指令识别**：检测 `/image ` 开头的用户输入
- **内容提取**：从指令中提取图片描述内容
- **API 调用**：调用 LocalAI 的 Stable Diffusion API
- **结果处理**：成功时显示图片，失败时显示错误信息
- **历史记录**：正确维护 `messages` 和 `history` 变量

**指令格式**：

- 图片生成：`/image A cute baby sea otter`

---

### API 接口说明

#### LocalAI Stable Diffusion API

**接口地址**：`http://localhost:8080/v1/images/generations`

**请求方法**：POST

**请求参数**：

```json
{
  "prompt": "图片描述内容",
  "size": "256x256",
  "n": 1
}
```

**响应格式**：

```json
{
  "data": [
    {
      "url": "生成的图片URL地址"
    }
  ]
}
```

**参数说明**：

- `prompt`：图片描述文本，指导图片生成
- `size`：生成图片的尺寸，固定为 `256x256`
- `n`：生成图片的数量，固定为 `1`

### 测试说明

#### 图片生成测试

- 输入：`/image generate a picture of an apple`
- 预期：生成并显示苹果图片

#### 错误处理测试

- 当 LocalAI 服务未启动时，输入 `/image test`
- 预期：显示错误信息“抱歉，无法生成图片，请稍后重试。”

### 使用说明

#### 环境要求

1. **LocalAI 服务**：需要在 `localhost:8080` 端口运行
2. **Stable Diffusion 模型**：需要在 LocalAI 中配置并启动
3. **Python 依赖**：`requests` 库

#### 使用方法

1. 启动 LocalAI 服务并加载 Stable Diffusion 模型
2. 运行 `app.py` 启动 Web 界面
3. 在输入框中输入 `/image [图片描述]`
4. 系统将生成并显示相应的图片

#### 注意事项

- 图片生成需要一定时间
- 确保 LocalAI 服务正常运行
- 图片描述越详细，生成效果越好

---

## 功能3.7：图片分类（附加分 10分）

### 功能描述

实现 AI 助手的手写数字分类功能，用户可以通过上传 PNG 格式的手写数字图片，系统会调用本地训练的改进 LeNet 模型进行图片分类，并返回 0-9 的数字识别结果。

### 实现详情

#### 1. mnist.py 实现

**文件路径**：`mnist.py`

**主要功能**：

- 接收上传的 PNG 图片文件
- 加载预训练的改进 LeNet 模型
- 进行图像预处理和标准化
- 执行数字分类预测
- 返回分类结果

**核心代码实现**：

```python
import torch
import torch.nn.functional as F
import torchvision.transforms as transforms
from PIL import Image
import gradio as gr
from lenet import LeNet


def image_classification(file):
    """
    使用 PyTorch 和本地 LeNet 模型进行图片分类
    参数: file - 上传的 PNG 图片文件
    返回: 分类结果字符串
    """
    try:
        # 加载模型文件
        checkpoint = torch.load('LocalAI/models/lenet.pth', map_location='cpu', weights_only=True)

        # 检查模型文件的结构
        if isinstance(checkpoint, dict) and 'state_dict' in checkpoint:
            # 如果模型文件包含 state_dict 键，提取权重
            state_dict = checkpoint['state_dict']
        else:
            # 否则直接使用加载的数据作为 state_dict
            state_dict = checkpoint

        # 创建模型实例并加载权重
        model = LeNet(num_classes=10)
        model.load_state_dict(state_dict)
        model.eval()

        # 图像预处理
        transform = transforms.Compose([
            transforms.Grayscale(num_output_channels=1),
            transforms.Resize((28, 28)),
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))
        ])

        # 加载和预处理图像
        image = Image.open(file.name)
        image_tensor = transform(image).unsqueeze(0)

        # 进行预测
        with torch.no_grad():
            outputs = model(image_tensor)
            probabilities = F.softmax(outputs, dim=1)
            predicted_class = torch.argmax(probabilities, dim=1).item()
            confidence = probabilities[0][predicted_class].item()

        # 返回结果
        return predicted_class

    except Exception as e:
        return f"Classification result: error - {str(e)}"
```

**技术要点**：

- 使用 PyTorch 加载预训练的改进 LeNet 模型
- 实现完整的图像预处理流程
- 支持模型文件的不同保存格式
- 使用 MNIST 数据集的标准化参数
- 提供详细的错误处理和日志输出

#### 2. lenet.py 模型定义

**文件路径**：`lenet.py`

**主要功能**：

- 定义改进的 LeNet 卷积神经网络架构
- 包含 3 个卷积层和 1 个全连接层
- 使用 BatchNorm 和 ReLU 激活函数
- 支持可配置的输出类别数

**核心代码实现**：

```python
import torch


class LeNet(torch.nn.Module):
    def __init__(self, num_classes=10):
        super(LeNet, self).__init__()

        # 第一个卷积层
        self.layer1 = torch.nn.Sequential(
            torch.nn.Conv2d(1, 16, kernel_size=5, stride=1, padding=2),
            torch.nn.BatchNorm2d(16),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(kernel_size=2, stride=2))

        # 第二个卷积层
        self.layer2 = torch.nn.Sequential(
            torch.nn.Conv2d(16, 32, kernel_size=5, stride=1, padding=2),
            torch.nn.BatchNorm2d(32),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(kernel_size=2, stride=2))

        # 第三个卷积层
        self.layer3 = torch.nn.Sequential(
            torch.nn.Conv2d(32, 64, kernel_size=5, stride=1, padding=2),
            torch.nn.BatchNorm2d(64),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(kernel_size=2, stride=2))

        # 全连接层
        self.fc = torch.nn.Linear(3 * 3 * 64, num_classes)

    def forward(self, x):
        out = self.layer1(x)
        out = self.layer2(out)
        if self.layer3 is not None:
            out = self.layer3(out)
        out = out.reshape(out.size(0), -1)
        out = self.fc(out)
        return out
```

#### 3. app.py 集成

**文件路径**：`app.py`

**主要修改**：

- 导入 `image_classification` 函数
- 修改 `add_file` 函数识别 PNG 图片上传
- 实现图片分类标记和文件存储
- 在 `bot` 函数中处理图片分类请求
- 正确显示分类结果

**关键实现**：

```python
def add_file(history, file):
    """
    处理文件上传，支持 PNG 图片分类和 TXT 文件处理
    """
    global is_image_classification, current_uploaded_file, current_file_text, messages

    filename = file.name

    # 检查是否为 PNG 图片
    if filename.lower().endswith('.png'):
        # 设置图片分类标记
        is_image_classification = True
        current_uploaded_file = file

        # 更新 messages，用户内容为 "Please classify {filename}"
        filename = os.path.basename(file.name)
        messages.append({"role": "user", "content": f"Please classify {filename}"})

        # 在 history 中显示上传的图片
        history = history + [((file.name,), None)]


def bot(history):
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
```

**数据处理逻辑**：

- **文件类型检测**：识别 PNG 格式的图片文件
- **分类标记设置**：设置 `is_image_classification` 标记
- **文件存储**：将上传的文件存储在 `current_uploaded_file` 变量中
- **模型调用**：调用 `image_classification` 函数进行预测
- **结果展示**：在聊天界面显示分类结果
- **状态重置**：处理完成后重置相关标记

### 测试说明

#### 手写数字分类测试

- 上传：手写数字 `0` 的 PNG 图片
- 预期：返回分类结果 `0`

### 使用说明

#### 环境要求

**Python 环境**：Python 3.12.4

#### 安装依赖

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

#### 使用方法

1. 启动 `app.py` 运行 Web 界面
2. 点击上传按钮选择 PNG 格式的手写数字图片
3. 系统自动进行图像预处理和分类
4. 在聊天界面查看分类结果

#### 注意事项

- 只支持 PNG 格式的图片文件
- 图片会被自动转换为 28x28 像素的灰度图
- 确保上传的是手写数字图片以获得准确结果
- 模型文件必须存在于指定路径
- 分类结果范围为 0-9 的数字

---

## 其他说明

### 文件修改汇总

1. **image_generate.py** - 实现图片生成功能的核心逻辑
2. **mnist.py** - 实现图片分类功能的核心逻辑
3. **lenet.py** - 改进的 LeNet 模型定义
4. **app.py** - 集成图片生成、图片分类功能到主程序

### 依赖配置

- **requests**：用于 HTTP API 调用
- **json**：用于 JSON 数据处理
- **LocalAI 服务**：需要本地运行 Stable Diffusion 模型
- **PyTorch**：深度学习框架
- **torchvision**：计算机视觉工具包
- **PIL (Pillow)**：图像处理库
- **LeNet 模型文件**：需要预训练的 `lenet.pth` 文件

---

## 个人贡献说明

### 负责的功能模块

- **图片生成功能**：基于 LocalAI 和 Stable Diffusion
- **手写数字分类功能**：基于 PyTorch 和改进的 LeNet 模型

### 具体工作内容

1. **需求分析**：理解图片生成、手写数字分类功能的技术要求
2. **API 研究**：学习 LocalAI 的图片生成 API 接口；学习导入 LeNet 模型架构和 PyTorch 使用
3. **代码实现**：完整实现 `image_generate.py`、`mnist.py` 的核心功能
4. **系统集成**：在 `app.py` 中正确集成图片生成、图片分类功能
5. **错误处理**：实现完整的异常处理和用户反馈

---

## 技术总结

### 主要技术栈

- **Python**：主要开发语言
- **PyTorch**：深度学习框架
- **torchvision**：计算机视觉工具包
- **PIL (Pillow)**：图像处理库
- **requests**：HTTP API 调用
- **Gradio**：Web 界面框架

### 核心技术要点

#### image_generate.py

1. **HTTP API 集成**：RESTful API 调用 LocalAI 的 Stable Diffusion 服务
2. **JSON 数据处理**：请求参数构造和响应解析
3. **错误处理机制**：完整的异常捕获和状态码检查
4. **本地模型调用**：通过 LocalAI 调用本地 Stable Diffusion 模型

#### mnist.py

1. **PyTorch 模型加载**：预训练权重的序列化和反序列化
2. **图像预处理流水线**：灰度化、缩放、标准化、张量化
3. **深度学习推理**：使用 `torch.no_grad()` 进行高效推理
4. **概率分布处理**：使用 softmax 获取分类概率

### 代码质量

- 代码结构清晰，功能模块化
- 遵循作业文档的技术规范
- 实现了文档要求的所有核心功能点
- 完整的异常处理机制，详细的错误日志输出
