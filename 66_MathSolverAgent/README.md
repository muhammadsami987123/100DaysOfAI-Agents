# 📚 MathSolverAgent - Day 66 of #100DaysOfAI-Agents

<div align="center">

![MathSolverAgent Banner](https://img.shields.io/badge/MathSolverAgent-Day%2066-blue?style=for-the-badge&logo=calculator&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-API-orange?style=for-the-badge&logo=google&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Web%20Framework-red?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-Frontend-blueviolet?style=for-the-badge&logo=react&logoColor=white)

**Solve math equations step-by-step with clear logic and explanation using AI.**

[🚀 Quick Start](#-quick-start) • [📖 Features](#-features) • [🎭 Examples](#-examples) • [🏗️ Project Architecture](#%EF%B8%8F-project-architecture) • [🤝 Contributing](#-contributing)

</div>

---

## ✨ What is MathSolverAgent?

MathSolverAgent is an intelligent AI-powered mathematics assistant designed to solve complex math equations step-by-step. It aims to provide clear, understandable explanations for each step, making learning interactive and helpful rather than just result-based. This agent uses the Google Gemini API to deliver real-time, comprehensive solutions through a modern web UI.

### 🌟 Key Highlights

-   **🌐 Web UI:** Intuitive and responsive web interface built with React, Shadcn-UI, and Tailwind CSS for seamless interaction.
-   **💡 Step-by-step Solutions:** Provides detailed, logical explanations for each stage of solving a math problem.
-   **➕ Diverse Topics:** Capable of handling various mathematical domains including Arithmetic, Algebra, Geometry, Calculus, and Word problems.
-   **➗ LaTeX Support:** Understands and generates mathematical expressions using LaTeX for precise representation.
-   **📈 Visual Graph Descriptions:** Describes relevant visual graphs and concepts where applicable.
-   **🌍 Multilingual Support:** Accepts input in multiple languages (e.g., English, Urdu) and provides solutions accordingly.
-   **🗂️ Structured Output:** Delivers responses in a clean, organized, and easy-to-read format.
-   **⚡ Streaming Mode:** Utilizes the Google Gemini API in streaming mode for real-time explanations, enhancing user experience.

## 🎯 Features

### 🚀 Core Functionality
-   ✅ **AI Math Solving**: Powered by Google Gemini API for high-quality problem-solving.
-   ✅ **Interactive Streaming**: Solutions appear in real-time, enhancing user engagement.
-   ✅ **Smart Problem Processing**: Understands context and provides relevant, accurate solutions.
-   ✅ **Error Handling**: Robust error handling with user-friendly messages for a smooth experience.

### 💻 User Interface
-   ✅ **Modern React UI**: Built with React, Vite, Shadcn-UI, and Tailwind CSS for a modern and responsive design.
-   ✅ **Integrated Frontend/Backend**: The FastAPI backend serves the React frontend, allowing for a single-command launch.
-   ✅ **File Upload Area**: Supports uploading images or PDFs for problem input (future enhancement).
-   ✅ **Quick Actions**: Pre-defined prompts for common math problems to get started instantly.
-   ✅ **Theme Toggle**: Switch between light and dark modes.

## 🚀 Quick Start

### 📋 Prerequisites

-   **Python 3.8+** installed on your system
-   **Node.js and npm** (or Yarn/Bun) for frontend development (installed automatically by `install.bat`)
-   **Google Gemini API Key** (get one from [Google AI Studio](https://aistudio.google.com/app/apikey))
-   **Internet connection** for AI problem-solving

### ⚡ One-Click Installation & Setup

1.  **Navigate to the project directory:**
    ```bash
    cd 66_MathSolverAgent
    ```
2.  **Run the installer script:**
    ```bash
    install.bat
    ```
    This script will:
    -   ✅ Check Python installation.
    -   ✅ Create a Python virtual environment.
    -   ✅ Install all backend Python dependencies.
    -   ✅ Navigate to `mathmate-ui`, install its Node.js dependencies (`npm install`).
    -   ✅ Build the frontend application (`npm run build`).
    -   ✅ Copy the built frontend files to the backend's `static/assets` directory.
    -   ✅ Create a `.env` file template if one doesn't exist.
    -   ✅ Verify essential Python imports.

3.  **Configure your Google Gemini API Key:**
    Open the `.env` file created in the `66_MathSolverAgent` directory and replace `your_gemini_api_key_here` with your actual API key:
    ```env
    GEMINI_API_KEY=your_gemini_api_key_here
    DEBUG=True # Set to False for production
    ```

### 🎯 Running the Application (Frontend & Backend Combined)

The frontend is served directly by the backend, so you only need to run one command to launch both:

1.  **Launch the server:**
    ```bash
    start.bat
    ```
    This script will:
    -   ✅ Activate the Python virtual environment.
    -   ✅ Ensure all dependencies are installed.
    -   ✅ Start the FastAPI backend server using `uvicorn`.

2.  **Access the Web UI:**
    Open your web browser and navigate to `http://localhost:8000`. The MathSolverAgent UI will be accessible directly.

3.  **Start Solving!**
    Enter your math problem in the input box and click the "Send" button to get step-by-step solutions from the AI agent.

### 🔄 Frontend Changes & Rebuild

If you make any changes to the frontend source files within `mathmate-ui/src`:

1.  **Navigate to the `mathmate-ui` directory:**
    ```bash
    cd 66_MathSolverAgent\mathmate-ui
    ```
2.  **Rebuild the frontend:**
    ```bash
    npm run build
    ```
3.  **Navigate back to the main project directory:**
    ```bash
    cd ..
    ```
4.  **Copy the new build files:**
    ```bash
    xcopy /E /I /Y mathmate-ui\dist static\assets
    ```
5.  **Restart the backend server** (stop it with `Ctrl+C` and then run `start.bat` again) to serve the updated frontend.

## 🎭 Examples & Usage

### 🌐 Web Interface

The web interface provides an interactive experience for math problem-solving:

1.  **📝 Enter Your Problem**: Type your math question or equation in the input box.
2.  **🚀 Get Solution**: Click the "Send" button (paper airplane icon) and watch the AI generate a step-by-step solution.
3.  **📂 File Upload (Planned)**: Use the upload area to add images or PDFs of problems (functionality to be fully implemented).

### Example Input (via Web UI):

`Solve 3x² - 12x = 0`

### Example Output (via Web UI):

(Displayed step-by-step in the browser, followed by the final answer from the AI agent)

## 🏗️ Project Architecture

### 📁 File Structure

```
66_MathSolverAgent/
├── main.py                 # FastAPI application to serve the UI and API
├── config.py               # Configuration settings (API keys, host, port)
├── math_agent.py           # Core logic for solving math problems using Gemini API
├── requirements.txt        # Python dependencies
├── install.bat             # Windows installation script
├── start.bat               # Windows startup script
├── static/                 # Static assets for the web UI
│   └── assets/             # Frontend build files (HTML, CSS, JS from mathmate-ui/dist)
├── mathmate-ui/            # Source code for the React frontend application
│   ├── public/             # Public assets for the frontend
│   ├── src/                # Frontend source files (React components, pages, etc.)
│   ├── index.html          # Frontend entry point (copied to static/assets)
│   ├── package.json        # Frontend dependencies and scripts
│   └── ...                 # Other frontend configuration and files
└── README.md               # This comprehensive documentation
```

### 🔧 Technical Stack

| Component         | Technology                  | Purpose                                        |
|:------------------|:----------------------------|:-----------------------------------------------|
| **Backend**       | Python 3.8+                 | Core application logic                         |
| **AI Engine**     | Google Gemini API           | Math problem-solving and explanations          |
| **Web Framework** | FastAPI                     | REST API and web server                        |
| **Frontend**      | React, Vite, Shadcn-UI, Tailwind CSS | Modern, responsive user interface            |
| **Server**        | Uvicorn                     | ASGI web server                                |
| **Environment**   | Python Virtual Environment, npm | Dependency management and build processes      |

### 🎯 Key Components

#### 🤖 MathSolverAgent (`math_agent.py`)
-   **Core AI Logic**: Handles Google Gemini API integration.
-   **Problem Solving**: Interprets math problems and generates step-by-step solutions.
-   **Structured Output**: Formats AI responses for clarity and readability.

#### 🌐 FastAPI Application (`main.py`)
-   **API Endpoint (`/api/solve`)**: Receives math problems from the frontend and delegates to `MathSolverAgent`.
-   **Static File Serving**: Serves the built React frontend application.
-   **Configuration Loading**: Loads settings from `config.py` and `.env`.

#### 🎨 Frontend (`mathmate-ui/`)
-   **Interactive UI**: Provides a modern and responsive chat-like interface.
-   **Message Handling**: Sends user input to the backend and displays AI responses.
-   **Real-time Interaction**: Facilitates seamless communication with the backend.

#### ⚙️ Configuration (`config.py`)
-   **Settings Management**: Centralized configuration.
-   **Environment Variables**: Manages API keys, host, port, and debug settings.
-   **Validation**: Ensures critical configurations like `GEMINI_API_KEY` are set.

## 🤝 Contributing

We welcome contributions to make MathSolverAgent even better!

### 🛠️ How to Contribute

1.  **Fork the repository**.
2.  **Create a feature branch**: `git checkout -b feature/your-feature-name`.
3.  **Make your changes** and test thoroughly.
4.  **Commit your changes**: `git commit -m 'Add your feature description'`.
5.  **Push to the branch**: `git push origin feature/your-feature-name`.
6.  **Open a Pull Request**.

### 🎯 Areas for Contribution

-   **Frontend Enhancements**: Improve UI/UX, add new components.
-   **Backend Logic**: Refine problem-solving capabilities, add new math domains.
-   **Error Handling**: Enhance robustness and user feedback.
-   **Documentation**: Improve guides and examples.
-   **Testing**: Add more test cases for both frontend and backend.
-   **Integrations**: Explore new APIs or tools.

### 📋 Contribution Guidelines

-   Follow the existing code style.
-   Add tests for new features.
-   Update documentation as needed.
-   Ensure all tests pass.
-   Be respectful and constructive.

## 📞 Support & Community

### 🆘 Getting Help

1.  **📖 Documentation**: Check this README and code comments.
2.  **🔍 Troubleshooting**: Review common issues and solutions.
3.  **📊 Logs**: Check terminal output for error messages.
4.  **🌐 API Status**: Verify Google Gemini API is operational.

### 🐛 Reporting Issues

When reporting issues, please include:
-   **System Information**: OS, Python version, Node.js/npm version, browser.
-   **Error Messages**: Full error output from the terminal and browser console.
-   **Steps to Reproduce**: What you were doing when the issue occurred.
-   **Expected vs Actual**: What you expected to happen versus what actually happened.

### 💬 Community

-   **GitHub Issues**: Report bugs and request features.
-   **Discussions**: Ask questions and share ideas.

## 📄 License & Credits

### 📜 License

This project is part of the **#100DaysOfAI-Agents** challenge by **Muhammad Sami Asghar Mughal**.

**MIT License** - Feel free to use, modify, and distribute!

### 🙏 Acknowledgments

-   **Google AI** for providing the Gemini API.
-   **FastAPI** team for the excellent web framework.
-   **React** and **Vite** communities for robust frontend tools.
-   **Shadcn-UI** and **Tailwind CSS** for modern UI components.
-   **Python community** for amazing libraries.
-   **All contributors** who help improve this project.

### 🌟 Inspiration

This project was inspired by the need for intelligent math-solving tools that are:
-   **Accessible**: Easy to use for everyone.
-   **Powerful**: Capable of generating high-quality, step-by-step solutions.
-   **Flexible**: Supporting multiple genres and languages.
-   **Fun**: Making story creation enjoyable.

---

<div align="center">

## 🎉 Ready to Solve Math Problems?

**Transform your math challenges into clear, step-by-step solutions with the power of AI!**

[🚀 Quick Start](#-quick-start) • [📖 Features](#-features) • [🎭 Examples](#-examples)

---

**Made with ❤️ by the #100DaysOfAI-Agents community**

*Day 66 of 100 - Building the future of AI agents, one day at a time!*

</div>
