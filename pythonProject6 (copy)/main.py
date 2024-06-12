import cv2
import numpy as np

# Örnek görüntü dosyalarını yükle
image_paths = ["Image1.jpg", "Image2.jpg", "Image3.jpg"]
images = [cv2.imread(path, cv2.IMREAD_GRAYSCALE) for path in image_paths]


def shi_tomasi_corner_detection(image, threshold=0.01):
    # Shi-Tomasi köşe tespiti parametreleri
    corners = cv2.goodFeaturesToTrack(image, maxCorners=100, qualityLevel=threshold,
                                      minDistance=10)
    corners = np.int0(corners)
    return corners


def harris_corner_detection(image, alpha=0.04):
    # Harris köşe tespiti parametreleri
    dst = cv2.cornerHarris(image, blockSize=2, ksize=3, k=alpha)
    corners = np.where(dst > 0.01 * dst.max())  # Köşeleri belirli bir eşik değerine göre seç
    return np.column_stack((corners[1], corners[0]))


def custom_corner_detection(image, alpha=0.04):
    # Özelleştirilmiş köşe tespiti
    # Hesaplamaları burada yapabilirsiniz (örneğin, eigenvalues)
    # Örneğin:
    eigenvalues = np.linalg.eigvals(H)  # H ise Hessian matrisi
    f_measure = eigenvalues[0] * eigenvalues[1] - alpha * (eigenvalues[0] + eigenvalues[1])
    corners = np.where(f_measure > 0)  # Köşeleri seç
    return np.column_stack((corners[1], corners[0]))


# Her bir görüntü için köşeleri bul ve çiz
for idx, image in enumerate(images):
    # Shi-Tomasi köşe tespiti
    corners_shi_tomasi = shi_tomasi_corner_detection(image)
    img_shi_tomasi = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    for corner in corners_shi_tomasi:
        x, y = corner.ravel()
        cv2.circle(img_shi_tomasi, (x, y), 3, (0, 0, 255), -1)

    # Harris köşe tespiti
    corners_harris = harris_corner_detection(image)
    img_harris = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    for corner in corners_harris:
        x, y = corner.ravel()
        cv2.circle(img_harris, (x, y), 3, (0, 255, 0), -1)

    # Özelleştirilmiş köşe tespiti
    corners_custom = custom_corner_detection(image)
    img_custom = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    for corner in corners_custom:
        x, y = corner.ravel()
        cv2.circle(img_custom, (x, y), 3, (255, 0, 0), -1)

    # Sonuçları göster
    cv2.imshow(f"Shi-Tomasi Corner Detection {idx + 1}", img_shi_tomasi)
    cv2.imshow(f"Harris Corner Detection {idx + 1}", img_harris)
    cv2.imshow(f"Custom Corner Detection {idx + 1}", img_custom)

cv2.waitKey(0)
cv2.destroyAllWindows()
















