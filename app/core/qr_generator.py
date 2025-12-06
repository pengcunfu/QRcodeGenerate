"""
二维码生成器业务逻辑类
负责所有二维码/条形码相关的核心功能
"""
import io
import qrcode
import barcode
from barcode.writer import ImageWriter
from pyzbar.pyzbar import decode
from PIL import Image
from MyQR import myqr
from PySide6 import QtWidgets, QtGui
from PySide6.QtWidgets import QProgressDialog, QMessageBox
from PySide6.QtGui import QImage


class QRCodeGenerator:
    """二维码生成器业务逻辑类"""

    def __init__(self):
        pass

    def generate_simple_qrcode(self, content, params=None):
        """
        生成普通二维码

        Args:
            content (str): 二维码内容
            params (dict): 参数字典，包含version, size, margin

        Returns:
            PIL.Image: 生成的二维码图片
        """
        if not content:
            content = "Hello World"

        if params is None:
            params = {'version': 1, 'size': 232, 'margin': 4}

        try:
            margin = params.get('margin', 4)
            size = params.get('size', 232)
            version = params.get('version', 1)

            qr = qrcode.QRCode(
                version=version,
                error_correction=qrcode.ERROR_CORRECT_L,
                box_size=size // 29,
                border=margin
            )
            qr.add_data(content)
            qr_img = qr.make_image()
            return qr_img

        except Exception as e:
            raise Exception(f"普通二维码生成失败: {e}")

    def generate_personal_qrcode(self, content, params=None):
        """
        生成个性化二维码

        Args:
            content (str): 二维码内容
            params (dict): 参数字典，包含picture_path, colorized

        Returns:
            PIL.Image: 生成的二维码图片
        """
        if not content:
            raise ValueError("请输入二维码内容")

        if params is None:
            params = {'picture_path': '', 'colorized': True}

        try:
            import tempfile
            import os

            # 创建临时文件保存个性化二维码
            temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
            temp_path = temp_file.name
            temp_file.close()

            picture_path = params.get('picture_path', '')
            colorized = params.get('colorized', True)

            if picture_path:
                # 有背景图片的个性化二维码
                myqr.run(
                    words=content,
                    picture=picture_path,
                    colorized=colorized,
                    save_name=temp_path
                )
            else:
                # 无背景图片的普通个性化二维码
                myqr.run(words=content, save_name=temp_path)

            # 加载生成的二维码
            qr_img = Image.open(temp_path)

            # 清理临时文件
            os.unlink(temp_path)

            return qr_img

        except Exception as e:
            raise Exception(f"个性化二维码生成失败: {e}")

    def generate_barcode(self, content):
        """
        生成条形码

        Args:
            content (str): 条形码内容

        Returns:
            PIL.Image: 生成的条形码图片
        """
        if not content:
            raise ValueError("请输入内容")

        try:
            code128 = barcode.get('code128', content, writer=ImageWriter())
            fp = io.BytesIO()
            code128.write(fp)
            fp.seek(0)
            img = Image.open(fp)
            return img

        except Exception as e:
            raise Exception(f"条形码生成失败: {e}")

    def recognize_code(self, image_path):
        """
        识别二维码/条形码

        Args:
            image_path (str): 图片文件路径

        Returns:
            list: 识别结果列表
        """
        try:
            img = Image.open(image_path)
            results = decode(img)
            return results

        except Exception as e:
            raise Exception(f"图片识别失败: {e}")

    def recognize_clipboard(self):
        """
        识别剪贴板中的二维码/条形码

        Returns:
            list: 识别结果列表
        """
        try:
            from PySide6.QtWidgets import QApplication
            from PySide6.QtGui import QImage
            from PySide6.QtCore import QBuffer, QIODevice
            import io

            clipboard = QApplication.clipboard()
            mime_data = clipboard.mimeData()

            # 检查剪贴板是否包含图片
            if mime_data.hasImage():
                # 获取剪贴板中的图片
                qimage = clipboard.image()
                if not qimage.isNull():
                    # 将QImage转换为PIL Image
                    buffer = QBuffer()
                    buffer.open(QIODevice.ReadWrite)
                    qimage.save(buffer, "BMP")
                    pil_image = Image.open(io.BytesIO(buffer.data()))

                    # 识别二维码/条形码
                    results = decode(pil_image)
                    return results

            elif mime_data.hasText():
                # 检查是否是图片文件的路径
                text = mime_data.text().strip()
                if text.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    try:
                        # 尝试作为文件路径打开
                        img = Image.open(text)
                        results = decode(img)
                        return results
                    except:
                        # 如果不是有效的图片文件路径，继续其他检查
                        pass

            raise Exception("剪贴板中没有有效的二维码图片")

        except Exception as e:
            raise Exception(f"剪贴板识别失败: {e}")

    def batch_generate_qrcodes(self, parent_widget, batch_data):
        """
        批量生成二维码

        Args:
            parent_widget: 父窗口
            batch_data (dict): 批量生成数据

        Returns:
            tuple: (成功数量, 失败数量)
        """
        lines = batch_data.get('lines', [])
        output_dir = batch_data.get('output_dir', '')
        prefix = batch_data.get('prefix', '')
        format_type = batch_data.get('format', 'png')
        version = batch_data.get('version', 1)
        size = batch_data.get('size', 200)
        margin = batch_data.get('margin', 4)

        if not lines:
            raise ValueError("没有有效的数据")

        if not output_dir:
            raise ValueError("请选择输出目录")

        # 处理文件名前缀
        if prefix and not prefix.endswith('_'):
            prefix += '_'

        # 创建进度对话框
        progress = QProgressDialog('正在生成二维码...', '取消', 0, len(lines), parent_widget)
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
                filename = f"{prefix}qrcode_{i+1}.{format_type}"
                filepath = f"{output_dir}/{filename}"

                try:
                    # 生成二维码
                    qr = qrcode.QRCode(
                        version=version,
                        error_correction=qrcode.ERROR_CORRECT_L,
                        box_size=size // 29,
                        border=margin
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
            return success_count, error_count

        except Exception as e:
            raise Exception(f"批量生成过程中发生错误: {e}")

    @staticmethod
    def show_error_message(parent, title, message):
        """显示错误消息"""
        QMessageBox.warning(parent, title, message)

    @staticmethod
    def show_info_message(parent, title, message):
        """显示信息消息"""
        QMessageBox.information(parent, title, message)

    @staticmethod
    def show_about_message(parent, title, message):
        """显示关于消息"""
        QMessageBox.about(parent, title, message)


class QRCodeController:
    """二维码生成器控制器类"""

    def __init__(self, ui_window):
        self.ui = ui_window
        self.generator = QRCodeGenerator()
        self.setup_connections()

    def setup_connections(self):
        """设置信号连接"""
        # 连接按钮信号
        self.ui.generate_button.clicked.connect(self.on_generate_qrcode)
        self.ui.save_button.clicked.connect(self.on_save_qrcode)
        self.ui.margin_spinbox.valueChanged.connect(self.on_generate_qrcode)
        self.ui.generate_barcode_button.clicked.connect(self.on_generate_barcode)
        self.ui.recognize_button.clicked.connect(self.on_recognize_code)
        self.ui.clipboard_button.clicked.connect(self.on_recognize_clipboard)
        self.ui.picture_button.clicked.connect(self.on_select_picture)

        # 连接单选按钮信号
        self.ui.radio_simple.toggled.connect(self.on_toggle_qr_type)

        # 连接菜单动作信号
        self.ui.batch_action.triggered.connect(self.on_batch_generate_qrcodes)
        self.ui.about_action.triggered.connect(self.on_show_about)

    def on_generate_qrcode(self):
        """生成二维码按钮点击事件"""
        content = self.ui.get_content()

        try:
            if self.ui.get_current_qr_type() == 'simple':
                # 生成普通二维码
                params = self.ui.get_qr_params()
                qr_img = self.generator.generate_simple_qrcode(content, params)
                self.ui.show_qrcode(qr_img)
                self.ui.show_status_message('✓ 普通二维码生成成功', 3000)
            else:
                # 生成个性化二维码
                params = self.ui.get_personal_params()
                qr_img = self.generator.generate_personal_qrcode(content, params)
                self.ui.show_qrcode(qr_img)
                self.ui.show_status_message('✓ 个性化二维码生成成功', 3000)

        except Exception as e:
            self.generator.show_error_message(self.ui, '错误', str(e))
            self.ui.show_status_message('✗ 生成失败', 3000)

    def on_save_qrcode(self):
        """保存图片按钮点击事件"""
        if not hasattr(self.ui, 'qr_img') or self.ui.qr_img is None:
            self.generator.show_error_message(self.ui, '错误', '请先生成二维码或条形码')
            return

        try:
            from PySide6.QtWidgets import QFileDialog

            filename, _ = QFileDialog.getSaveFileName(
                self.ui, '保存图片', './qrcode.png',
                '图片文件 (*.png);;所有文件 (*)'
            )
            if filename:
                self.ui.qr_img.save(filename)
                self.generator.show_info_message(self.ui, '成功', '图片保存成功！')
                self.ui.show_status_message(f'✓ 图片已保存: {filename}', 5000)

        except Exception as e:
            self.generator.show_error_message(self.ui, '错误', f'保存失败: {e}')

    def on_generate_barcode(self):
        """生成条形码按钮点击事件"""
        content = self.ui.get_content()

        try:
            barcode_img = self.generator.generate_barcode(content)
            self.ui.show_qrcode(barcode_img)
            self.ui.show_status_message('✓ 条形码生成成功', 3000)

        except Exception as e:
            self.generator.show_error_message(self.ui, '错误', str(e))
            self.ui.show_status_message('✗ 条形码生成失败', 3000)

    def on_recognize_code(self):
        """识别图片按钮点击事件"""
        try:
            from PySide6.QtWidgets import QFileDialog

            filename, _ = QFileDialog.getOpenFileName(
                self.ui, '选择图片', '',
                '图片文件 (*.png *.jpg *.jpeg *.bmp *.gif);;所有文件 (*)'
            )

            if filename:
                results = self.generator.recognize_code(filename)
                if not results:
                    self.generator.show_info_message(
                        self.ui, '识别结果', '未识别到二维码或条形码内容'
                    )
                    self.ui.show_status_message('⚠ 未识别到内容', 3000)
                    return

                msg = '\n'.join([f'{r.type}: {r.data.decode()}' for r in results])
                self.generator.show_info_message(
                    self.ui, '识别结果', f'识别成功！\n\n{msg}'
                )
                self.ui.show_status_message('✓ 识别成功', 3000)

        except Exception as e:
            self.generator.show_error_message(self.ui, '错误', f'图片识别失败: {e}')
            self.ui.show_status_message('识别失败', 3000)

    def on_recognize_clipboard(self):
        """识别剪贴板按钮点击事件"""
        try:
            results = self.generator.recognize_clipboard()
            if not results:
                self.generator.show_info_message(
                    self.ui, '识别结果', '剪贴板中未识别到二维码或条形码内容'
                )
                self.ui.show_status_message('⚠ 剪贴板未识别到内容', 3000)
                return

            msg = '\n'.join([f'{r.type}: {r.data.decode()}' for r in results])
            self.generator.show_info_message(
                self.ui, '识别结果', f'剪贴板识别成功！\n\n{msg}'
            )
            self.ui.show_status_message('✓ 剪贴板识别成功', 3000)

        except Exception as e:
            self.generator.show_error_message(self.ui, '错误', f'剪贴板识别失败: {e}')
            self.ui.show_status_message('剪贴板识别失败', 3000)

    def on_select_picture(self):
        """选择背景图片按钮点击事件"""
        file_path = self.ui.select_picture_file()
        if file_path:
            self.ui.picture_path = file_path
            filename = file_path.split("/")[-1] if "/" in file_path else file_path.split("\\")[-1]
            if len(filename) > 20:
                filename = filename[:17] + "..."
            self.ui.set_picture_status(f'✓ {filename}')
            self.ui.show_status_message(f'背景图片已选择: {filename}', 3000)

    def on_toggle_qr_type(self):
        """切换二维码类型事件"""
        is_simple = self.ui.radio_simple.isChecked()

        # 普通二维码参数控件的可见性
        self.ui.version_combobox.setEnabled(is_simple)
        self.ui.size_combobox.setEnabled(is_simple)
        self.ui.margin_spinbox.setEnabled(is_simple)

        # 个性化选项的可见性
        self.ui.picture_button.setEnabled(not is_simple)
        self.ui.check_colorized.setEnabled(not is_simple)
        self.ui.picture_status.setEnabled(not is_simple)

    def on_batch_generate_qrcodes(self):
        """批量生成二维码菜单事件"""
        from ui.main_window import BatchGenerateDialog
        dialog = BatchGenerateDialog(self.ui)

        # 连接批量生成逻辑
        dialog.setup_batch_logic(self)

        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            self.ui.show_status_message('批量生成完成', 3000)

    def on_batch_generate_with_data(self, batch_data):
        """执行批量生成二维码"""
        try:
            success_count, error_count = self.generator.batch_generate_qrcodes(self.ui, batch_data)

            # 显示结果
            self.generator.show_info_message(
                self.ui, '批量生成完成',
                f'生成完成！\n'
                f'成功: {success_count} 个\n'
                f'失败: {error_count} 个\n'
                f'输出目录: {batch_data.get("output_dir", "")}'
            )

            if success_count > 0:
                self.ui.parent().accept()

        except Exception as e:
            self.generator.show_error_message(self.ui, '错误', f'批量生成过程中发生错误: {e}')

    def on_show_about(self):
        """显示关于对话框"""
        self.generator.show_about_message(
            self.ui, '关于',
            '二维码/条形码生成工具\n\n'
            '功能：\n'
            '• 生成普通二维码\n'
            '• 生成个性化二维码\n'
            '• 生成条形码\n'
            '• 识别二维码/条形码\n'
            '• 批量生成二维码\n\n'
            '版本：1.0'
        )

    def initialize(self):
        """初始化控制器"""
        # 生成初始二维码
        self.on_generate_qrcode()