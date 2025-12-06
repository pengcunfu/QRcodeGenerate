"""
二维码扫描器引擎
负责所有二维码和条形码的识别功能
"""
import io
from PIL import Image
from pyzbar.pyzbar import decode


class QRCodeScanner:
    """二维码扫描器核心业务逻辑类"""

    def __init__(self):
        pass

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

    def get_clipboard_info(self):
        """
        获取剪贴板信息（用于调试）

        Returns:
            dict: 剪贴板信息
        """
        try:
            from PySide6.QtWidgets import QApplication

            clipboard = QApplication.clipboard()
            mime_data = clipboard.mimeData()

            info = {
                'has_text': mime_data.hasText(),
                'has_image': mime_data.hasImage(),
                'has_urls': mime_data.hasUrls(),
                'formats': mime_data.formats()
            }

            if mime_data.hasText():
                info['text'] = mime_data.text()[:100] + ('...' if len(mime_data.text()) > 100 else '')

            if mime_data.hasImage():
                qimage = clipboard.image()
                info['image_size'] = (qimage.width(), qimage.height()) if not qimage.isNull() else None

            return info

        except Exception as e:
            return {'error': str(e)}