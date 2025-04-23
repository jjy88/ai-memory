from flask import Flask, request, make_response, send_file
from pathlib import Path
from PIL import Image
import pytesseract
import uuid
import shutil
import os

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent


# 获取用户 ID（若不存在则生成 UUID4）
def get_user_id():
    user_id = request.cookies.get("user_id")
    if not user_id:
        user_id = str(uuid.uuid4())
    return user_id


# 根据用户 ID 创建并返回各类目录
def get_user_dirs(user_id: str):
    upload_dir = BASE_DIR / "uploads" / user_id
    text_dir = BASE_DIR / "text" / user_id
    processed_dir = BASE_DIR / "processed_uploads_image_pdfs" / user_id

    for d in [upload_dir, text_dir, processed_dir]:
        d.mkdir(parents=True, exist_ok=True)

    return upload_dir, text_dir, processed_dir


@app.route("/", methods=["GET", "POST"])
def index():
    user_id = get_user_id()
    upload_dir, text_dir, processed_dir = get_user_dirs(user_id)

    if request.method == "POST":
        uploaded_files = request.files.getlist("files")
        converted_files = []
        for file in uploaded_files:
            filename = file.filename
            if filename.lower().endswith((".jpg", ".jpeg", ".png")):
                filepath = upload_dir / filename
                print(f"📥 正在保存上传文件：{filepath}")  # ✅ 新增调试
                try:
                    file.save(filepath)
                except Exception as e:
                    print(f"❌ 保存文件失败: {e}")
                    continue
                # for file in uploaded_files:
                #     filename = file.filename
                #     if filename.lower().endswith((".jpg", ".jpeg", ".png")):
                #         filepath = upload_dir / filename
                #         file.save(filepath)

                print(f"✅ 正在处理文件：{filename}")
                try:
                    text = pytesseract.image_to_string(
                        Image.open(filepath), lang="chi_sim+eng"
                    )
                except Exception as e:
                    print(f"❌ OCR 失败：{e}")
                    continue

                txt_filename = Path(filename).stem + ".txt"
                txt_path = text_dir / txt_filename
                with open(txt_path, "w", encoding="utf-8") as f:
                    f.write(text)

                # 转存已处理图片
                shutil.move(str(filepath), processed_dir / filename)
                converted_files.append(txt_filename)

        html = f"""
        ✅ 共上传并转换 {len(converted_files)} 张图像为文本：
        <ul>{"".join(f"<li>{f}</li>" for f in converted_files)}</ul>
        📁 你可以在 <code>text/{user_id}/</code> 中查看待处理的文本。<br>
        🆔 当前用户 ID：<code>{user_id}</code>（请保存）
        """
        resp = make_response(html)
        resp.set_cookie(
            "user_id", user_id, max_age=60 * 60 * 24 * 7
        )  # Cookie 有效期 7 天
        return resp

    # 默认首页
    html = f"""
    <!doctype html>
    <html>
    <head><title>Obsi喵 · Markdown生成</title></head>
    <body>
        <h2>上传你的课件图片（支持批量）</h2>
        <p>📌 当前用户 ID：<code>{user_id}</code></p>
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="files" multiple required>
            <button type="submit">上传并转换</button>
        </form>
        <p>请妥善保存你的 ID，未来可用于找回 Markdown 文件。</p>
    </body>
    </html>
    """
    resp = make_response(html)
    resp.set_cookie("user_id", user_id, max_age=60 * 60 * 24 * 7)
    return resp


if __name__ == "__main__":
    app.run(debug=True, port=8082)
