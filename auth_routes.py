# auth_routes.py - JWT认证路由
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from datetime import timedelta
import uuid

auth_bp = Blueprint("auth", __name__)

# 模拟用户数据库（实际应使用真实数据库）
users_db = {}  # {user_id: {"username": str, "password": str, "token_valid_until": datetime}}
tokens_db = {}  # {token: {"user_id": str, "created_at": datetime}}


@auth_bp.route("/auth/register", methods=["POST"])
def register():
    """用户注册"""
    username = request.json.get("username")
    password = request.json.get("password")
    
    if not username or not password:
        return jsonify({"error": "用户名和密码不能为空"}), 400
    
    # 检查用户是否已存在
    for user in users_db.values():
        if user["username"] == username:
            return jsonify({"error": "用户名已存在"}), 400
    
    user_id = str(uuid.uuid4())
    users_db[user_id] = {
        "username": username,
        "password": password  # 实际应该使用密码哈希
    }
    
    return jsonify({
        "message": "注册成功",
        "user_id": user_id
    }), 201


@auth_bp.route("/auth/login", methods=["POST"])
def login():
    """用户登录，返回JWT token"""
    username = request.json.get("username")
    password = request.json.get("password")
    
    if not username or not password:
        return jsonify({"error": "用户名和密码不能为空"}), 400
    
    # 验证用户
    user_id = None
    for uid, user in users_db.items():
        if user["username"] == username and user["password"] == password:
            user_id = uid
            break
    
    if not user_id:
        return jsonify({"error": "用户名或密码错误"}), 401
    
    # 创建JWT tokens
    access_token = create_access_token(
        identity=user_id,
        expires_delta=timedelta(days=7)
    )
    refresh_token = create_refresh_token(
        identity=user_id,
        expires_delta=timedelta(days=30)
    )
    
    return jsonify({
        "message": "登录成功",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user_id": user_id
    }), 200


@auth_bp.route("/auth/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """刷新access token"""
    current_user = get_jwt_identity()
    new_access_token = create_access_token(
        identity=current_user,
        expires_delta=timedelta(days=7)
    )
    
    return jsonify({
        "access_token": new_access_token
    }), 200


@auth_bp.route("/auth/verify", methods=["GET"])
@jwt_required()
def verify():
    """验证JWT token是否有效"""
    current_user = get_jwt_identity()
    jwt_data = get_jwt()
    
    return jsonify({
        "message": "Token有效",
        "user_id": current_user,
        "token_type": jwt_data.get("type", "access")
    }), 200
