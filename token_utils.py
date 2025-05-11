from datetime import datetime, timedelta
import uuid

# 判断 token 是否在 7 天内有效
def is_token_valid(created_time: datetime) -> bool:
    now = datetime.utcnow()
    return now - created_time <= timedelta(days=7)

# 生成唯一 token（用于付款成功后发放）
def generate_token() -> str:
    return str(uuid.uuid4())
