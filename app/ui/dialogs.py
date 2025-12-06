"""
自定义对话框模块
包含应用程序中使用的所有对话框类
"""
from PySide6 import QtWidgets


class RecognizeResultDialog(QtWidgets.QDialog):
    """识别结果对话框"""

    def __init__(self, results, parent=None):
        super().__init__(parent)
        self.setWindowTitle('识别结果')
        self.setModal(True)
        self.setMinimumSize(500, 400)

        self.results = results
        self.setup_ui()

    def setup_ui(self):
        """设置对话框界面"""
        layout = QtWidgets.QVBoxLayout(self)

        # 结果说明
        info_label = QtWidgets.QLabel('识别结果：')
        info_label.setStyleSheet("font-weight: bold; font-size: 12pt;")
        layout.addWidget(info_label)

        # 结果展示区域
        self.result_text = QtWidgets.QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setMinimumHeight(200)

        # 格式化显示结果
        result_text = ""
        if self.results:
            for i, result in enumerate(self.results, 1):
                content = result.data.decode('utf-8')
                result_type = result.type
                result_text += f"结果 {i}:\n"
                result_text += f"类型: {result_type}\n"
                result_text += f"内容: {content}\n"
                if i < len(self.results):
                    result_text += "-" * 40 + "\n"
            self.result_text.setText(result_text)
        else:
            self.result_text.setText("未识别到二维码或条形码内容")

        layout.addWidget(self.result_text)

        # 按钮区域
        button_layout = QtWidgets.QHBoxLayout()

        self.copy_button = QtWidgets.QPushButton('复制内容')
        self.copy_button.clicked.connect(self.copy_content)

        self.copy_all_button = QtWidgets.QPushButton('复制全部')
        self.copy_all_button.clicked.connect(self.copy_all)

        self.close_button = QtWidgets.QPushButton('关闭')
        self.close_button.clicked.connect(self.accept)

        button_layout.addStretch()
        button_layout.addWidget(self.copy_button)
        button_layout.addWidget(self.copy_all_button)
        button_layout.addWidget(self.close_button)

        layout.addLayout(button_layout)

    def copy_content(self):
        """复制识别到的内容"""
        if self.results:
            contents = [result.data.decode('utf-8') for result in self.results]
            content_text = '\n'.join(contents)

            from PySide6.QtWidgets import QApplication
            clipboard = QApplication.clipboard()
            clipboard.setText(content_text)

            QtWidgets.QMessageBox.information(self, '复制成功', f'已复制 {len(contents)} 个识别内容到剪贴板')
        else:
            QtWidgets.QMessageBox.warning(self, '警告', '没有可复制的内容')

    def copy_all(self):
        """复制所有结果信息（包含类型和格式）"""
        all_text = self.result_text.toPlainText()

        from PySide6.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        clipboard.setText(all_text)

        QtWidgets.QMessageBox.information(self, '复制成功', '已复制完整识别结果到剪贴板')


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
        layout = QtWidgets.QVBoxLayout(self)

        # 输入区域
        input_group = QtWidgets.QGroupBox('输入设置')
        input_layout = QtWidgets.QFormLayout()

        self.data_edit = QtWidgets.QTextEdit()
        self.data_edit.setPlaceholderText(
            '请输入要生成二维码的内容，每行一个：\n例如：\nhttps://www.example.com\n联系电话：13800138000\n产品名称：XXX'
        )
        self.data_edit.setMinimumHeight(150)

        input_layout.addRow('数据列表:', self.data_edit)
        input_group.setLayout(input_layout)

        # 输出设置
        output_group = QtWidgets.QGroupBox('输出设置')
        output_layout = QtWidgets.QFormLayout()

        self.output_dir_edit = QtWidgets.QLineEdit()
        self.output_dir_edit.setPlaceholderText('选择输出目录...')
        self.output_dir_button = QtWidgets.QPushButton('选择目录')

        dir_layout = QtWidgets.QHBoxLayout()
        dir_layout.addWidget(self.output_dir_edit)
        dir_layout.addWidget(self.output_dir_button)

        self.prefix_edit = QtWidgets.QLineEdit()
        self.prefix_edit.setPlaceholderText('文件名前缀（可选）')

        self.format_combo = QtWidgets.QComboBox()
        self.format_combo.addItems(['PNG', 'JPEG', 'BMP'])

        output_layout.addRow('输出目录:', dir_layout)
        output_layout.addRow('文件名前缀:', self.prefix_edit)
        output_layout.addRow('图片格式:', self.format_combo)
        output_group.setLayout(output_layout)

        # 二维码参数
        params_group = QtWidgets.QGroupBox('二维码参数')
        params_layout = QtWidgets.QFormLayout()

        self.version_spin = QtWidgets.QSpinBox()
        self.version_spin.setRange(1, 40)
        self.version_spin.setValue(1)

        self.size_spin = QtWidgets.QSpinBox()
        self.size_spin.setRange(100, 1000)
        self.size_spin.setValue(200)
        self.size_spin.setSuffix(' px')

        self.margin_spin = QtWidgets.QSpinBox()
        self.margin_spin.setRange(0, 20)
        self.margin_spin.setValue(4)

        params_layout.addRow('版本:', self.version_spin)
        params_layout.addRow('尺寸:', self.size_spin)
        params_layout.addRow('边距:', self.margin_spin)
        params_group.setLayout(params_layout)

        # 按钮
        button_layout = QtWidgets.QHBoxLayout()
        self.generate_button = QtWidgets.QPushButton('开始生成')
        self.cancel_button = QtWidgets.QPushButton('取消')

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
        from PySide6.QtWidgets import QFileDialog
        dir_path = QFileDialog.getExistingDirectory(self, '选择输出目录')
        return dir_path

    def setup_batch_logic(self, controller):
        """设置批量生成逻辑连接"""
        self.output_dir_button.clicked.connect(lambda: self.output_dir_edit.setText(self.select_output_directory()))
        self.generate_button.clicked.connect(lambda: controller.on_batch_generate_with_data(self.get_batch_data()))