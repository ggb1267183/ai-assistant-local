import torch
import torch.nn.functional as F
import torchvision.transforms as transforms
from PIL import Image
import gradio as gr
from lenet import LeNet

def image_classification(file):
    """
    使用PyTorch和本地LeNet模型进行图片分类
    参数: file - 上传的PNG图片文件
    返回: 分类结果字符串
    """
    try:
        # 加载模型文件
        checkpoint = torch.load('lenet.pth', map_location='cpu', weights_only=True)
        
        # 检查模型文件的结构
        if isinstance(checkpoint, dict) and 'state_dict' in checkpoint:
            # 如果模型文件包含state_dict键，提取权重
            state_dict = checkpoint['state_dict']
        else:
            # 否则直接使用加载的数据作为state_dict
            state_dict = checkpoint
        
        # 创建模型实例并加载权重
        model = LeNet(num_classes=10)
        model.load_state_dict(state_dict)
        model.eval()
        
        # 图像预处理
        transform = transforms.Compose([
            transforms.Grayscale(num_output_channels=1),  # 转换为灰度图
            transforms.Resize((28, 28)),  # 调整大小为28x28
            transforms.ToTensor(),  # 转换为张量
            transforms.Normalize((0.1307,), (0.3081,))  # MNIST标准化参数
        ])
        
        # 加载和预处理图像
        image = Image.open(file.name)
        image_tensor = transform(image).unsqueeze(0)  # 添加batch维度
        
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