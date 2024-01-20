import numpy as np
import cv2

def add_gaussian_noise(image, mean, sigma):
    noise = np.random.normal(mean, sigma, image.shape).astype(np.uint8)
    noisy_image = cv2.add(image, noise)
    return noisy_image

# ファイルパスを指定
image_path = '/Users/hanya/Documents/01スクリーンショット/ochi2.jpg'
image = cv2.imread(image_path)

# ノイズの平均と標準偏差を引数で指定（この場合は平均0、標準偏差5）
noisy_image = add_gaussian_noise(image, mean=0, sigma=5)

# ノイズが加えられた画像を指定したフォルダに保存
output_path = '/Users/hanya/Documents/01スクリーンショット/noisy_ochi2260.jpg'
cv2.imwrite(output_path, noisy_image)

# ノイズが加えられた画像を表示(確認用）
cv2.imshow('Noisy Image', noisy_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 画像を読み込ませる
image_path = '/Users/hanya/Documents/01スクリーンショット/noisy_ochi2260.jpg'
image = cv2.imread(image_path)

# カーネルサイズ
ksize = (5, 5)

# 標準偏差の候補の配列
sigmas = [5, 10, 15, 20, 25]

for i in sigmas:
    # ガウシアンフィルタを適用
    smoothed_image = cv2.GaussianBlur(image, ksize, i)

    # 結果を保存
    output_path = f'/Users/hanya/Documents/01スクリーンショット/f{i}.jpg'
    cv2.imwrite(output_path, smoothed_image)
