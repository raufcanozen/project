import cv2
import numpy as np
from matplotlib import pyplot as plt


image_path = '/home/rauf/PycharmProjects/GiGodev5/face1.png'
img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
if img is None:
    raise ValueError("Görüntü dosyası yüklenemedi. Dosya yolunu ve dosya adını kontrol edin.")


plt.imshow(img, cmap='gray')
plt.title('Original Image')
plt.axis('off')
plt.show()

hessian_threshold = 400
surf = cv2.xfeatures2d.SURF_create(hessian_threshold)

keypoints, descriptors = surf.detectAndCompute(img, None)

img_with_keypoints = cv2.drawKeypoints(img, keypoints, None, (255, 0, 0), 4)

plt.imshow(img_with_keypoints, cmap='gray')
plt.title('Image with Keypoints')
plt.axis('off')
plt.show()

print(f"Number of keypoints detected: {len(keypoints)}")
print(f"Descriptor shape: {descriptors.shape}")
