import subprocess
from pathlib import Path

from flask import Flask, render_template, request
from PIL import Image

# 创建 Flask 应用实例
app = Flask(__name__)

# 设置上传目录
UPLOAD_DIR = Path(__file__).resolve().parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)


# 首页路由：支持 GET 与 POST 上传文件
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        file.save(UPLOAD_DIR / file.filename)
        return f"上传成功：{file.filename}"
    return """
        <!doctype html>
        <html>
        <head><title>Obsi喵 · Markdown生成</title></head>
        <body>
            <h2>上传你的课件或文本：</h2>
            <form method="POST" enctype="multipart/form-data">
                <input type="file" name="file" required>
                <button type="submit">上传</button>
            </form>
        </body>
        </html>
    """


# 启动服务
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
