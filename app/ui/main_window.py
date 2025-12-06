"""
主窗口界面类
负责所有GUI界面的创建和布局
"""
import sys
import webbrowser
from PySide6 import QtWidgets, QtGui
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QPushButton,
                                QComboBox, QSpinBox, QFileDialog, QMessageBox,
                                QRadioButton, QButtonGroup, QCheckBox, QVBoxLayout,
                                QHBoxLayout, QFormLayout, QGroupBox, QStatusBar,
                                QMainWindow, QProgressDialog)
from ..core.qr_generator_engine import QRCodeGenerator
from ..core.qr_scanner_engine import QRCodeScanner
from PySide6.QtGui import QPixmap, QFont, QImage
from PySide6.QtCore import Qt, QPoint
from .dialogs import RecognizeResultDialog, BatchGenerateDialog


class QrCodeGUI(QMainWindow):
    """二维码生成工具主窗口界面类"""

    def __init__(self, parent=None):
        super().__init__()
        self.setMinimumSize(900, 650)
        self.setWindowTitle('二维码/条形码生成工具')

        # 初始化变量
        self.picture_path = ""

        # 初始化核心引擎
        self.generator = QRCodeGenerator()
        self.scanner = QRCodeScanner()

        # 设置应用程序图标
        self.set_app_icon()

        # 创建菜单栏
        self.create_menu_bar()

        # 创建中心部件
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        # 创建界面
        self.setup_ui(central_widget)

        # 初始化界面状态
        self.initialize_ui()

    def setup_ui(self, central_widget):
        """设置用户界面"""
        # 主内容布局 - 水平布局
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # 左侧控制区域
        self.left_widget = QtWidgets.QWidget()
        self.left_widget.setObjectName('leftPanel')
        left_layout = QVBoxLayout(self.left_widget)
        left_layout.setSpacing(12)

        # 创建左侧控制面板
        self.create_control_panel(left_layout)

        # 右侧预览区域
        self.right_widget = QtWidgets.QWidget()
        self.right_widget.setObjectName('rightPanel')
        right_layout = QVBoxLayout(self.right_widget)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 创建预览区域
        self.create_preview_area(right_layout)

        # 主布局组装
        main_layout.addWidget(self.left_widget, 2)
        main_layout.addWidget(self.right_widget, 3)

        # 设置状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage('就绪 - 欢迎使用二维码/条形码生成工具')

    def create_control_panel(self, parent_layout):
        """创建左侧控制面板"""
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
        parent_layout.addWidget(type_group)
        parent_layout.addWidget(content_group)
        parent_layout.addWidget(params_group)
        parent_layout.addWidget(personal_group)
        parent_layout.addWidget(action_group)
        parent_layout.addStretch()

    def create_preview_area(self, parent_layout):
        """创建右侧预览区域"""
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

        # 启用右键菜单
        self.show_label.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.show_label.customContextMenuRequested.connect(self.show_preview_context_menu)

        preview_layout.addWidget(self.show_label)
        preview_group.setLayout(preview_layout)
        parent_layout.addWidget(preview_group)

    def create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()

        # 文件菜单
        file_menu = menubar.addMenu('文件(&F)')

        # 批量生成二维码
        batch_action = QtGui.QAction('批量生成二维码(&B)', self)
        batch_action.setShortcut('Ctrl+B')
        batch_action.setStatusTip('批量生成多个二维码')
        file_menu.addAction(batch_action)

        file_menu.addSeparator()

        # 退出
        exit_action = QtGui.QAction('退出(&X)', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('退出应用程序')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # 识别菜单
        recognize_menu = menubar.addMenu('识别(&R)')

        # 识别图片文件
        recognize_file_action = QtGui.QAction('识别图片文件(&F)', self)
        recognize_file_action.setShortcut('Ctrl+O')
        recognize_file_action.setStatusTip('识别本地图片文件中的二维码/条形码')
        recognize_menu.addAction(recognize_file_action)

        # 识别剪贴板
        recognize_clipboard_action = QtGui.QAction('识别剪贴板(&C)', self)
        recognize_clipboard_action.setShortcut('Ctrl+V')
        recognize_clipboard_action.setStatusTip('识别剪贴板中的二维码/条形码')
        recognize_menu.addAction(recognize_clipboard_action)

        # 工具菜单
        tools_menu = menubar.addMenu('工具(&T)')



        # 草料二维码
        caoliaovip_action = QtGui.QAction('草料二维码(&C)', self)
        caoliaovip_action.setStatusTip('在线二维码生成工具 - https://cli.im/')
        tools_menu.addAction(caoliaovip_action)

        # 帮助菜单
        help_menu = menubar.addMenu('帮助(&H)')

        # 关于
        about_action = QtGui.QAction('关于(&A)', self)
        about_action.setStatusTip('关于此应用程序')
        help_menu.addAction(about_action)

        # 连接菜单项的信号
        caoliaovip_action.triggered.connect(lambda: webbrowser.open('https://cli.im/'))

        # 返回菜单动作供外部连接信号
        self.batch_action = batch_action
        self.recognize_file_action = recognize_file_action
        self.recognize_clipboard_action = recognize_clipboard_action
        self.about_action = about_action

    def set_app_icon(self):
        """设置应用程序图标"""
        # 尝试使用PNG格式的图标（运行时）
        icon_formats = ["resources/icon.png", "resources/icon.ico"]

        for icon_path in icon_formats:
            try:
                app_icon = QtGui.QIcon(icon_path)
                self.setWindowIcon(app_icon)

                # 同时设置应用程序图标，这样对话框等也会使用相同图标
                QApplication.instance().setWindowIcon(app_icon)
                break  # 成功设置后退出循环
            except Exception as e:
                print(f"设置图标失败 ({icon_path}): {e}")
                # 如果图标设置失败，程序继续运行，只是没有图标

    def initialize_ui(self):
        """初始化界面状态"""
        # 普通二维码参数控件的可见性
        self.version_combobox.setEnabled(True)
        self.size_combobox.setEnabled(True)
        self.margin_spinbox.setEnabled(True)
        # 个性化选项的可见性
        self.picture_button.setEnabled(False)
        self.check_colorized.setEnabled(False)
        self.picture_status.setEnabled(False)

        # 连接信号
        self.setup_connections()

        # 生成初始二维码
        self.generate_qrcode()

    def setup_connections(self):
        """设置信号连接"""
        # 连接按钮信号
        self.generate_button.clicked.connect(self.on_generate_qrcode)
        self.save_button.clicked.connect(self.on_save_qrcode)
        self.margin_spinbox.valueChanged.connect(self.on_generate_qrcode)
        self.generate_barcode_button.clicked.connect(self.on_generate_barcode)
        self.recognize_button.clicked.connect(self.on_recognize_code)
        self.picture_button.clicked.connect(self.on_select_picture)

        # 连接单选按钮信号
        self.radio_simple.toggled.connect(self.on_toggle_qr_type)

        # 连接菜单动作信号
        self.batch_action.triggered.connect(self.on_batch_generate_qrcodes)
        self.recognize_file_action.triggered.connect(self.on_recognize_code)
        self.recognize_clipboard_action.triggered.connect(self.on_recognize_clipboard)
        self.about_action.triggered.connect(self.on_show_about)

    # 事件处理方法
    def on_generate_qrcode(self):
        """生成二维码按钮点击事件"""
        content = self.get_content()

        try:
            if self.get_current_qr_type() == 'simple':
                # 生成普通二维码
                params = self.get_qr_params()
                qr_img = self.generator.generate_simple_qrcode(content, params)
                self.show_qrcode(qr_img)
                self.show_status_message('✓ 普通二维码生成成功', 3000)
            else:
                # 生成个性化二维码
                params = self.get_personal_params()
                qr_img = self.generator.generate_personal_qrcode(content, params)
                self.show_qrcode(qr_img)
                self.show_status_message('✓ 个性化二维码生成成功', 3000)

        except Exception as e:
            QMessageBox.warning(self, '错误', str(e))
            self.show_status_message('✗ 生成失败', 3000)

    def generate_qrcode(self):
        """生成二维码的简化方法"""
        self.on_generate_qrcode()

    def on_save_qrcode(self):
        """保存图片按钮点击事件"""
        if not hasattr(self, 'qr_img') or self.qr_img is None:
            QMessageBox.warning(self, '错误', '请先生成二维码或条形码')
            return

        try:
            filename, _ = QFileDialog.getSaveFileName(
                self, '保存图片', './qrcode.png',
                '图片文件 (*.png);;所有文件 (*)'
            )
            if filename:
                self.qr_img.save(filename)
                QMessageBox.information(self, '成功', '图片保存成功！')
                self.show_status_message(f'✓ 图片已保存: {filename}', 5000)

        except Exception as e:
            QMessageBox.warning(self, '错误', f'保存失败: {e}')

    def on_generate_barcode(self):
        """生成条形码按钮点击事件"""
        content = self.get_content()

        try:
            barcode_img = self.generator.generate_barcode(content)
            self.show_qrcode(barcode_img)
            self.show_status_message('✓ 条形码生成成功', 3000)

        except Exception as e:
            QMessageBox.warning(self, '错误', str(e))
            self.show_status_message('✗ 条形码生成失败', 3000)

    def on_recognize_code(self):
        """识别图片按钮点击事件"""
        try:
            filename, _ = QFileDialog.getOpenFileName(
                self, '选择图片', '',
                '图片文件 (*.png *.jpg *.jpeg *.bmp *.gif);;所有文件 (*)'
            )

            if filename:
                results = self.scanner.recognize_code(filename)
                self.show_recognize_results(results, "图片识别完成")

        except Exception as e:
            QMessageBox.warning(self, '错误', f'图片识别失败: {e}')
            self.show_status_message('识别失败', 3000)

    def on_recognize_clipboard(self):
        """识别剪贴板按钮点击事件"""
        try:
            results = self.scanner.recognize_clipboard()
            self.show_recognize_results(results, "剪贴板识别完成")

        except Exception as e:
            QMessageBox.warning(self, '错误', f'剪贴板识别失败: {e}')
            self.show_status_message('剪贴板识别失败', 3000)

    def on_select_picture(self):
        """选择背景图片按钮点击事件"""
        file_path = self.select_picture_file()
        if file_path:
            self.picture_path = file_path
            filename = file_path.split("/")[-1] if "/" in file_path else file_path.split("\\")[-1]
            if len(filename) > 20:
                filename = filename[:17] + "..."
            self.set_picture_status(f'✓ {filename}')
            self.show_status_message(f'背景图片已选择: {filename}', 3000)

    def on_toggle_qr_type(self):
        """切换二维码类型事件"""
        is_simple = self.radio_simple.isChecked()
        # 普通二维码参数控件的可见性
        self.version_combobox.setEnabled(is_simple)
        self.size_combobox.setEnabled(is_simple)
        self.margin_spinbox.setEnabled(is_simple)
        # 个性化选项的可见性
        self.picture_button.setEnabled(not is_simple)
        self.check_colorized.setEnabled(not is_simple)
        self.picture_status.setEnabled(not is_simple)

    def on_batch_generate_qrcodes(self):
        """批量生成二维码菜单事件"""
        dialog = BatchGenerateDialog(self)
        dialog.setup_batch_logic(self)

        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            self.show_status_message('批量生成完成', 3000)

    def on_batch_generate_with_data(self, batch_data):
        """执行批量生成二维码"""
        # 创建进度对话框
        progress = QProgressDialog('正在生成二维码...', '取消', 0, len(batch_data.get('lines', [])), self)
        progress.setWindowTitle('批量生成进度')
        progress.setMinimumDuration(0)
        progress.setModal(True)

        # 定义进度回调函数
        def progress_callback(current, total, message):
            progress.setLabelText(message)
            progress.setValue(current)
            return progress.wasCanceled()

        try:
            success_count, error_count = self.generator.batch_generate_qrcodes(batch_data, progress_callback)
            progress.setValue(progress.maximum())

            # 显示结果
            QMessageBox.information(
                self, '批量生成完成',
                f'生成完成！\n'
                f'成功: {success_count} 个\n'
                f'失败: {error_count} 个\n'
                f'输出目录: {batch_data.get("output_dir", "")}'
            )

            if success_count > 0:
                QtWidgets.QDialog.accept(dialog)

        except Exception as e:
            QMessageBox.warning(self, '错误', f'批量生成过程中发生错误: {e}')

    def on_show_about(self):
        """显示关于对话框"""
        QMessageBox.about(
            self, '关于',
            '二维码/条形码生成工具\n\n'
            '功能：\n'
            '• 生成普通二维码\n'
            '• 生成个性化二维码\n'
            '• 生成条形码\n'
            '• 识别二维码/条形码\n'
            '• 批量生成二维码\n\n'
            '版本：1.0'
        )

    def show_recognize_results(self, results, status_message):
        """显示识别结果对话框"""
        dialog = RecognizeResultDialog(results, self)
        dialog.exec()
        self.show_status_message(f'✓ {status_message}', 3000)

    def get_current_qr_type(self):
        """获取当前选择的二维码类型"""
        return 'simple' if self.radio_simple.isChecked() else 'personal'

    def get_content(self):
        """获取输入的内容"""
        return self.content_edit.text()

    def set_picture_status(self, status_text):
        """设置背景图片状态文本"""
        self.picture_status.setText(status_text)

    def get_qr_params(self):
        """获取普通二维码参数"""
        try:
            margin = int(self.margin_spinbox.text().replace(' px', ''))
        except:
            margin = 0
        size = int(self.size_combobox.currentText().split('×')[0].strip())
        version = int(self.version_combobox.currentText())

        return {
            'version': version,
            'size': size,
            'margin': margin
        }

    def get_personal_params(self):
        """获取个性化二维码参数"""
        return {
            'picture_path': self.picture_path,
            'colorized': self.check_colorized.isChecked()
        }

    def show_qrcode(self, qrcode_img):
        """显示二维码图片"""
        self.qr_img = qrcode_img
        if hasattr(qrcode_img, 'save'):  # PIL Image
            # 将PIL图片转换为QPixmap显示
            import io
            fp = io.BytesIO()
            qrcode_img.save(fp, 'BMP')
            fp.seek(0)
            qimg = QtGui.QImage()
            qimg.loadFromData(fp.getvalue())
            qimg_pixmap = QtGui.QPixmap.fromImage(qimg)
        else:  # QImage or QPixmap
            qimg_pixmap = qrcode_img if isinstance(qrcode_img, QtGui.QPixmap) else QtGui.QPixmap.fromImage(qrcode_img)

        scaled_pixmap = qimg_pixmap.scaled(
            self.show_label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.show_label.setPixmap(scaled_pixmap)

    def show_status_message(self, message, timeout=0):
        """显示状态栏消息"""
        self.status_bar.showMessage(message, timeout)

    def select_picture_file(self):
        """选择背景图片文件对话框"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择背景图片", "",
            "图片文件 (*.png *.jpg *.jpeg *.gif *.bmp)"
        )
        return file_path

    def show_preview_context_menu(self, position):
        """显示预览区域的右键菜单"""
        # 检查是否有图片显示
        if not hasattr(self, 'qr_img') or self.qr_img is None:
            return

        # 创建右键菜单
        context_menu = QtWidgets.QMenu(self)

        # 复制图片动作
        copy_action = context_menu.addAction('复制图片')
        copy_action.triggered.connect(self.copy_preview_image)

        # 保存图片动作
        save_action = context_menu.addAction('保存图片')
        save_action.triggered.connect(self.save_preview_image)

        # 显示菜单
        context_menu.exec(self.show_label.mapToGlobal(position))

    def copy_preview_image(self):
        """复制预览图片到剪贴板"""
        try:
            if hasattr(self, 'qr_img') and self.qr_img is not None:
                from PySide6.QtWidgets import QApplication
                from PySide6.QtGui import QPixmap
                import io

                # 将PIL图片转换为QPixmap
                if hasattr(self.qr_img, 'save'):  # PIL Image
                    buffer = io.BytesIO()
                    self.qr_img.save(buffer, 'BMP')
                    buffer.seek(0)
                    qimg = QImage()
                    qimg.loadFromData(buffer.getvalue())
                    pixmap = QPixmap.fromImage(qimg)
                else:  # 已经是QImage或QPixmap
                    pixmap = self.qr_img if isinstance(self.qr_img, QPixmap) else QPixmap.fromImage(self.qr_img)

                # 复制到剪贴板
                clipboard = QApplication.clipboard()
                clipboard.setPixmap(pixmap)

                self.show_status_message('✓ 图片已复制到剪贴板', 3000)
            else:
                QMessageBox.warning(self, '错误', '没有可复制的图片')
        except Exception as e:
            QMessageBox.warning(self, '错误', f'复制图片失败: {e}')

    def save_preview_image(self):
        """保存预览图片"""
        try:
            if hasattr(self, 'qr_img') and self.qr_img is not None:
                filename, _ = QFileDialog.getSaveFileName(
                    self, '保存图片', './qrcode.png',
                    '图片文件 (*.png *.jpg *.jpeg *.bmp);;PNG文件 (*.png);;JPEG文件 (*.jpg *.jpeg);;BMP文件 (*.bmp);;所有文件 (*)'
                )
                if filename:
                    self.qr_img.save(filename)
                    QMessageBox.information(self, '成功', '图片保存成功！')
                    self.show_status_message(f'✓ 图片已保存: {filename}', 5000)
            else:
                QMessageBox.warning(self, '错误', '没有可保存的图片')
        except Exception as e:
            QMessageBox.warning(self, '错误', f'保存图片失败: {e}')