"""
二维码生成器程序入口
genQrcode

2025/03/11

pip install PySide6
pip install qrcode
pip install MyQR
"""
import sys
from PySide6.QtWidgets import QApplication
from PySide6 import QtGui
from app.ui.main_window import QrCodeGUI, BatchGenerateDialog
from app.core.qr_generator import QRCodeController


def main():
    """程序主入口"""
    # 创建应用程序实例
    app = QApplication(sys.argv)

    # 使用Windows原生样式
    app.setStyle('WindowsVista')  # 在Windows上使用原生样式

    # 设置应用程序图标（全局设置）
    icon_formats = ["resources/icon.png", "resources/icon.ico"]
    for icon_path in icon_formats:
        try:
            app_icon = QtGui.QIcon(icon_path)
            app.setWindowIcon(app_icon)
            break  # 成功设置后退出循环
        except Exception as e:
            print(f"设置应用程序图标失败 ({icon_path}): {e}")

    # 创建主窗口
    gui = QrCodeGUI()

    # 为批量生成对话框关联BatchGenerateDialog类
    QrCodeGUI.BatchGenerateDialog = BatchGenerateDialog

    # 创建控制器并连接界面和业务逻辑
    controller = QRCodeController(gui)

    # 初始化
    controller.initialize()

    # 显示窗口并启动应用程序
    gui.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()