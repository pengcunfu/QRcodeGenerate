<div align="center">

# 🔲 二维码与条形码生成器

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![PySide6](https://img.shields.io/badge/PySide6-6.0+-green.svg)](https://pypi.org/project/PySide6/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**一个用于生成和识别二维码与条形码的现代化桌面应用程序**

[功能特性](#-功能特性) • [安装说明](#-安装说明) • [使用指南](#-使用指南) • [截图展示](#-截图展示) • [构建打包](#-构建打包)

</div>

---

## ✨ 功能特性

### 🎯 二维码生成
- **标准二维码** - 可自定义版本、尺寸和边距设置
- **个性化二维码** - 添加背景图片并支持彩色效果
- **批量处理** - 高效生成多个二维码

### 📊 条形码支持
- **Code128 格式** - 行业标准条形码生成
- **高质量输出** - 导出 PNG 格式，支持自定义分辨率

### 🔍 识别引擎
- **多格式支持** - 识别二维码和各种条形码格式
- **图像处理** - 支持 PNG、JPG、JPEG、BMP 和 GIF 文件
- **快速检测** - 基于 pyzbar 的准确识别

### 🎨 现代化界面
- **简洁界面** - 采用 Fusion 风格的直观设计
- **实时预览** - 即时视觉反馈
- **状态通知** - 清晰的操作状态更新
- **响应式布局** - 自适应窗口大小

---

## 📦 安装说明

### 系统要求
- Python 3.7 或更高版本
- pip 包管理器

### 快速开始

1. **克隆仓库**
   ```bash
   git clone https://github.com/yourusername/QRcodeGenerate.git
   cd QRcodeGenerate
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **运行应用**
   ```bash
   python main.py
   ```

### 依赖包

| 包名 | 版本 | 用途 |
|---------|---------|----------|
| PySide6 | 最新 | GUI 框架 |
| qrcode | 最新 | 标准二维码生成 |
| MyQR | 最新 | 带图片的个性化二维码 |
| python-barcode | 最新 | 条形码生成 |
| pyzbar | 最新 | 二维码/条形码识别 |
| Pillow | 最新 | 图像处理 |
| pyinstaller | 最新 | 应用程序打包 |

> **注意**：为了让 `pyzbar` 正常工作，您需要安装 ZBar 库：
> - **Windows**：从 [ZBar 下载页面](http://zbar.sourceforge.net/download.html) 下载
> - **Linux**：`sudo apt-get install libzbar0`
> - **macOS**：`brew install zbar`

---

## 🚀 使用指南

### 标准二维码
1. 选择 **"普通二维码"**
2. 在文本框中输入您的内容
3. 调整参数：
   - **版本**：二维码版本（1-40）
   - **尺寸**：输出尺寸
   - **边距**：边框宽度（像素）
4. 点击 **"📱 生成二维码"**

### 个性化二维码
1. 选择 **"个性化二维码"**
2. 输入您的内容
3. 点击 **"选择图片"** 添加背景
4. 开启 **"启用彩色效果"** 进行着色
5. 点击 **"📱 生成二维码"**

### 条形码生成
1. 输入字母数字内容
2. 点击 **"📊 生成条形码"**
3. 预览会显示在显示区域

### 保存生成的图片
- 点击 **"💾 保存图片"**
- 选择目标位置和文件名
- 图片保存为 PNG 格式

### 识别功能
1. 点击 **"🔍 识别图片"**
2. 选择包含二维码或条形码的图片文件
3. 识别结果会显示在对话框中

---

## 📸 截图展示

<div align="center">

### 主界面
*现代化、简洁的用户界面，操作直观*

### 二维码生成
*支持标准和个性化二维码*

### 条形码生成
*支持 Code128 条形码格式*

</div>

---

## 🏗️ 构建打包

### 打包为可执行文件

项目包含用于创建独立可执行文件的自动构建脚本：

#### Windows
```bash
build.bat
```

#### Linux/macOS
```bash
chmod +x build.sh
./build.sh
```

#### 手动构建
```bash
pip install pyinstaller
pyinstaller --clean build.spec
```

可执行文件将生成在 `dist/` 目录中：
- **Windows**：`dist/QRCodeGenerator.exe`
- **Linux/macOS**：`dist/QRCodeGenerator`

详细的打包说明请参见 [PACKAGING_GUIDE.md](PACKAGING_GUIDE.md)

---

## 📁 项目结构

```
QRcodeGenerate/
├── main.py              # 主应用程序入口
├── requirements.txt     # Python 依赖
├── build.spec          # PyInstaller 配置
├── build.bat           # Windows 构建脚本
├── build.sh            # Linux/macOS 构建脚本
├── README.md           # 项目文档（中文）
├── README.en.md        # 项目文档（英文）
└── PACKAGING_GUIDE.md  # 详细打包说明
```

---

## 🛠️ 开发

### 代码规范
- 遵循 PEP 8 指南
- 使用有意义的变量名
- 为函数和类添加文档字符串

### 测试
- 提交前测试所有功能
- 验证跨平台兼容性
- 检查 UI 响应性

---

## 🤝 贡献

欢迎贡献！请随时提交 Pull Request。

1. Fork 本仓库
2. 创建您的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

---

## 📝 许可证

本项目基于 MIT 许可证 - 详情请参见 [LICENSE](LICENSE) 文件。

---

## 🙏 致谢

- [PySide6](https://www.qt.io/qt-for-python) - Qt for Python
- [qrcode](https://github.com/lincolnloop/python-qrcode) - 纯 Python 二维码生成器
- [MyQR](https://github.com/sylnsfar/qrcode) - 艺术二维码生成器
- [python-barcode](https://github.com/WhyNotHugo/python-barcode) - 条形码生成器
- [pyzbar](https://github.com/NaturalHistoryMuseum/pyzbar) - Python 的 ZBar 包装器

---

<div align="center">

**使用 Python 和 PySide6 制作 ❤️**

[⬆ 返回顶部](#-二维码与条形码生成器)

</div>