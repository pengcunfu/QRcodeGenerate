"""
二维码生成器引擎
负责所有二维码和条形码的生成功能
"""
import io
import qrcode
import barcode
from barcode.writer import ImageWriter
from PIL import Image
from MyQR import myqr


class QRCodeGenerator:
    """二维码生成器核心业务逻辑类"""

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

    def batch_generate_qrcodes(self, batch_data, progress_callback=None):
        """
        批量生成二维码

        Args:
            batch_data (dict): 批量生成数据
            progress_callback (callable): 进度回调函数，接收(current, total, message)

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

        success_count = 0
        error_count = 0

        try:
            for i, content in enumerate(lines):
                # 调用进度回调
                if progress_callback:
                    cancel = progress_callback(i, len(lines), f'正在生成第 {i+1}/{len(lines)} 个二维码...')
                    if cancel:
                        break

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

            # 调用进度回调完成
            if progress_callback:
                progress_callback(len(lines), len(lines), '生成完成')

            return success_count, error_count

        except Exception as e:
            raise Exception(f"批量生成过程中发生错误: {e}")