#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
二维码/条形码生成工具 - 打包脚本
"""

import subprocess
import sys
import os


def print_header():
    """打印脚本头部信息"""
    print("=" * 40)
    print("二维码/条形码生成工具 - 打包脚本")
    print("=" * 40)
    print()


def check_dependencies():
    """检查并安装依赖"""
    print("[1/3] 检查依赖...")
    
    try:
        import PyInstaller
        print("PyInstaller 已安装")
    except ImportError:
        print("PyInstaller 未安装，正在安装...")
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "pyinstaller"],
                check=True
            )
            print("PyInstaller 安装成功")
        except subprocess.CalledProcessError as e:
            print(f"[错误] PyInstaller 安装失败: {e}")
            sys.exit(1)


def build_application():
    """打包应用程序"""
    print()
    print("[2/3] 开始打包应用程序...")
    print("这可能需要几分钟时间，请耐心等待...")
    print()
    
    try:
        # 运行 pyinstaller 命令
        result = subprocess.run(
            ["pyinstaller", "--clean", "build.spec"],
            check=True,
            capture_output=False
        )
        return True
    except subprocess.CalledProcessError as e:
        print()
        print("[错误] 打包失败！请检查错误信息。")
        return False
    except FileNotFoundError:
        print()
        print("[错误] 找不到 pyinstaller 命令。请确保 PyInstaller 已正确安装。")
        return False


def print_success():
    """打印成功信息"""
    print()
    print("[3/3] 打包完成！")
    print()
    print("可执行文件位置: dist/QRCodeGenerator/QRCodeGenerator.exe")
    print("依赖文件位置: dist/QRCodeGenerator/_internal/")
    print()
    print("注意：运行程序时需要保持整个 QRCodeGenerator 文件夹完整")
    print()
    print("=" * 40)
    print("打包成功完成！")
    print("=" * 40)


def main():
    """主函数"""
    # 切换到脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print_header()
    check_dependencies()
    
    if build_application():
        print_success()
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
