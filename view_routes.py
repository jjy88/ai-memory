# view_routes.py
from flask import Blueprint, request, send_file, jsonify, render_template
from pathlib import Path

view_bp = Blueprint("view", __name__)
BASE_DIR = Path(__file__).resolve().parent
GENERATED_FOLDER = BASE_DIR / "static" / "generated"


@view_bp.route("/records", methods=["GET"])
def view_records():
    user_id = request.args.get("id")
    if not user_id:
        return "❌ 缺少用户 ID 参数 id=..."

    matched_files = list(GENERATED_FOLDER.glob(f"{user_id}*.md"))
    if not matched_files:
        return f"❌ 没有找到用户 ID 为 {user_id} 的 Markdown 文件。"

    file_list_html = "".join(
        f'<li>{f.name} - <a href="/download?file={f.name}">点击下载</a></li>'
        for f in matched_files
    )

    return f"""
    <h2>📑 用户 {user_id} 的 Markdown 文件</h2>
    <ul>{file_list_html}</ul>
    <p>可直接点击下载结果</p>
    """


@view_bp.route("/download", methods=["GET"])
def download_markdown():
    filename = request.args.get("file")
    if not filename:
        return "❌ 缺少参数 file=..."

    file_path = GENERATED_FOLDER / filename
    if not file_path.exists():
        return f"❌ 找不到文件：{filename}"

    return send_file(file_path, as_attachment=True)
