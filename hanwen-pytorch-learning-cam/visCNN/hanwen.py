import torch
import cv2, urllib
import numpy as np
from torchvision import models, transforms

# https://s0pytorch0org.icopy.site/hub/pytorch_vision_densenet/

# 预训练模型时会把权值下载到一个缓存文件夹
model = models.resnet18(pretrained=True)
model.eval()

# demo
url, filename = ("https://github.com/pytorch/hub/raw/master/dog.jpg", "dog.jpg")
try:
    urllib.URLopener().retrieve(url, filename)
except:
    urllib.request.urlretrieve(url, filename)

from PIL import Image

input_image = Image.open(filename)
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])
input_tensor = preprocess(input_image)
input_batch = input_tensor.unsqueeze(0)

# move the input and model to GPU for speed if available
if torch.cuda.is_available():
    input_batch = input_batch.to('cuda')
    model.to('cuda')
with torch.no_grad():
    output = model(input_batch)
# Tensor of shape 1000, with confidence scores over Imagenet's 1000 classes
final_result = output
# print(output[0])

# The output has unnormalized scores. To get probabilities, you can run a softmax on it.
# final_result = torch.nn.functional.softmax(output[0], dim=0)
# print(final_result)

# 研究内部结构
from torchsummary import summary

# summary(model, (3, 224, 224))

# 可视化网络
from torchviz import make_dot

vis_graph = make_dot(model(final_result), params=dict(model.named_parameters()))
vis_graph.view()
