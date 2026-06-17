import subprocess
import time
import sys
import os
import webbrowser

root = r"D:\Programs\GidHub\Проекти\AI_OS_Voice_Agent_Web"

print("⚙️ Стартиране на подсистемите на Уеб Агента...")

# 1. Стартираме Уеб Бекенда (FastAPI)
backend_proc = subprocess.Popen([sys.executable, "-m", "uvicorn", "backend.main:app", "--port", "8000"], 
                                cwd=root, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# 2. Стартираме Уеб Фронтенда (Vite/React)
frontend_proc = subprocess.Popen(["cmd", "/c", "npm run dev"], 
                                 cwd=os.path.join(root, "frontend"), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Изчакваме 4 секунди системитите да влязат в щатен режим
time.sleep(4)

print("🌐 Отварям приложението в браузъра...")
# 3. Отваряме стандартния браузър на адреса на фронтенда
webbrowser.open("http://localhost:3000")

try:
    # Държим мениджъра отворен, докато потребителят не реши да го спре с Ctrl+C в конзолата
    print("\n🚀 Уеб Агентът работи! Натиснете Ctrl+C тук, за да спрете сървърите.")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n🛑 Спиране на уеб сървърите и почистване...")
finally:
    backend_proc.terminate()
    frontend_proc.terminate()
    subprocess.run("taskkill /f /im node.exe", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
