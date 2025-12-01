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
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QPushButton,
                                QComboBox, QSpinBox, QFileDialog, QDialog, QMessageBox,
                                QRadioButton, QButtonGroup, QCheckBox, QVBoxLayout,
                                QHBoxLayout, QFormLayout, QGroupBox, QStatusBar,
                                QMainWindow, QTextEdit, QProgressDialog)
from PySide6.QtGui import QPixmap, QFont, QImage
from PySide6.QtCore import Qt
import barcode
from barcode.writer import ImageWriter
from pyzbar.pyzbar import decode
from PIL import Image
from MyQR import myqr


class QrCodeGUI(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.setMinimumSize(900, 650)
        self.setWindowTitle('二维码/条形码生成工具')
        
        # 初始化变量
        self.picture_path = ""

        # 创建菜单栏
        self.create_menu_bar()

        # 创建中心部件
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        # 主内容布局 - 水平布局
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # 左侧控制区域
        left_widget = QtWidgets.QWidget()
        left_widget.setObjectName('leftPanel')
        left_layout = QVBoxLayout(left_widget)
        left_layout.setSpacing(12)
        
        # 二维码类型选择组
        type_group = QGroupBox('二维码类型')
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
        content_group = QGroupBox('内容设置')
        content_layout = QFormLayout()
        
        self.content_edit = QLineEdit()
        self.content_edit.setPlaceholderText('请输入要生成的内容...')
        content_layout.addRow('内容:', self.content_edit)
        content_group.setLayout(content_layout)
        
        # 普通二维码参数设置组
        params_group = QGroupBox('参数设置')
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
        personal_group = QGroupBox('个性化选项')
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
        action_group = QGroupBox('操作')
        action_layout = QVBoxLayout()
        
        # 生成按钮行
        generate_layout = QHBoxLayout()
        self.generate_button = QPushButton('生成二维码')
        self.generate_button.setMinimumHeight(40)
        self.generate_barcode_button = QPushButton('生成条形码')
        self.generate_barcode_button.setMinimumHeight(40)
        generate_layout.addWidget(self.generate_button)
        generate_layout.addWidget(self.generate_barcode_button)
        
        # 功能按钮行
        function_layout = QHBoxLayout()
        self.save_button = QPushButton('保存图片')
        self.save_button.setMinimumHeight(36)
        self.recognize_button = QPushButton('识别图片')
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
        
        preview_group = QGroupBox('预览区域')
        preview_layout = QVBoxLayout()
        preview_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        preview_layout.setContentsMargins(20, 20, 20, 20)
        
        self.show_label = QLabel()
        self.show_label.setScaledContents(False)
        self.show_label.setMinimumSize(350, 350)
        self.show_label.setMaximumSize(450, 450)
        self.show_label.setFrameStyle(QLabel.Shape.Box | QLabel.Shadow.Plain)
        self.show_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
        
        # 设置状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage('就绪 - 欢迎使用二维码/条形码生成工具')
        
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

    def create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()

        # 文件菜单
        file_menu = menubar.addMenu('文件(&F)')

        # 批量生成二维码
        batch_action = QtGui.QAction('批量生成二维码(&B)', self)
        batch_action.setShortcut('Ctrl+B')
        batch_action.setStatusTip('批量生成多个二维码')
        batch_action.triggered.connect(self.batch_generate_qrcodes)
        file_menu.addAction(batch_action)

        file_menu.addSeparator()

        # 退出
        exit_action = QtGui.QAction('退出(&X)', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('退出应用程序')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # 帮助菜单
        help_menu = menubar.addMenu('帮助(&H)')

        # 关于
        about_action = QtGui.QAction('关于(&A)', self)
        about_action.setStatusTip('关于此应用程序')
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def batch_generate_qrcodes(self):
        """批量生成二维码"""
        dialog = BatchGenerateDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.status_bar.showMessage('批量生成完成', 3000)

    def show_about(self):
        """显示关于对话框"""
        QMessageBox.about(self, '关于',
                         '二维码/条形码生成工具\n\n'
                         '功能：\n'
                         '• 生成普通二维码\n'
                         '• 生成个性化二维码\n'
                         '• 生成条形码\n'
                         '• 识别二维码/条形码\n'
                         '• 批量生成二维码\n\n'
                         '版本：1.0')

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
                self.status_bar.showMessage('识别失败', 3000)


class BatchGenerateDialog(QDialog):
    """批量生成二维码对话框"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('批量生成二维码')
        self.setModal(True)
        self.setMinimumSize(600, 500)

        layout = QVBoxLayout(self)

        # 输入区域
        input_group = QGroupBox('输入设置')
        input_layout = QFormLayout()

        self.data_edit = QTextEdit()
        self.data_edit.setPlaceholderText('请输入要生成二维码的内容，每行一个：\n例如：\nhttps://www.example.com\n联系电话：13800138000\n产品名称：XXX')
        self.data_edit.setMinimumHeight(150)

        input_layout.addRow('数据列表:', self.data_edit)
        input_group.setLayout(input_layout)

        # 输出设置
        output_group = QGroupBox('输出设置')
        output_layout = QFormLayout()

        self.output_dir_edit = QLineEdit()
        self.output_dir_edit.setPlaceholderText('选择输出目录...')
        self.output_dir_button = QPushButton('选择目录')
        self.output_dir_button.clicked.connect(self.select_output_dir)

        dir_layout = QHBoxLayout()
        dir_layout.addWidget(self.output_dir_edit)
        dir_layout.addWidget(self.output_dir_button)

        self.prefix_edit = QLineEdit()
        self.prefix_edit.setPlaceholderText('文件名前缀（可选）')

        self.format_combo = QComboBox()
        self.format_combo.addItems(['PNG', 'JPEG', 'BMP'])

        output_layout.addRow('输出目录:', dir_layout)
        output_layout.addRow('文件名前缀:', self.prefix_edit)
        output_layout.addRow('图片格式:', self.format_combo)
        output_group.setLayout(output_layout)

        # 二维码参数
        params_group = QGroupBox('二维码参数')
        params_layout = QFormLayout()

        self.version_spin = QSpinBox()
        self.version_spin.setRange(1, 40)
        self.version_spin.setValue(1)

        self.size_spin = QSpinBox()
        self.size_spin.setRange(100, 1000)
        self.size_spin.setValue(200)
        self.size_spin.setSuffix(' px')

        self.margin_spin = QSpinBox()
        self.margin_spin.setRange(0, 20)
        self.margin_spin.setValue(4)

        params_layout.addRow('版本:', self.version_spin)
        params_layout.addRow('尺寸:', self.size_spin)
        params_layout.addRow('边距:', self.margin_spin)
        params_group.setLayout(params_layout)

        # 按钮
        button_layout = QHBoxLayout()
        self.generate_button = QPushButton('开始生成')
        self.generate_button.clicked.connect(self.generate_batch)
        self.cancel_button = QPushButton('取消')
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addStretch()
        button_layout.addWidget(self.generate_button)
        button_layout.addWidget(self.cancel_button)

        # 布局组装
        layout.addWidget(input_group)
        layout.addWidget(output_group)
        layout.addWidget(params_group)
        layout.addLayout(button_layout)

    def select_output_dir(self):
        """选择输出目录"""
        dir_path = QFileDialog.getExistingDirectory(self, '选择输出目录')
        if dir_path:
            self.output_dir_edit.setText(dir_path)

    def generate_batch(self):
        """批量生成二维码"""
        data_text = self.data_edit.toPlainText().strip()
        if not data_text:
            QMessageBox.warning(self, '错误', '请输入要生成二维码的数据')
            return

        output_dir = self.output_dir_edit.text().strip()
        if not output_dir:
            QMessageBox.warning(self, '错误', '请选择输出目录')
            return

        lines = [line.strip() for line in data_text.split('\n') if line.strip()]
        if not lines:
            QMessageBox.warning(self, '错误', '没有有效的数据')
            return

        prefix = self.prefix_edit.text().strip()
        if prefix and not prefix.endswith('_'):
            prefix += '_'

        # 创建进度对话框
        progress = QProgressDialog('正在生成二维码...', '取消', 0, len(lines), self)
        progress.setWindowTitle('批量生成进度')
        progress.setMinimumDuration(0)
        progress.setModal(True)

        success_count = 0
        error_count = 0

        try:
            for i, content in enumerate(lines):
                if progress.wasCanceled():
                    break

                progress.setLabelText(f'正在生成第 {i+1}/{len(lines)} 个二维码...')
                progress.setValue(i)

                # 生成文件名
                filename = f"{prefix}qrcode_{i+1}.{self.format_combo.currentText().lower()}"
                filepath = f"{output_dir}/{filename}"

                try:
                    # 生成二维码
                    qr = qrcode.QRCode(
                        version=self.version_spin.value(),
                        error_correction=qrcode.ERROR_CORRECT_L,
                        box_size=self.size_spin.value() // 29,
                        border=self.margin_spin.value()
                    )
                    qr.add_data(content)
                    qr_img = qr.make_image()

                    # 保存图片
                    qr_img.save(filepath)
                    success_count += 1

                except Exception as e:
                    error_count += 1
                    print(f"生成二维码失败: {content}, 错误: {e}")

            progress.setValue(len(lines))

            # 显示结果
            QMessageBox.information(
                self, '批量生成完成',
                f'生成完成！\n'
                f'成功: {success_count} 个\n'
                f'失败: {error_count} 个\n'
                f'输出目录: {output_dir}'
            )

            if success_count > 0:
                self.accept()

        except Exception as e:
            QMessageBox.critical(self, '错误', f'批量生成过程中发生错误: {e}')


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 使用Windows原生样式
    app.setStyle('WindowsVista')  # 在Windows上使用原生样式

    gui = QrCodeGUI()
    gui.show()
    sys.exit(app.exec())
