import subprocess
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
TEXT_DIR = BASE_DIR / "text"


def has_pending_txt():
    return any(f.suffix == ".txt" for f in TEXT_DIR.iterdir())


while True:
    if has_pending_txt():
        print("🚀 检测到待处理 TXT 文件，触发 Shortcuts...")
        subprocess.run(["shortcuts", "run", "REDNOTE_MD_GPT"])
    else:
        print("✅ 暂无待处理 TXT，等待中...")
    time.sleep(10)  # 每 10 秒轮询一次
