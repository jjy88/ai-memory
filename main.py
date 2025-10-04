import os
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from upload_routes import upload_bp
from pay_routes import pay_bp
from chat_routes import chat_bp
from auth_routes import auth_bp

app = Flask(__name__)

# JWT配置
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 60 * 60 * 24 * 7  # 7天
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 60 * 60 * 24 * 30  # 30天

jwt = JWTManager(app)

# 注册蓝图
app.register_blueprint(upload_bp)
app.register_blueprint(pay_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(auth_bp)

@app.route("/")
def index():
    return "<h2>欢迎来到 Obsi喵 🐾</h2><p>请访问 <a href='/docs'>/docs</a> 查看API文档或 <a href='/pay'>/pay</a> 开始使用。</p>"

@app.route("/health")
def health():
    """健康检查端点"""
    return jsonify({
        "status": "healthy",
        "service": "ai-memory",
        "version": "1.0.0"
    }), 200

@app.route("/docs")
def docs():
    """API文档页面"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Obsi喵 AI Memory API 文档</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }
            h1 { color: #5a6d7a; }
            .endpoint { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
            .method { display: inline-block; padding: 5px 10px; border-radius: 3px; color: white; font-weight: bold; }
            .get { background: #61affe; }
            .post { background: #49cc90; }
            .path { font-family: monospace; font-size: 1.1em; margin: 10px 0; }
            .description { color: #666; margin: 5px 0; }
        </style>
    </head>
    <body>
        <h1>🐾 Obsi喵 AI Memory API 文档</h1>
        <p>AI驱动的智能文档处理和记忆管理系统</p>
        
        <h2>认证相关</h2>
        <div class="endpoint">
            <div><span class="method post">POST</span><span class="path">/auth/register</span></div>
            <div class="description">用户注册</div>
            <div>请求: {"username": "user1", "password": "pass123"}</div>
        </div>
        
        <div class="endpoint">
            <div><span class="method post">POST</span><span class="path">/auth/login</span></div>
            <div class="description">用户登录，获取JWT token</div>
            <div>请求: {"username": "user1", "password": "pass123"}</div>
            <div>响应: {"access_token": "...", "refresh_token": "..."}</div>
        </div>
        
        <div class="endpoint">
            <div><span class="method post">POST</span><span class="path">/auth/refresh</span></div>
            <div class="description">刷新access token (需要refresh token)</div>
            <div>Headers: Authorization: Bearer &lt;refresh_token&gt;</div>
        </div>
        
        <div class="endpoint">
            <div><span class="method get">GET</span><span class="path">/auth/verify</span></div>
            <div class="description">验证JWT token是否有效</div>
            <div>Headers: Authorization: Bearer &lt;access_token&gt;</div>
        </div>
        
        <h2>聊天接口</h2>
        <div class="endpoint">
            <div><span class="method post">POST</span><span class="path">/chat</span></div>
            <div class="description">聊天接口</div>
            <div>请求: {"user_token": "token", "message": "你好"}</div>
        </div>
        
        <h2>文件上传</h2>
        <div class="endpoint">
            <div><span class="method post">POST</span><span class="path">/upload</span></div>
            <div class="description">上传文件（支持PDF、Word、图片等）</div>
            <div>Form Data: user_token, files[]</div>
        </div>
        
        <h2>支付相关</h2>
        <div class="endpoint">
            <div><span class="method get">GET</span><span class="path">/pay</span></div>
            <div class="description">支付页面</div>
        </div>
        
        <div class="endpoint">
            <div><span class="method post">POST</span><span class="path">/pay/success</span></div>
            <div class="description">支付成功回调</div>
            <div>请求: {"order_id": "..."}</div>
        </div>
        
        <div class="endpoint">
            <div><span class="method post">POST</span><span class="path">/validate_token</span></div>
            <div class="description">验证支付token</div>
            <div>请求: {"user_token": "..."}</div>
        </div>
        
        <h2>系统接口</h2>
        <div class="endpoint">
            <div><span class="method get">GET</span><span class="path">/health</span></div>
            <div class="description">健康检查</div>
        </div>
    </body>
    </html>
    """
    return html

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
