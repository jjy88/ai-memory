import subprocess
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
TEXT_DIR = BASE_DIR / "text"

SHORTCUT_NAME = "REDNOTE_MD_GPT_UUID_VERSION"  # ← 改成你现在的 Shortcuts 名字


def has_pending_txt():
    # 遍历所有用户 UUID 文件夹
    for user_dir in TEXT_DIR.iterdir():
        if user_dir.is_dir():
            for file in user_dir.glob("*.txt"):
                print(f"🟡 检测到用户 {user_dir.name} 有待处理 TXT：{file.name}")
                return True
    return False


while True:
    if has_pending_txt():
        print(f"🚀 触发 Shortcuts：{SHORTCUT_NAME}")
        subprocess.run(["shortcuts", "run", SHORTCUT_NAME])
    else:
        print("✅ 暂无待处理 TXT，等待中...")
    time.sleep(10)  # 每 10 秒轮询一次
