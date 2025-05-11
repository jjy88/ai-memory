# upload_routes.py
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from datetime import datetime
from pathlib import Path
import os
import uuid
import shutil
import pytesseract
from PIL import Image
import pyheif
import PyPDF2
from docx import Document

from token_utils import is_token_valid
from pay_routes import payments
from summarize_utils import summarize_with_ollama  # 假设你封装了调用 Ollama 的总结函数

upload_bp = Blueprint("upload", __name__)

# 配置
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / "uploads"
GENERATED_FOLDER = BASE_DIR / "static" / "generated"
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'jpg', 'jpeg', 'png', 'heic'}
MAX_TOTAL_SIZE_MB = 150
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GENERATED_FOLDER, exist_ok=True)

# 辅助函数


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def count_pdf_pages(filepath):
    with open(filepath, 'rb') as f:
        return len(PyPDF2.PdfReader(f).pages)


def count_docx_pages(filepath):
    doc = Document(filepath)
    return max(1, len(doc.paragraphs) // 30)


def count_image_pages(filepath):
    return 1  # 每张图按一页算


def convert_heic_to_jpg(filepath):
    heif_file = pyheif.read(filepath)
    image = Image.frombytes(heif_file.mode, heif_file.size,
                            heif_file.data, "raw", heif_file.mode)
    jpg_path = str(filepath).rsplit('.', 1)[0] + ".jpg"
    image.save(jpg_path, "JPEG")
    return jpg_path

# 上传接口（支持多文件）


@upload_bp.route("/upload", methods=["POST"])
def upload():
    token = request.form.get("user_token")
    if not token:
        return jsonify({"error": "缺少 Token"}), 403

    # 校验 token
    found = False
    for record in payments.values():
        if record["user_token"] == token:
            found = True
            if not is_token_valid(record["created_time"]):
                return jsonify({"error": "Token 已过期，请重新购买。"}), 403
            break
    if not found:
        return jsonify({"error": "无效 Token"}), 403

    uploaded_files = request.files.getlist("files")
    if not uploaded_files:
        return jsonify({"error": "未上传任何文件"}), 400

    total_size_mb = 0
    content_list = []
    page_count = 0
    user_id = str(uuid.uuid4())
    user_folder = UPLOAD_FOLDER / user_id
    user_folder.mkdir(parents=True, exist_ok=True)

    for file in uploaded_files:
        filename = secure_filename(file.filename)
        if not allowed_file(filename):
            continue

        filepath = user_folder / filename
        file.save(filepath)

        total_size_mb += os.path.getsize(filepath) / (1024 * 1024)
        if total_size_mb > MAX_TOTAL_SIZE_MB:
            shutil.rmtree(user_folder)
            return jsonify({"error": "上传资料过大，请分批上传（最多150MB）"}), 400

        ext = filename.rsplit('.', 1)[1].lower()
        try:
            if ext == 'pdf':
                page_count += count_pdf_pages(filepath)
                content_list.append(f"[PDF] {filename}\n")
            elif ext == 'docx':
                page_count += count_docx_pages(filepath)
                content_list.append(f"[Word] {filename}\n")
            elif ext == 'heic':
                jpg_path = convert_heic_to_jpg(filepath)
                text = pytesseract.image_to_string(
                    Image.open(jpg_path), lang="chi_sim+eng")
                content_list.append(f"[Image OCR] {filename}:\n{text}\n")
                page_count += 1
                os.remove(jpg_path)
            elif ext in ['jpg', 'jpeg', 'png']:
                text = pytesseract.image_to_string(
                    Image.open(filepath), lang="chi_sim+eng")
                content_list.append(f"[Image OCR] {filename}:\n{text}\n")
                page_count += 1
        except Exception as e:
            continue

    # 拼接内容并总结
    all_text = "\n".join(content_list)
    markdown_summary = summarize_with_ollama(all_text)

    # 保存为 Markdown
    md_filename = f"{user_id}.md"
    md_path = GENERATED_FOLDER / md_filename
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown_summary)

    return jsonify({
        "message": "上传成功！",
        "page_count": page_count,
        "price": round(page_count * 0.1, 2),
        "download_url": f"/static/generated/{md_filename}"
    })
