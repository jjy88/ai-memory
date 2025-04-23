import os

import pytesseract
from PIL import Image

base_path = os.path.dirname(os.path.dirname(__file__))
img_folder = os.path.join(base_path, "images")
test_folder = os.path.join(base_path, "text")

for filename in os.listdir(img_folder):
    if filename.lower().endswith((".jpg", ".jpeg")):
        img_path = os.path.join(img_folder, filename)
        text = pytesseract.image_to_string(Image.open(img_path), lang="chi_sim+eng")

        txt_path = os.path.splitext(filename)[0] + ".txt"
        with open(os.path.join(test_folder, txt_path), "w", encoding="utf-8") as f:
            f.write(text)

        print(f"✅ 已提取：{filename} → {txt_path}")
