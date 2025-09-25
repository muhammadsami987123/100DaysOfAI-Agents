# PhotoOrganizerAgent - Day 53 of #100DaysOfAI-Agents 

### this project is incomplele


[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111+-green.svg)](https://fastapi.tiangolo.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-orange.svg)](https://openai.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Organize your photos by face or location with AI-powered intelligence!** 📸

PhotoOrganizerAgent is a modern application that organizes your photo collection into folders based on detected faces or locations (mocked for demo). It features a beautiful web UI, robust CLI, and professional error handling—perfect for photographers, families, and anyone with a large photo library.

---

## ✨ **Features**

### 🎨 **Modern Web Interface**
- **Tailwind CSS Design** - Responsive, clean, and user-friendly
- **Folder Path Input** - Organize any local folder
- **Mode Selection** - Choose face or location (mocked)
- **Loading & Error States** - Professional feedback for all actions

### 🤖 **AI-Powered (Mocked) Organization**
- **Face/Location Detection** - Simulated for demo (can be extended)
- **Batch Processing** - Organize hundreds of photos at once
- **Safe File Handling** - No data loss, robust error checks

### 🖥️ **Command Line Interface**
- **Interactive CLI** - Organize from terminal with clear prompts
- **Batch Mode** - Scriptable for automation
- **Cross-platform** - Works on Windows, macOS, and Linux

---

## � **Quick Start**

### **Prerequisites**
- Python 3.8 or higher

### **Installation**

1. **Clone the repository**
	```bash
	git clone https://github.com/yourusername/100DaysOfAI-Agents.git
	cd 100DaysOfAI-Agents/53_PhotoOrganizerAgent
	```

2. **Install dependencies**
	```bash
	pip install -r requirements.txt
	```

3. **Set up environment**
	```bash
	cp .env.example .env
	# Edit .env with your settings (if needed)
	```

4. **Start the application**
	```bash
	# Web UI
	python web_app.py
	# CLI
	python main.py organize <your_photo_folder> --mode face
	```

5. **Open your browser**
	```
	http://localhost:8053
	```

---

## 🎯 **Usage Examples**

### **Web Interface**
1. Enter the folder path containing your photos
2. Select organization mode (face/location)
3. Click "Organize Photos"
4. View results and error messages in real time

### **Command Line Interface**
```bash
python main.py organize "D:/Photos" --mode location
```

---

## 🔧 **Configuration**

### **Environment Variables**
Create a `.env` file in the project root:

```env
# OpenAI Configuration (future use)
OPENAI_API_KEY=your_openai_api_key_here
# Default organization mode
ORGANIZE_MODE=face
```

---

## 📁 **Project Structure**

```
53_PhotoOrganizerAgent/
├── static/                # Frontend assets (JS, images)
│   ├── script.js
│   └── banner.png
├── templates/             # HTML templates
│   └── index.html
├── uploads/               # (Reserved for future file uploads)
├── outputs/               # (Reserved for future exports)
├── main.py                # CLI interface
├── web_app.py             # FastAPI web server
├── core/                  # Core logic
│   └── organizer.py
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── .env.example           # Environment template
├── test_installation.py   # Installation verification
└── README.md              # This file
```

---

## 🛠️ **Technical Architecture**

### **Backend Components**
- **FastAPI Web Server** - RESTful endpoints and web UI
- **Photo Organizer** - Core logic for organizing photos
- **Config Loader** - Environment and settings management

### **Frontend Components**
- **Responsive UI** - Tailwind CSS for modern design
- **Interactive Elements** - JavaScript for dynamic feedback
- **Progress Indicators** - Loading and error states

### **Data Flow**
1. **Input Processing** - Validate folder and mode
2. **Mocked Detection** - Assign face/location to each photo
3. **File Operations** - Move photos to subfolders
4. **Result Display** - Show summary and errors

---

## 🧪 **Testing**

### **Installation Testing**
```bash
python test_installation.py
```

### **Manual Testing**
- Test web UI with valid/invalid folders
- Test CLI with all options
- Check error handling and feedback

---

## 🚨 **Troubleshooting**

### **Common Issues**

#### **1. Invalid Folder Path**
```
Error: Folder does not exist
Solution: Check the path and try again
```

#### **2. Permission Denied**
```
Error: Permission denied
Solution: Run as administrator or choose another folder
```

#### **3. No Photos Found**
```
Error: No supported photo files in folder
Solution: Add .jpg/.png files and retry
```

### **Debug Mode**
Add print statements or use a debugger for more details.

---

## 📈 **Performance Tips**
- Organize in batches for large folders
- Avoid network drives for best speed

---

## 🔒 **Security Considerations**
- No files are uploaded to the cloud
- All processing is local
- API keys are never logged or shared

---

## 🤝 **Contributing**
- Fork the repository
- Create a feature branch
- Make your changes and add tests
- Submit a pull request

---

## 📚 **Learning Resources**
- **Python** - [Official Documentation](https://docs.python.org/)
- **FastAPI** - [FastAPI Docs](https://fastapi.tiangolo.com/)
- **Tailwind CSS** - [Tailwind Docs](https://tailwindcss.com/docs)

---

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Made with ❤️ by the 100DaysOfAI-Agents community**

*Organize your memories with AI-powered intelligence!* 📸✨

</div>
