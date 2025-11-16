"""
二维码生成器
genQrcode

2025/03/11

pip install PySide6
pip install qrcode
pip install MyQR
"""
import io
import sys
import qrcode
from PySide6 import QtWidgets, QtGui
from PySide6 import QtCore
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QLineEdit, QPushButton, 
                                QComboBox, QSpinBox, QFileDialog, QDialog, QMessageBox, 
                                QRadioButton, QButtonGroup, QCheckBox, QVBoxLayout, 
                                QHBoxLayout, QFormLayout, QGroupBox, QStatusBar, QFrame)
from PySide6.QtGui import QPixmap, QIcon, QFont, QImage
from PySide6.QtCore import Qt
import barcode
from barcode.writer import ImageWriter
from pyzbar.pyzbar import decode
from PIL import Image
from MyQR import myqr


class QrCodeGUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.setMinimumSize(900, 650)
        self.setWindowTitle('二维码/条形码生成工具')
        
        # 初始化变量
        self.picture_path = ""
        
        # 应用样式表
        self.apply_stylesheet()
        
        # 主布局 - 垂直布局包含内容和状态栏
        main_container = QVBoxLayout(self)
        main_container.setSpacing(0)
        main_container.setContentsMargins(0, 0, 0, 0)
        
        # 主内容布局 - 水平布局
        main_layout = QHBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # 左侧控制区域
        left_widget = QtWidgets.QWidget()
        left_widget.setObjectName('leftPanel')
        left_layout = QVBoxLayout(left_widget)
        left_layout.setSpacing(12)
        
        # 二维码类型选择组
        type_group = QGroupBox('🔧 二维码类型')
        type_group.setObjectName('typeGroup')
        type_layout = QHBoxLayout()
        
        self.radio_simple = QRadioButton('普通二维码')
        self.radio_personal = QRadioButton('个性化二维码')
        self.radio_simple.setChecked(True)
        self.button_group = QButtonGroup()
        self.button_group.addButton(self.radio_simple)
        self.button_group.addButton(self.radio_personal)
        
        type_layout.addWidget(self.radio_simple)
        type_layout.addWidget(self.radio_personal)
        type_layout.addStretch()
        type_group.setLayout(type_layout)
        
        # 内容输入组
        content_group = QGroupBox('📝 内容设置')
        content_group.setObjectName('contentGroup')
        content_layout = QFormLayout()
        
        self.content_edit = QLineEdit()
        self.content_edit.setPlaceholderText('请输入要生成的内容...')
        content_layout.addRow('内容:', self.content_edit)
        content_group.setLayout(content_layout)
        
        # 普通二维码参数设置组
        params_group = QGroupBox('⚙️ 参数设置')
        params_group.setObjectName('paramsGroup')
        params_layout = QFormLayout()
        
        self.version_combobox = QComboBox()
        for i in range(1, 41):
            self.version_combobox.addItem(str(i))
        
        self.size_combobox = QComboBox()
        for i in range(8, 40, 2):
            self.size_combobox.addItem(f'{i*29} × {i*29}')
        
        self.margin_spinbox = QSpinBox()
        self.margin_spinbox.setRange(0, 20)
        self.margin_spinbox.setSuffix(' px')
        
        params_layout.addRow('版本:', self.version_combobox)
        params_layout.addRow('尺寸:', self.size_combobox)
        params_layout.addRow('边距:', self.margin_spinbox)
        params_group.setLayout(params_layout)
        
        # 个性化选项组
        personal_group = QGroupBox('🎨 个性化选项')
        personal_group.setObjectName('personalGroup')
        personal_layout = QVBoxLayout()
        
        # 背景图片选择
        picture_layout = QHBoxLayout()
        self.picture_label = QLabel('背景图片:')
        self.picture_button = QPushButton('选择图片')
        self.picture_button.clicked.connect(self.select_picture)
        self.picture_status = QLabel('未选择')
        
        picture_layout.addWidget(self.picture_label)
        picture_layout.addWidget(self.picture_button)
        picture_layout.addWidget(self.picture_status)
        picture_layout.addStretch()
        
        # 彩色化选项
        self.check_colorized = QCheckBox('启用彩色效果')
        self.check_colorized.setChecked(True)
        
        personal_layout.addLayout(picture_layout)
        personal_layout.addWidget(self.check_colorized)
        personal_group.setLayout(personal_layout)
        
        # 操作按钮组
        action_group = QGroupBox('🚀 操作')
        action_group.setObjectName('actionGroup')
        action_layout = QVBoxLayout()
        
        # 生成按钮行
        generate_layout = QHBoxLayout()
        self.generate_button = QPushButton('📱 生成二维码')
        self.generate_button.setObjectName('primaryButton')
        self.generate_button.setMinimumHeight(40)
        self.generate_barcode_button = QPushButton('📊 生成条形码')
        self.generate_barcode_button.setObjectName('primaryButton')
        self.generate_barcode_button.setMinimumHeight(40)
        generate_layout.addWidget(self.generate_button)
        generate_layout.addWidget(self.generate_barcode_button)
        
        # 功能按钮行
        function_layout = QHBoxLayout()
        self.save_button = QPushButton('💾 保存图片')
        self.save_button.setObjectName('secondaryButton')
        self.save_button.setMinimumHeight(36)
        self.recognize_button = QPushButton('🔍 识别图片')
        self.recognize_button.setObjectName('secondaryButton')
        self.recognize_button.setMinimumHeight(36)
        function_layout.addWidget(self.save_button)
        function_layout.addWidget(self.recognize_button)
        
        action_layout.addLayout(generate_layout)
        action_layout.addLayout(function_layout)
        action_group.setLayout(action_layout)
        
        # 组装左侧控制区
        left_layout.addWidget(type_group)
        left_layout.addWidget(content_group)
        left_layout.addWidget(params_group)
        left_layout.addWidget(personal_group)
        left_layout.addWidget(action_group)
        left_layout.addStretch()
        
        # 右侧预览区域
        right_widget = QtWidgets.QWidget()
        right_widget.setObjectName('rightPanel')
        right_layout = QVBoxLayout(right_widget)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        preview_group = QGroupBox('👁️ 预览区域')
        preview_group.setObjectName('previewGroup')
        preview_layout = QVBoxLayout()
        preview_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        preview_layout.setContentsMargins(20, 20, 20, 20)
        
        self.show_label = QLabel()
        self.show_label.setScaledContents(False)
        self.show_label.setMinimumSize(350, 350)
        self.show_label.setMaximumSize(450, 450)
        self.show_label.setFrameStyle(QLabel.Shape.Box | QLabel.Shadow.Plain)
        self.show_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.show_label.setObjectName('previewLabel')
        placeholder_font = QFont()
        placeholder_font.setPointSize(12)
        self.show_label.setFont(placeholder_font)
        self.show_label.setText('预览区域\n\n生成的二维码/条形码\n将显示在这里')
        
        preview_layout.addWidget(self.show_label)
        preview_group.setLayout(preview_layout)
        right_layout.addWidget(preview_group)
        
        # 主布局组装
        main_layout.addWidget(left_widget, 2)
        main_layout.addWidget(right_widget, 3)
        
        # 状态栏
        self.status_bar = QStatusBar()
        self.status_bar.setObjectName('statusBar')
        self.status_bar.showMessage('就绪 - 欢迎使用二维码/条形码生成工具')
        
        # 组装主容器
        main_container.addLayout(main_layout)
        main_container.addWidget(self.status_bar)
        
        # 信号绑定
        self.generate_button.clicked.connect(self.gen_qrcode)
        self.save_button.clicked.connect(self.save_qrcode)
        self.margin_spinbox.valueChanged.connect(self.gen_qrcode)
        self.generate_barcode_button.clicked.connect(self.gen_barcode)
        self.recognize_button.clicked.connect(self.recognize_code)
        self.radio_simple.toggled.connect(self.toggle_qr_type)
        self.radio_personal.toggled.connect(self.toggle_qr_type)
        
        # 初始化界面状态
        self.toggle_qr_type()
        self.gen_qrcode()

    def toggle_qr_type(self):
        """切换二维码类型时的界面状态"""
        is_simple = self.radio_simple.isChecked()
        # 普通二维码参数控件的可见性
        self.version_combobox.setEnabled(is_simple)
        self.size_combobox.setEnabled(is_simple)
        self.margin_spinbox.setEnabled(is_simple)
        # 个性化选项的可见性
        self.picture_button.setEnabled(not is_simple)
        self.check_colorized.setEnabled(not is_simple)
        self.picture_status.setEnabled(not is_simple)

    def select_picture(self):
        """选择背景图片"""
        file_path, _ = QFileDialog.getOpenFileName(self, "选择背景图片", "", "图片文件 (*.png *.jpg *.jpeg *.gif *.bmp)")
        if file_path:
            self.picture_path = file_path
            filename = file_path.split("/")[-1]
            if len(filename) > 20:
                filename = filename[:17] + "..."
            self.picture_status.setText(f'✓ {filename}')
            self.status_bar.showMessage(f'背景图片已选择: {filename}', 3000)

    def gen_qrcode(self):
        """生成二维码"""
        content = self.content_edit.text()
        if not content:
            content = "Hello World"
            
        if self.radio_simple.isChecked():
            # 普通二维码生成
            try:
                margin = int(self.margin_spinbox.text().replace(' px', ''))
            except:
                margin = 0
            size = int(self.size_combobox.currentText().split('×')[0].strip())
            qr = qrcode.QRCode(version=1,
                               error_correction=qrcode.ERROR_CORRECT_L,
                               box_size=size//29,
                               border=margin)
            qr.add_data(content)
            self.qr_img = qr.make_image()
            fp = io.BytesIO()
            self.qr_img.save(fp, 'BMP')
            qimg = QtGui.QImage()
            qimg.loadFromData(fp.getvalue())
            qimg_pixmap = QtGui.QPixmap.fromImage(qimg)
            scaled_pixmap = qimg_pixmap.scaled(self.show_label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.show_label.setPixmap(scaled_pixmap)
            self.status_bar.showMessage('✓ 普通二维码生成成功', 3000)
        else:
            # 个性化二维码生成
            self.gen_personal_qrcode()

    def gen_personal_qrcode(self):
        """生成个性化二维码"""
        content = self.content_edit.text()
        if not content:
            QMessageBox.warning(self, '错误', '请输入二维码内容')
            return
            
        try:
            # 创建临时文件保存个性化二维码
            import tempfile
            temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
            temp_path = temp_file.name
            temp_file.close()
            
            if self.picture_path:
                # 有背景图片的个性化二维码
                myqr.run(words=content, 
                        picture=self.picture_path, 
                        colorized=self.check_colorized.isChecked(), 
                        save_name=temp_path)
            else:
                # 无背景图片的普通个性化二维码
                myqr.run(words=content, save_name=temp_path)
            
            # 显示生成的二维码
            pixmap = QPixmap(temp_path)
            scaled_pixmap = pixmap.scaled(self.show_label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.show_label.setPixmap(scaled_pixmap)
            self.status_bar.showMessage('✓ 个性化二维码生成成功', 3000)
            
            # 保存图片对象用于后续保存
            self.qr_img = Image.open(temp_path)
            
            # 清理临时文件
            import os
            os.unlink(temp_path)
            
        except Exception as e:
            QMessageBox.warning(self, '错误', f'个性化二维码生成失败: {e}')
            self.status_bar.showMessage('✗ 个性化二维码生成失败', 3000)

    def save_qrcode(self):
        """保存二维码"""
        if not hasattr(self, 'qr_img') or self.qr_img is None:
            QMessageBox.warning(self, '错误', '请先生成二维码或条形码')
            return
            
        filename, _ = QFileDialog.getSaveFileName(
            self, '保存图片', './qrcode.png', '图片文件 (*.png);;所有文件 (*)')
        if filename != '':
            # PIL Image and qrcode image both support save with filename
            self.qr_img.save(filename)  # type: ignore
            QMessageBox.information(self, '成功', '图片保存成功！')
            self.status_bar.showMessage(f'✓ 图片已保存: {filename}', 5000)

    def gen_barcode(self):
        """生成条形码"""
        content = self.content_edit.text()
        if not content:
            QMessageBox.warning(self, '错误', '请输入内容')
            return
        try:
            code128 = barcode.get('code128', content, writer=ImageWriter())
            fp = io.BytesIO()
            code128.write(fp)
            fp.seek(0)
            img = Image.open(fp)
            qimg = QtGui.QImage(fp.getvalue(), img.width, img.height, QImage.Format.Format_RGB888)
            qimg_pixmap = QtGui.QPixmap.fromImage(qimg)
            scaled_pixmap = qimg_pixmap.scaled(self.show_label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.show_label.setPixmap(scaled_pixmap)
            self.qr_img = img
            self.status_bar.showMessage('✓ 条形码生成成功', 3000)
        except Exception as e:
            QMessageBox.warning(self, '错误', f'条形码生成失败: {e}')
            self.status_bar.showMessage('✗ 条形码生成失败', 3000)

    def recognize_code(self):
        """识别二维码/条形码"""
        filename, _ = QFileDialog.getOpenFileName(self, '选择图片', '', '图片文件 (*.png *.jpg *.jpeg *.bmp *.gif);;所有文件 (*)')
        if filename:
            try:
                img = Image.open(filename)
                results = decode(img)
                if not results:
                    QMessageBox.information(self, '识别结果', '未识别到二维码或条形码内容')
                    self.status_bar.showMessage('⚠ 未识别到内容', 3000)
                    return
                msg = '\n'.join([f'{r.type}: {r.data.decode()}' for r in results])
                QMessageBox.information(self, '识别结果', f'识别成功！\n\n{msg}')
                self.status_bar.showMessage('✓ 识别成功', 3000)
            except Exception as e:
                QMessageBox.warning(self, '错误', f'图片识别失败: {e}')
                self.status_bar.showMessage('✗ 识别失败', 3000)


    def apply_stylesheet(self):
        """应用现代化样式表"""
        stylesheet = """
        QWidget {
            background-color: #f5f5f5;
            font-family: 'Microsoft YaHei UI', 'Segoe UI', Arial;
            font-size: 10pt;
        }
        
        QGroupBox {
            font-weight: bold;
            font-size: 11pt;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            margin-top: 12px;
            padding-top: 10px;
            background-color: white;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            left: 15px;
            padding: 0 8px;
            color: #2c3e50;
        }
        
        #typeGroup, #contentGroup, #paramsGroup, #personalGroup, #actionGroup {
            background-color: white;
        }
        
        #previewGroup {
            background-color: #fafafa;
            border: 2px solid #d0d0d0;
        }
        
        QLineEdit, QComboBox, QSpinBox {
            padding: 6px 10px;
            border: 2px solid #dcdcdc;
            border-radius: 5px;
            background-color: white;
            selection-background-color: #3498db;
        }
        
        QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
            border: 2px solid #3498db;
        }
        
        QPushButton#primaryButton {
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: bold;
            font-size: 10pt;
        }
        
        QPushButton#primaryButton:hover {
            background-color: #2980b9;
        }
        
        QPushButton#primaryButton:pressed {
            background-color: #21618c;
        }
        
        QPushButton#secondaryButton {
            background-color: #95a5a6;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 6px 14px;
            font-weight: bold;
        }
        
        QPushButton#secondaryButton:hover {
            background-color: #7f8c8d;
        }
        
        QPushButton#secondaryButton:pressed {
            background-color: #6c7a7b;
        }
        
        QPushButton {
            background-color: #ecf0f1;
            color: #2c3e50;
            border: 1px solid #bdc3c7;
            border-radius: 5px;
            padding: 5px 12px;
        }
        
        QPushButton:hover {
            background-color: #d5dbdb;
        }
        
        QPushButton:pressed {
            background-color: #bdc3c7;
        }
        
        QPushButton:disabled {
            background-color: #ecf0f1;
            color: #95a5a6;
        }
        
        QRadioButton {
            spacing: 8px;
            color: #2c3e50;
        }
        
        QRadioButton::indicator {
            width: 18px;
            height: 18px;
        }
        
        QRadioButton::indicator:unchecked {
            border: 2px solid #95a5a6;
            border-radius: 9px;
            background-color: white;
        }
        
        QRadioButton::indicator:checked {
            border: 2px solid #3498db;
            border-radius: 9px;
            background-color: #3498db;
        }
        
        QCheckBox {
            spacing: 8px;
            color: #2c3e50;
        }
        
        QCheckBox::indicator {
            width: 18px;
            height: 18px;
        }
        
        QCheckBox::indicator:unchecked {
            border: 2px solid #95a5a6;
            border-radius: 3px;
            background-color: white;
        }
        
        QCheckBox::indicator:checked {
            border: 2px solid #27ae60;
            border-radius: 3px;
            background-color: #27ae60;
        }
        
        QLabel#previewLabel {
            background-color: white;
            border: 3px dashed #bdc3c7;
            border-radius: 8px;
            color: #95a5a6;
            padding: 20px;
        }
        
        QStatusBar {
            background-color: #34495e;
            color: white;
            font-size: 9pt;
            padding: 4px;
        }
        
        QStatusBar::item {
            border: none;
        }
        """
        self.setStyleSheet(stylesheet)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # 设置应用程序样式
    app.setStyle('Fusion')
    
    gui = QrCodeGUI()
    gui.show()
    sys.exit(app.exec())
