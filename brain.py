import base64
import torchxrayvision as xrv
from torchvision import transforms
import torch
import skimage.io

# Load and encode the image
image_path = "person100_bacteria_475.jpeg"
with open(image_path, "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

# Decode the image for processing
decoded_image_path = "decoded_lungs.jpeg"
with open(decoded_image_path, "wb") as decoded_file:
    decoded_file.write(base64.b64decode(encoded_image))

# Load the image using skimage
img = skimage.io.imread(decoded_image_path)
img = xrv.datasets.normalize(img, 255)

# Ensure the image is 2D (grayscale)
if len(img.shape) > 2:
    img = img[:, :, 0]
if len(img.shape) < 2:
    raise ValueError("Error: Image dimension is lower than 2.")

# Add a color channel
img = img[None, :, :]

# Preprocess the image
transform = transforms.Compose([
    xrv.datasets.XRayCenterCrop(),  # Center crop the X-ray image
    xrv.datasets.XRayResizer(224),  # Resize to 224x224
])
img = transform(img)

# Load the torchxrayvision model from Hugging Face
model_name = "densenet121-res224-mimic_ch"
model = xrv.models.get_model(model_name)
model.eval()

# Perform inference
with torch.no_grad():
    img_tensor = torch.from_numpy(img).unsqueeze(0)
    preds = model(img_tensor).cpu()

# Map the outputs to the model's labels
predictions = {
    pathology: float(prob)
    for pathology, prob in zip(xrv.datasets.default_pathologies, preds[0].detach().numpy())
}

# Print the predictions
print("Predicted pathologies and probabilities:")
for pathology, probability in predictions.items():
    print(f"{pathology}: {probability:.4f}")