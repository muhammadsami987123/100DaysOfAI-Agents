# 🌐 TSHelperBot — Day 49 of #100DaysOfAI-Agents

<div align="center">

![TSHelperBot](https://img.shields.io/badge/TSHelperBot-AI%20Powered-blue?style=for-the-badge&logo=typescript)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT%20API-purple?style=for-the-badge&logo=openai)
![Rich](https://img.shields.io/badge/Rich-Terminal%20UI-orange?style=for-the-badge&logo=terminal)

**Intelligent Terminal-Based JavaScript/TypeScript Assistant with AI-Powered Suggestions**

[Features](#-features) • [Quick Start](#-quick-start) • [Usage](#-usage) • [Configuration](#-configuration) • [API](#-api) • [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [✨ Features](#-features)
- [🚀 Quick Start](#-quick-start)
- [🎯 Usage](#-usage)
- [🛠️ Configuration](#-configuration)
- [🔧 API Reference](#-api-reference)
- [📁 Project Structure](#-project-structure)
- [🎨 UI Features](#-ui-features)
- [🔒 Safety Features](#-safety-features)
- [🐛 Troubleshooting](#-troubleshooting)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## 🌟 Overview

TSHelperBot is an intelligent, AI-powered terminal assistant that revolutionizes how developers interact with JavaScript and TypeScript code. Whether you're a beginner learning JS/TS or an experienced developer looking to streamline your workflow, TSHelperBot provides intelligent assistance, code generation, and comprehensive explanations for all your JS/TS needs.

### Key Benefits

- **⚡ Speed**: Instant code generation, explanation, refactoring, conversion, and debugging suggestions
- **🧠 Intelligence**: AI-powered explanations and natural language processing
- **🎨 Beautiful UI**: Rich terminal interface with tables, panels, and colors
- **🔄 Multiple Interfaces**: Main menu, quick actions, and direct command processing

---

## ✨ Features

### 🤖 AI-Powered Intelligence
- **OpenAI GPT Integration**: Uses GPT for detailed JS/TS explanations, generation, refactoring, conversion, and debugging
- **Natural Language Processing**: Convert plain language descriptions into valid, semantic JS/TS
- **Code Explanation**: Explain each part's purpose, structure, and best practices
- **Code Optimization**: Suggest improvements, highlight potential issues

### 🎯 Core Capabilities
- **Code Generation**: Generate complete, clean JS/TS structures from descriptions
- **Code Explanation**: Understand and explain existing JS/TS snippets
- **Code Refactoring**: Optimize and clean up JS/TS logic
- **Code Conversion**: Convert code between JavaScript and TypeScript, including type annotations
- **Code Debugging**: Identify and fix syntax or logic errors
- **Help System**: Comprehensive help and documentation

### 🎨 Enhanced User Experience
- **Beautiful Terminal UI**: Rich, colorful interface with tables, panels, and progress indicators
- **Interactive Menus**: Numbered suggestion lists and easy navigation
- **Syntax-Colored Output**: JS/TS output with syntax highlighting
- **Quick Actions**: One-key shortcuts for common JS/TS workflows (to be implemented)

### 🛡️ Safety-First Design (Adapted for JS/TS)
- **Validation Checks**: Generated code can be validated before saving (to be implemented)
- **Error Handling**: Comprehensive error handling and user-friendly messages

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** (3.9+ recommended)
- **OpenAI API Key** ([Get one here](https://platform.openai.com/api-keys)) - Optional for AI features

### Installation

1. **Navigate to the project directory:**
   ```bash
   cd 49_LangChainStarter/TSHelperBot
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up OpenAI API key (optional):**

   **Option A: Environment Variable (Recommended)**
   ```bash
   # Windows (Command Prompt)
   set OPENAI_API_KEY=your_api_key_here

   # Windows (PowerShell)
   $env:OPENAI_API_KEY="your_api_key_here"

   # Linux/Mac
   export OPENAI_API_KEY=your_api_key_here
   ```

   **Option B: .env file**
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_api_key_here
   ```

### First Run

#### Main Menu (Recommended)
```bash
python agent.py --menu
```

#### Interactive Mode (to be implemented for JS/TS-specific quick actions)
```bash
python agent.py --interactive
```

#### Single Command
```bash
python agent.py --generate "responsive header" --lang ts
python agent.py --explain "const x: number = 5;"
python agent.py --refactor "function add(a,b){return a+b}"
python agent.py --convert "let x = 5;" --to ts
python agent.py --debug "function sum(a, b) { return a  b; }"
```

#### Save Output
```bash
python agent.py --generate "basic webpage" --save output.ts
```

---

## 🎯 Usage

### Main Menu System

The main menu provides easy access to all TSHelperBot features:

```
📋 Main Menu
╭─────┬──────────────────────────┬──────────────────────────────────────────╮
│ Key │ Option                   │ Description                              │
├─────┼──────────────────────────┼──────────────────────────────────────────┤
│ 1   │ Generate Code            │ Create JS/TS code from a description     │
│ 2   │ Explain Code             │ Understand existing JS/TS code           │
│ 3   │ Refactor Code            │ Optimize and clean up JS/TS code         │
│ 4   │ Convert JS ↔ TS          │ Convert code between JavaScript and TypeScript │
│ 5   │ Debug Code               │ Identify and fix errors in JS/TS code    │
│ 6   │ Save Output              │ Save generated code to a file            │
│ 7   │ Help                     │ Show help information                    │
│ 0   │ Exit                     │ Leave the application                    │
╰─────┴──────────────────────────┴──────────────────────────────────────────╯
```

### Code Generation Examples

Generate complete JS/TS structures from natural language descriptions:

#### Function to Validate Email (TypeScript)
```bash
Input:  generate "a function to validate an email" --lang ts
Output: (Generated TypeScript function with type annotations)
```

#### Simple React Component (JavaScript)
```bash
Input:  generate "a simple React counter component" --lang js
Output: (Generated JavaScript React component)
```

### Code Explanation Examples

Understand existing JS/TS code with detailed explanations:

#### TypeScript Interface
```bash
Input:  explain "interface User { id: number; name: string; }" --lang ts
Output:
### Explanation for `interface User`
Defines a new type named `User` with properties `id` (number) and `name` (string).
...
```

#### JavaScript Async Function
```bash
Input:  explain "async function fetchData() { const res = await fetch('/api'); return res.json(); }" --lang js
Output:
### Explanation for `async function fetchData()`
An asynchronous function that fetches data from an API endpoint.
...
```

### Code Refactoring Examples

Get suggestions and a cleaner version of your code:

#### Simple Sum Function
```bash
Input:  refactor "function add(a,b){return a+b}" --lang js
Output:
### Refactored Code for `add` function
```javascript
const add = (a, b) => a + b;
```
**Explanation:** Converted to a concise arrow function.
...
```

### Code Conversion Examples

Convert code seamlessly between JavaScript and TypeScript:

#### JS to TS
```bash
Input:  convert "function greet(name) { console.log('Hello, ' + name); }" --to ts
Output:
```typescript
function greet(name: string): void {
  console.log('Hello, ' + name);
}
```
```

#### TS to JS
```bash
Input:  convert "interface Point { x: number; y: number; }\nconst p: Point = { x: 10, y: 20 };" --to js
Output:
```javascript
const p = { x: 10, y: 20 };
```
```

### Code Debugging Examples

Identify and fix errors in your code, with or without error messages:

#### Function with Syntax Error
```bash
Input:  debug "function calculate(a, b) { return a ** b; }" --lang js
Output:
### Error: Missing operator
The code `a ** b` is a syntax error in some JavaScript environments. Corrected to `a * b` if multiplication was intended.
```

---

## 🛠️ Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | None | Optional |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-4o-mini` | Optional |
| `TEMPERATURE` | Creativity level for AI (0.0-1.0) | `0.7` | Optional |
| `MAX_TOKENS` | Maximum output tokens for AI response | `1500` | Optional |
| `DEFAULT_LANG` | Default output language for generation/refactoring | `ts` | Optional |
| `MINIMAL_MARKUP` | Generate minimal code/explanations by default | `false` | Optional |

### Command Line Options

```bash
python agent.py [OPTIONS]

Options:
  --menu, -m              Show main menu (default)
  --interactive, -i       Run in interactive mode (coming soon)
  --generate <description> Generate code from natural language
  --explain <code_snippet> Explain code snippet
  --refactor <code_snippet> Refactor code snippet
  --convert <code_snippet> Convert code snippet
  --to <js|ts>            Target language for conversion
  --debug <code_snippet>  Debug code snippet
  --error <message>       Optional error message for debugging
  --lang <js|ts>          Specify output language (js or ts)
  --save <filename>       Save output to a .js or .ts file
  --minimal               Generate minimal code/markup
  --help                  Show help message
```

---

## 🔧 API Reference

### Command Line Interface

| Command | Description | Example |
|---------|-------------|---------|
| `python agent.py` | Start main menu | Default startup |
| `python agent.py --menu` | Show main menu | Interactive menu mode |
| `python agent.py --generate "description"` | Generate code | `python agent.py --generate "a login form" --lang js` |
| `python agent.py --explain "<code>"` | Explain code | `python agent.py --explain "<span>" --lang html` |
| `python agent.py --refactor "<code>"` | Refactor code | `python agent.py --refactor "function() {return 1;}"` |
| `python agent.py --convert "<code>" --to <js|ts>` | Convert code | `python agent.py --convert "const x: number = 5;" --to js` |
| `python agent.py --debug "<code>"` | Debug code | `python agent.py --debug "let x=;"` |
| `python agent.py --save output.ts` | Save output | `python agent.py --generate "simple page" --save index.ts` |
| `python agent.py --lang js` | Specify language | `python agent.py --generate "button" --lang js` |
| `python agent.py --minimal` | Minimal markup | `python agent.py --generate "button" --minimal` |
| `python agent.py --interactive` | Quick actions (coming soon) | `python agent.py -i` |

### Internal API (to be implemented)

#### TSGenerator
```python
generator = TSGenerator(openai_client)
ts_code = generator.generate_code("a responsive hero section", language="ts")
```

#### TSExplainer
```python
explainer = TSExplainer(openai_client)
explanation = explainer.explain_code("const x = 5;", language="js")
```

#### TSRefactorer
```python
refactorer = TSRefactorer(openai_client)
refactored_code = refactorer.refactor_code("function add(a,b){return a+b}", language="js")
```

#### TSConverter
```python
converter = TSConverter(openai_client)
converted_code = converter.convert_code("const x: number = 5;", target_language="js")
```

#### TSDebugger
```python
debugger = TSDebugger(openai_client)
debug_output = debugger.debug_code("function sum(a,b) { return a + c; }", error_message="ReferenceError: c is not defined", language="js")
```

---

## 📁 Project Structure

```
49_LangChainStarter/TSHelperBot/
├── 📄 agent.py                   # Main CLI entry point
├── ⚙️ config/
│   └── 📄 openai_config.py       # OpenAI API configuration
├── 🧠 core/
│   ├── 📄 ts_generator.py        # JS/TS generation logic
│   ├── 📄 ts_explainer.py        # JS/TS explanation logic
│   ├── 📄 ts_refactorer.py       # JS/TS refactoring logic
│   ├── 📄 ts_converter.py        # JS/TS conversion logic
│   └── 📄 ts_debugger.py         # JS/TS debugging logic
├── 🛠️ utils/
│   └── 📄 cli_interface.py       # Rich terminal interface
├── 📋 requirements.txt           # Python dependencies
├── 🔧 env.example               # Environment variables template
├── 🚀 install.bat               # Windows installation script
├── ▶️ start.bat                 # Windows startup script
└── 📖 README.md                 # This documentation
```

### Key Files (to be implemented)

- **`agent.py`**: Main entry point with CLI argument parsing and menu system
- **`config/openai_config.py`**: OpenAI GPT integration and configuration
- **`core/ts_generator.py`**: Logic for generating JS/TS from natural language
- **`core/ts_explainer.py`**: Logic for explaining JS/TS code
- **`core/ts_refactorer.py`**: Logic for refactoring and optimizing JS/TS code
- **`core/ts_converter.py`**: Logic for converting JS ↔ TS code
- **`core/ts_debugger.py`**: Logic for debugging JS/TS code
- **`utils/cli_interface.py`**: Rich terminal UI with tables and panels

---

## 🎨 UI Features

### Visual Design
- **Rich Terminal Output**: Beautiful tables, panels, and colored text
- **Interactive Menus**: Numbered lists with easy selection
- **Progress Indicators**: Loading states and status updates
- **Error Handling**: Clear, user-friendly error messages
- **Success Feedback**: Confirmation messages and completion indicators

### Interactive Elements
- **Suggestion Menus**: (To be implemented for JS/TS snippets or attributes)
- **Confirmation Dialogs**: (To be implemented for saving files)
- **History Navigation**: (To be implemented for generated/explained items)

### Responsive Design
- **Terminal Compatibility**: Works with all modern terminal emulators
- **Screen Size Adaptation**: Adjusts to different terminal sizes
- **Color Support**: Full color support with fallbacks for basic terminals
- **Unicode Support**: Emoji and special characters throughout

---

## 🔒 Safety Features

### Input Validation (to be implemented)
- **Code Sanitization**: Ensure generated code is safe and doesn't contain malicious scripts (future consideration).
- **Confirmation System**: Saving files will require explicit user confirmation.

### Safety Measures
- **Timeout Protection**: API calls will be limited to prevent hanging.
- **Validation Checks**: (To be implemented for output code)
- **Error Recovery**: Graceful handling of API failures.
- **User Control**: Full control over output and file saving.

---

## 🐛 Troubleshooting

### Common Issues

#### 1. "OpenAI API key not found"
**Solution:**
```bash
# Check if API key is set
echo $OPENAI_API_KEY

# Set API key (Linux/Mac)
export OPENAI_API_KEY=your_api_key_here

# Set API key (Windows)
set OPENAI_API_KEY=your_api_key_here
```

#### 2. "Module not found errors"
**Solution:**
```bash
# Install dependencies
pip install -r requirements.txt

# Or install individually
pip install openai rich python-dotenv pyperclip
```

#### 3. "Rich library display issues"
**Solution:**
```bash
# Update Rich library
pip install --upgrade rich

# Check terminal compatibility
python -c "from rich.console import Console; Console().print('Test')"
```

### Debug Mode (to be implemented)

Enable debug logging by setting environment variable:
```bash
export DEBUG=1
python agent.py --menu
```

### Installation Verification

Run the main script directly or use the demo (if created):
```bash
python agent.py --help
```

### Getting Help

1. **Check the terminal output** for detailed error messages
2. **Verify your OpenAI API key** is working with a simple test
3. **Review the logs** for specific error details

---

## 🤝 Contributing

This project is part of the **#100DaysOfAI-Agents** challenge. We welcome contributions!

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and add tests
4. **Commit your changes**: `git commit -m 'Add amazing feature'`
5. **Push to the branch**: `git push origin feature/amazing-feature`
6. **Open a Pull Request**

### Areas for Contribution

- **🐛 Bug Fixes**: Report and fix bugs
- **✨ New Features**: Add new JS/TS generation/explanation/refactoring/conversion/debugging features
- **📚 Documentation**: Improve README, add examples
- **🎨 UI/UX**: Enhance the terminal interface
- **🧪 Testing**: Add more test coverage
- **🔧 Configuration**: Improve configuration options

### Development Setup

```bash
# Clone the repository
git clone <repository-url>
cd 49_LangChainStarter/TSHelperBot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run main script
python agent.py --help
```

### Code Style

- Follow **PEP 8** Python style guidelines
- Use **type hints** for function parameters
- Add **docstrings** for all functions
- Write **comprehensive tests**
- Keep **commit messages** clear and descriptive

---

## 📄 License

This project is part of the **#100DaysOfAI-Agents** challenge by [Muhammad Sami Asghar Mughal](https://github.com/your-username).

### License Terms

- **Open Source**: This project is open source and available under the MIT License
- **Educational Use**: Free to use for educational and personal purposes
- **Commercial Use**: Contact the author for commercial licensing
- **Attribution**: Please credit the original author when using this code

---

## 🙏 Acknowledgments

### Open Source Libraries
- **[OpenAI](https://openai.com/)** - GPT API for intelligent explanations
- **[Rich](https://rich.readthedocs.io/)** - Beautiful terminal output and UI
- **[Python](https://python.org/)** - The programming language that makes it all possible

### Community
- **AI Community** - For inspiration and support
- **Open Source Contributors** - For the amazing tools that make this possible
- **Beta Testers** - For valuable feedback and bug reports

### Special Thanks
- **OpenAI Team** - For making powerful AI accessible
- **Rich Library Community** - For the excellent terminal UI framework
- **#100DaysOfAI-Agents** - For the motivation to build amazing AI tools

---

<div align="center">

**Happy Coding with JS/TS! 🚀**

[⬆️ Back to Top](#-tshelperbot---day-49-of-100daysofai-agents)

*Transform your JavaScript/TypeScript workflow with AI-powered intelligence and beautiful terminal interfaces!*
