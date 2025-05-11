# summarize_utils.py
import subprocess


def summarize_with_ollama(text_content):
    result = subprocess.run(
        ["ollama", "run", "qwen-deepseek-R1", text_content],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()
