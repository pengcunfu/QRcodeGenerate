<div align="center">

# 🔲 QR Code & Barcode Generator

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![PySide6](https://img.shields.io/badge/PySide6-6.0+-green.svg)](https://pypi.org/project/PySide6/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**A modern desktop application for generating and recognizing QR codes and barcodes**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Screenshots](#-screenshots) • [Build](#-build)

</div>

---

## ✨ Features

### 🎯 QR Code Generation
- **Standard QR Codes** - Customizable version, size, and margin settings
- **Personalized QR Codes** - Add background images with colorization effects
- **Batch Processing** - Generate multiple QR codes efficiently

### 📊 Barcode Support
- **Code128 Format** - Industry-standard barcode generation
- **High Quality Output** - Export in PNG format with customizable resolution

### 🔍 Recognition Engine
- **Multi-format Support** - Recognize QR codes and various barcode formats
- **Image Processing** - Support for PNG, JPG, JPEG, BMP, and GIF files
- **Fast Detection** - Powered by pyzbar for accurate recognition

### 🎨 Modern UI
- **Clean Interface** - Intuitive design with Fusion style
- **Real-time Preview** - Instant visual feedback
- **Status Notifications** - Clear operation status updates
- **Responsive Layout** - Adaptive window sizing

---

## 📦 Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/QRcodeGenerate.git
   cd QRcodeGenerate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

### Dependencies

| Package | Version | Purpose |
|---------|---------|----------|
| PySide6 | Latest | GUI framework |
| qrcode | Latest | Standard QR code generation |
| MyQR | Latest | Personalized QR codes with images |
| python-barcode | Latest | Barcode generation |
| pyzbar | Latest | QR/Barcode recognition |
| Pillow | Latest | Image processing |
| pyinstaller | Latest | Application packaging |

> **Note**: For `pyzbar` to work properly, you need to install the ZBar library:
> - **Windows**: Download from [ZBar Downloads](http://zbar.sourceforge.net/download.html)
> - **Linux**: `sudo apt-get install libzbar0`
> - **macOS**: `brew install zbar`

---

## 🚀 Usage

### Standard QR Code
1. Select **"Standard QR Code"** from the menu
2. Enter your content in the text field
3. Adjust parameters:
   - **Version**: QR code version (1-40)
   - **Size**: Output dimensions
   - **Margin**: Border width in pixels
4. Click **"📱 Generate QR Code"**

### Personalized QR Code
1. Select **"Personalized QR Code"** from the menu
2. Enter your content
3. Click **"Select Image"** to add a background
4. Toggle **"Enable Color Effect"** for colorization
5. Click **"📱 Generate QR Code"**

### Barcode Generation
1. Enter alphanumeric content
2. Click **"📊 Generate Barcode"**
3. Preview appears in the display area

### Save Generated Images
- Click **"💾 Save Image"**
- Choose your destination and filename
- Image saved as PNG format

### Recognition
1. Click **"🔍 Recognize Image"**
2. Select an image file containing QR code or barcode
3. Recognition results displayed in a dialog

---

## 📸 Screenshots

<div align="center">

### Main Interface
*Modern, clean UI with intuitive controls*

### QR Code Generation
*Support for both standard and personalized QR codes*

### Barcode Generation
*Code128 barcode format support*

</div>

---

## 🏗️ Build

### Package as Executable

The project includes automated build scripts for creating standalone executables:

#### Windows
```bash
build.bat
```

#### Linux/macOS
```bash
chmod +x build.sh
./build.sh
```

#### Manual Build
```bash
pip install pyinstaller
pyinstaller --clean build.spec
```

The executable will be generated in the `dist/` directory:
- **Windows**: `dist/QRCodeGenerator.exe`
- **Linux/macOS**: `dist/QRCodeGenerator`

For detailed packaging instructions, see [PACKAGING_GUIDE.md](PACKAGING_GUIDE.md)

---

## 📁 Project Structure

```
QRcodeGenerate/
├── main.py              # Main application entry point
├── requirements.txt     # Python dependencies
├── build.spec          # PyInstaller configuration
├── build.bat           # Windows build script
├── build.sh            # Linux/macOS build script
├── README.md           # Project documentation (Chinese)
├── README.en.md        # Project documentation (English)
└── PACKAGING_GUIDE.md  # Detailed packaging instructions
```

---

## 🛠️ Development

### Code Style
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions and classes

### Testing
- Test all features before committing
- Verify cross-platform compatibility
- Check UI responsiveness

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [PySide6](https://www.qt.io/qt-for-python) - Qt for Python
- [qrcode](https://github.com/lincolnloop/python-qrcode) - Pure Python QR Code generator
- [MyQR](https://github.com/sylnsfar/qrcode) - Artistic QR Code generator
- [python-barcode](https://github.com/WhyNotHugo/python-barcode) - Barcode generator
- [pyzbar](https://github.com/NaturalHistoryMuseum/pyzbar) - ZBar wrapper for Python

---

<div align="center">

**Made with ❤️ using Python and PySide6**

[⬆ Back to top](#-qr-code--barcode-generator)

</div>