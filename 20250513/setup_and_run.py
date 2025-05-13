import os
import subprocess
import sys

def install_packages():
    print("正在安裝依賴套件...")
    result = subprocess.run([sys.executable, "-m", "pip", "install", "."], text=True)
    if result.returncode != 0:
        print("套件安裝失敗。")
        sys.exit(1)
    print("套件安裝完成。")

def run_main_script():
    print("正在執行主程式 ebus_map.py...")
    result = subprocess.run([sys.executable, "ebus_map.py"])
    if result.returncode != 0:
        print("主程式執行失敗。")
        sys.exit(1)

if __name__ == "__main__":
    install_packages()
    run_main_script()

