from flask import Flask, request
from pathlib import Path
from PIL import Image
import pytesseract
import shutil

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent


def get_user_dirs(user_id: str):
    upload_dir = BASE_DIR / "uploads" / user_id
    text_dir = BASE_DIR / "text" / user_id
    processed_upload_dir = BASE_DIR / "processed_uploads" / user_id

    for d in [upload_dir, text_dir, processed_upload_dir]:
        d.mkdir(parents=True, exist_ok=True)

    return upload_dir, text_dir, processed_upload_dir


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_id = request.form.get("user_id", "default_user")
        uploaded_files = request.files.getlist("files")
        upload_dir, text_dir, processed_upload_dir = get_user_dirs(user_id)

        converted_files = []

        for file in uploaded_files:
            if file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
                filepath = upload_dir / file.filename
                file.save(filepath)

                text = pytesseract.image_to_string(
                    Image.open(filepath), lang="chi_sim+eng"
                )

                txt_filename = Path(file.filename).stem + ".txt"
                txt_path = text_dir / txt_filename
                with open(txt_path, "w", encoding="utf-8") as f:
                    f.write(text)

                shutil.move(str(filepath), processed_upload_dir / file.filename)
                converted_files.append(txt_filename)

        return f"""
            ✅ 共上传并转换 {len(converted_files)} 张图像为文本：
            <ul>{"".join(f"<li>{f}</li>" for f in converted_files)}</ul>
            📁 文件已保存至 <code>text/{user_id}/</code>，处理过的图像已转移。
        """

    return """
        <!doctype html>
        <html>
        <head><title>Obsi喵 · Markdown生成</title></head>
        <body>
            <h2>上传你的课件图像（支持批量）：</h2>
            <form method="POST" enctype="multipart/form-data">
                <input type="text" name="user_id" placeholder="请输入用户 ID" required><br><br>
                <input type="file" name="files" multiple required>
                <button type="submit">上传并转换文字</button>
            </form>
        </body>
        </html>
    """


if __name__ == "__main__":
    app.run(debug=True, port=8081)
