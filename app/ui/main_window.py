"""
主窗口界面类
负责所有GUI界面的创建和布局
"""
import sys
from PySide6 import QtWidgets, QtGui
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QPushButton,
                                QComboBox, QSpinBox, QFileDialog, QMessageBox,
                                QRadioButton, QButtonGroup, QCheckBox, QVBoxLayout,
                                QHBoxLayout, QFormLayout, QGroupBox, QStatusBar,
                                QMainWindow, QTextEdit, QProgressDialog)
from PySide6.QtGui import QPixmap, QFont, QImage
from PySide6.QtCore import Qt


class QrCodeGUI(QMainWindow):
    """二维码生成工具主窗口界面类"""

    def __init__(self, parent=None):
        super().__init__()
        self.setMinimumSize(900, 650)
        self.setWindowTitle('二维码/条形码生成工具')

        # 初始化变量
        self.picture_path = ""

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
        self.clipboard_button = QPushButton('识别剪贴板')
        self.clipboard_button.setMinimumHeight(36)
        function_layout.addWidget(self.save_button)
        function_layout.addWidget(self.recognize_button)
        function_layout.addWidget(self.clipboard_button)

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

        # 帮助菜单
        help_menu = menubar.addMenu('帮助(&H)')

        # 关于
        about_action = QtGui.QAction('关于(&A)', self)
        about_action.setStatusTip('关于此应用程序')
        help_menu.addAction(about_action)

        # 返回菜单动作供外部连接信号
        self.batch_action = batch_action
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


class BatchGenerateDialog(QtWidgets.QDialog):
    """批量生成二维码对话框"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('批量生成二维码')
        self.setModal(True)
        self.setMinimumSize(600, 500)

        self.setup_ui()

    def setup_ui(self):
        """设置对话框界面"""
        layout = QVBoxLayout(self)

        # 输入区域
        input_group = QGroupBox('输入设置')
        input_layout = QFormLayout()

        self.data_edit = QTextEdit()
        self.data_edit.setPlaceholderText(
            '请输入要生成二维码的内容，每行一个：\n例如：\nhttps://www.example.com\n联系电话：13800138000\n产品名称：XXX'
        )
        self.data_edit.setMinimumHeight(150)

        input_layout.addRow('数据列表:', self.data_edit)
        input_group.setLayout(input_layout)

        # 输出设置
        output_group = QGroupBox('输出设置')
        output_layout = QFormLayout()

        self.output_dir_edit = QLineEdit()
        self.output_dir_edit.setPlaceholderText('选择输出目录...')
        self.output_dir_button = QPushButton('选择目录')

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
        self.cancel_button = QPushButton('取消')

        button_layout.addStretch()
        button_layout.addWidget(self.generate_button)
        button_layout.addWidget(self.cancel_button)

        # 布局组装
        layout.addWidget(input_group)
        layout.addWidget(output_group)
        layout.addWidget(params_group)
        layout.addLayout(button_layout)

    def get_batch_data(self):
        """获取批量生成数据"""
        data_text = self.data_edit.toPlainText().strip()
        lines = [line.strip() for line in data_text.split('\n') if line.strip()]

        return {
            'lines': lines,
            'output_dir': self.output_dir_edit.text().strip(),
            'prefix': self.prefix_edit.text().strip(),
            'format': self.format_combo.currentText().lower(),
            'version': self.version_spin.value(),
            'size': self.size_spin.value(),
            'margin': self.margin_spin.value()
        }

    def select_output_directory(self):
        """选择输出目录对话框"""
        dir_path = QFileDialog.getExistingDirectory(self, '选择输出目录')
        return dir_path

    def setup_batch_logic(self, controller):
        """设置批量生成逻辑连接"""
        self.output_dir_button.clicked.connect(lambda: self.output_dir_edit.setText(self.select_output_directory()))
        self.generate_button.clicked.connect(lambda: controller.on_batch_generate_with_data(self.get_batch_data()))