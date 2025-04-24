import torchxrayvision as xrv
import torchvision.transforms as transforms
from PIL import Image
import io
import torch

model = xrv.models.DenseNet(weights="densenet121-res224-all")
model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485], [0.229])
])

def analyze_xray(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert('L')
    img_tensor = transform(img).unsqueeze(0)
    with torch.no_grad():
        preds = model(img_tensor)
    return {k: float(preds[0][i]) for i, k in enumerate(model.pathologies)}
