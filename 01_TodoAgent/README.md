# 🤖 TodoAgent - Day 1 of #100DaysOfAI-Agents

A smart todo management agent that understands natural language commands and manages tasks with priority levels, due dates, categories, and status tracking.

## 🚀 Features

- **Natural Language Processing**: Use OpenAI GPT to understand commands like "add buy groceries" or "mark task 1 as completed"
- **Full CRUD Operations**: Create, Read, Update, Delete todos
- **Priority Levels**: High, Medium, Low priority management
- **Categories**: Organize todos by work, personal, shopping, health, learning, or other
- **Due Dates**: Set and track deadlines with overdue warnings
- **Status Tracking**: Pending, In Progress, Completed statuses
- **Persistent Storage**: Todos saved to JSON file
- **Colorful CLI**: Beautiful colored interface with emojis
- **Search Functionality**: Find todos by keywords
- **Statistics**: Track completion rates and progress

## 📋 Requirements

- Python 3.7+
- OpenAI API key
- Internet connection (for GPT API calls)

## 🛠️ Installation

### Quick Setup (Recommended)

1. **Clone or navigate to the TodoAgent directory:**
   ```bash
   cd 01_TodoAgent
   ```

2. **Run the setup script:**
   ```bash
   python setup.py
   ```
   
   This will:
   - Install all dependencies
   - Create a `.env` file in your home directory
   - Prompt you for your OpenAI API key
   - Test the setup

### Manual Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up your OpenAI API key:**
   
   **Option 1: .env file in home directory (Recommended)**
   ```bash
   # Create .env file in your home directory
   echo "OPENAI_API_KEY=your_api_key_here" > ~/.env
   ```
   
   **Option 2: Environment Variable**
   ```bash
   # Windows
   set OPENAI_API_KEY=your_api_key_here
   
   # macOS/Linux
   export OPENAI_API_KEY=your_api_key_here
   ```
   
   **Option 3: Command Line Argument**
   ```bash
   python main.py your_api_key_here
   ```

## 🎯 Usage

### Starting the Agent

```bash
python main.py
```

### Natural Language Commands

The TodoAgent understands natural language! Here are some examples:

#### Adding Todos
```bash
📝 TodoAgent> add buy groceries
📝 TodoAgent> add urgent meeting with client tomorrow
📝 TodoAgent> add workout session high priority health category
📝 TodoAgent> add study Python programming due 2024-01-20
```

#### Managing Todos
```bash
📝 TodoAgent> mark task 1 as completed
📝 TodoAgent> mark task 2 as in progress
📝 TodoAgent> delete task 3
📝 TodoAgent> update task 2 priority high due_date 2024-01-20
```

#### Searching and Listing
```bash
📝 TodoAgent> search groceries
📝 TodoAgent> list
📝 TodoAgent> stats
```

### Direct Commands

- `list` - Show all todos
- `stats` - Show statistics
- `help` - Show help information
- `quit` - Exit the program

## 🎨 Features in Detail

### Priority Levels
- **High** (Red): Urgent tasks that need immediate attention
- **Medium** (Yellow): Important tasks with moderate urgency
- **Low** (Green): Tasks that can be done when convenient

### Categories
- **work** - Professional tasks and meetings
- **personal** - Personal errands and activities
- **shopping** - Shopping lists and purchases
- **health** - Exercise, medical appointments, wellness
- **learning** - Study sessions, courses, skill development
- **other** - Miscellaneous tasks

### Status Tracking
- **Pending** (⏳): Tasks not yet started
- **In Progress** (🔄): Tasks currently being worked on
- **Completed** (✅): Finished tasks

### Due Date Features
- **Overdue** (Red): Tasks past their due date
- **Today** (Yellow): Tasks due today
- **Future** (Green): Tasks with future due dates

## 📁 File Structure

```
01_TodoAgent/
├── main.py              # Main TodoAgent application
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── todos.json          # Todo data storage (created automatically)
└── .gitignore          # Git ignore file
```

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key (required)

### Data Storage
Todos are automatically saved to `todos.json` in the same directory. The file is created automatically when you add your first todo.

## 🎯 Example Session

```
🚀 Starting TodoAgent - Day 1 of #100DaysOfAI-Agents
Author: Muhammad Sami Asghar Mughal

🤖 Welcome to TodoAgent!
I can help you manage your todos using natural language.
Type 'help' for commands, 'quit' to exit.
--------------------------------------------------
📝 TodoAgent> add buy groceries tomorrow
🤖 Processing: add buy groceries tomorrow
✅ Added todo: buy groceries

[ 1] ⏳ buy groceries
     Priority: MEDIUM
     Category: other
     Status: Pending
     Due: 2024-01-16

📝 TodoAgent> add urgent meeting with client high priority work category
🤖 Processing: add urgent meeting with client high priority work category
✅ Added todo: meeting with client

[ 2] ⏳ meeting with client
     Priority: HIGH
     Category: work
     Status: Pending

📝 TodoAgent> list
📋 Your Todos (2 items):
--------------------------------------------------------------------------------

[ 1] ⏳ buy groceries
     Priority: MEDIUM
     Category: other
     Status: Pending
     Due: 2024-01-16

[ 2] ⏳ meeting with client
     Priority: HIGH
     Category: work
     Status: Pending

📝 TodoAgent> mark task 1 as completed
🤖 Processing: mark task 1 as completed
✅ Updated todo 1

[ 1] ✅ buy groceries
     Priority: MEDIUM
     Category: other
     Status: Completed
     Due: 2024-01-16

📝 TodoAgent> stats
📊 Todo Statistics:
Total todos: 2
Completed: 1
Pending: 1
In Progress: 0
Completion rate: 50.0%

📝 TodoAgent> quit
👋 Goodbye! Your todos are saved.
```

## 🐛 Troubleshooting

### Common Issues

1. **"OpenAI API key not found"**
   - Make sure you've set the `OPENAI_API_KEY` environment variable
   - Or pass it as a command line argument: `python main.py your_key_here`

2. **"Error parsing command"**
   - Check your internet connection
   - Verify your OpenAI API key is valid
   - Try rephrasing your command

3. **"Error loading todos"**
   - Check file permissions in the directory
   - The `todos.json` file will be created automatically

4. **"Wrong or invalid API key"**
   - **Check your API key format**: Should start with `sk-` and be about 51 characters long
   - **Verify API key**: Go to https://platform.openai.com/api-keys to check if it's valid
   - **Check API credits**: Ensure you have sufficient credits in your OpenAI account

### 🔧 How to Change Your API Key

If you entered the wrong API key during setup, here are ways to fix it:

#### **Option 1: Edit .env file (Recommended)**
```bash
# Windows - Open in Notepad
notepad C:\Users\YourUsername\.env

# macOS/Linux - Open in text editor
nano ~/.env
# or
code ~/.env
```
Then replace the old key with your correct API key and save.

#### **Option 2: Set environment variable (temporary)**
```bash
# Windows
set OPENAI_API_KEY=your_correct_api_key_here
python main.py

# macOS/Linux
export OPENAI_API_KEY=your_correct_api_key_here
python main.py
```

#### **Option 3: Use command line argument**
```bash
python main.py your_correct_api_key_here
```

#### **Option 4: Delete and recreate .env file**
```bash
# Windows
del C:\Users\YourUsername\.env
python setup.py

# macOS/Linux
rm ~/.env
python setup.py
```

### 🔑 Getting Your OpenAI API Key

1. **Go to OpenAI Platform**: https://platform.openai.com/api-keys
2. **Sign in** or create an account
3. **Click "Create new secret key"**
4. **Copy the key** (it starts with `sk-`)
5. **Keep it secure** - don't share it publicly

### Getting Help

- Type `help` in the TodoAgent interface for command examples
- Check the OpenAI API documentation for API-related issues
- Ensure you have sufficient OpenAI API credits
- **API Key Issues**: Check your OpenAI account billing and usage limits

## 🔮 Future Enhancements

Potential improvements for future versions:
- Voice input/output integration
- Calendar integration
- Email notifications for due dates
- Web interface
- Mobile app
- Team collaboration features
- Recurring tasks
- Subtasks and dependencies

## 📝 License

This project is part of the #100DaysOfAI-Agents challenge by Muhammad Sami Asghar Mughal.

## 🤝 Contributing

Feel free to contribute to this project by:
- Reporting bugs
- Suggesting new features
- Improving documentation
- Adding new capabilities

---

**Happy Todo Management! 🎉** 