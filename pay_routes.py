# pay_routes.py
from flask import Blueprint, request, jsonify, render_template
from datetime import datetime
import uuid
from token_utils import is_token_valid, generate_token

pay_bp = Blueprint("pay", __name__)

# 模拟数据库（你可替换为真实持久化）
payments = {}  # {order_id: {"status": "pending"/"paid", "created_time": datetime, "user_token": str}}

# 显示支付二维码页面


@pay_bp.route("/pay", methods=["GET"])
def pay_page():
    order_id = str(uuid.uuid4())
    qr_code_url = "/static/images/weixin_qrcode.png"  # 二维码图像路径（可换成支付宝）
    payments[order_id] = {
        "status": "pending",
        "created_time": datetime.utcnow(),
        "user_token": None
    }
    return render_template("pay.html", order_id=order_id, qr_code_url=qr_code_url)

# 用户点击“我已付款”后，触发发放 token


@pay_bp.route("/pay/success", methods=["POST"])
def pay_success():
    order_id = request.json.get("order_id")

    if order_id not in payments or payments[order_id]["status"] != "pending":
        return jsonify({"error": "订单无效或已支付"}), 400

    # 生成 token 并记录时间
    token = generate_token()
    payments[order_id]["status"] = "paid"
    payments[order_id]["user_token"] = token
    payments[order_id]["created_time"] = datetime.utcnow()

    return jsonify({
        "message": "支付成功！",
        "user_token": token
    })

# 用于后续接口验证 token 是否有效


@pay_bp.route("/validate_token", methods=["POST"])
def validate_token():
    token = request.json.get("user_token")
    found = False

    for record in payments.values():
        if record["user_token"] == token:
            found = True
            if not is_token_valid(record["created_time"]):
                return jsonify({"error": "Token 已过期，请重新购买。"}), 403
            return jsonify({"message": "Token 有效"})

    if not found:
        return jsonify({"error": "Token 无效，请检查或重新购买。"}), 403
