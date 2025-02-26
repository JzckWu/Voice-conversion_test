import torch

# Tensor X: 20 images of size 128x128
X = torch.randn(128, 128, 20)  

# Tensor w: weights corresponding to image dimensions
w = torch.randn(128, 128)      

y = X.T @ w

print("X shape:", X.shape)  # (20, 128, 128)
print("w shape:", w.shape)  # (128, 128)