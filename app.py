import os
from flask import Flask
from upload_routes import upload_bp
from pay_routes import pay_bp
from chat_routes import chat_bp

app = Flask(__name__)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
# 注册蓝图
app.register_blueprint(upload_bp)
app.register_blueprint(pay_bp)
app.register_blueprint(chat_bp)

