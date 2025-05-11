# chat_routes.py

from flask import Blueprint, request, jsonify
from pay_routes import is_token_valid  # 注意：导入验证Token的函数

# 创建 Blueprint
chat_bp = Blueprint('chat', __name__)

# 聊天接口


@chat_bp.route("/chat", methods=["POST"])
def chat():
    user_token = request.json.get("user_token", "")
    if not is_token_valid(user_token):
        return jsonify({"error": "无效或过期的Token，请重新购买"}), 403

    # Token合法，继续正常服务
    user_input = request.json.get("message", "")
    reply = f"你好，欢迎来到 Obsi喵！你说的是：{user_input}"
    return jsonify({"reply": reply})
