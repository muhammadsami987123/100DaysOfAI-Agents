# 📧 EmailCleanerAgent - Day 88 of #100DaysOfAI-Agents

<div align="center">

![EmailCleanerAgent Banner](https://img.shields.io/badge/EmailCleanerAgent-Day%2088-blue?style=for-the-badge&logo=gmail&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini%202.0-Flash-orange?style=for-the-badge&logo=google-gemini&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Web%20Framework-red?style=for-the-badge&logo=fastapi&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-Styling-blueviolet?style=for-the-badge&logo=tailwindcss&logoColor=white)

**A smart productivity tool that automatically cleans your inbox by identifying and managing spam, promotions, and low-priority emails using AI.**

[🚀 Quick Start](#-quick-start) • [🎯 Features](#-features) • [⚙️ How It Works](#️-how-it-works) • [🔧 Setup Guide](#-setup-guide-creating-and-using-client_secretjson) • [🤝 Contributing](#-contributing)

</div>

---

## ✨ What is EmailCleanerAgent?

**EmailCleanerAgent** is an intelligent AI-powered assistant designed to help you reclaim your inbox. It securely connects to your Gmail account, fetches your latest emails, and uses advanced Large Language Models (like Google's Gemini) to classify each email as important, promotional, or spam. You can then review the classifications and perform bulk actions like deleting spam and archiving promotional content, making inbox management fast, simple, and efficient.

### 🌟 Key Highlights

- **🤖 AI-Powered Classification**: Leverages the natural language understanding of Google Gemini to analyze and accurately categorize emails.
- **🔒 Secure & Private**: Uses Google's official and secure OAuth 2.0 protocol, ensuring your credentials are never exposed.
- **✅ Bulk Actions**: Clean your inbox in seconds by deleting all identified spam and archiving promotions with user confirmation.
- **🚀 Modern Web UI**: A clean, responsive, and intuitive interface built with FastAPI and styled with TailwindCSS.
- **⚙️ Flexible LLM Support**: Designed to be adaptable, allowing for easy integration with different LLMs like OpenAI's GPT series.
- **🛡️ User in Control**: The agent suggests actions, but the final decision to delete or archive always rests with the user.

---

## 🎯 Features

### 🚀 Core Functionality
- ✅ **Secure Gmail Authentication**: Integrates with the Gmail API using OAuth 2.0, the industry standard for secure access.
- ✅ **Inbox Fetching**: Retrieves the most recent 50-100 emails from the user's primary inbox for analysis.
- ✅ **AI-Driven Email Analysis**:
  - **Spam Scoring**: Identifies patterns, keywords, and sender reputations indicative of spam.
  - **Promotion Detection**: Recognizes newsletters, marketing campaigns, and promotional offers.
  - **Priority Identification**: Distinguishes important, personal, and transactional emails from general clutter.
- ✅ **Intelligent Email Classification**:
  - **✅ Safe/Important**: Personal conversations, receipts, and critical alerts that need your attention.
  - **🗑️ Spam**: Unsolicited junk mail that can be safely deleted.
  - **📦 Promotional**: Newsletters, sales alerts, and marketing content suitable for archiving.
- ✅ **User-Controlled Actions**:
  - **Delete**: Permanently removes selected emails from the inbox and moves them to Trash.
  - **Archive**: Cleans the inbox by removing emails from view without permanently deleting them.
  - **Keep**: Allows users to leave important emails untouched.

### 💻 User Interface & Experience
- ✅ **Simple Authentication Flow**: A straightforward process to connect a Google account with a single click.
- ✅ **One-Click Scan Button**: Initiates the entire fetching and analysis process.
- ✅ **Dynamic Results Panel**: Displays a clear, card-based list of analyzed emails.
- ✅ **Color-Coded Classification**: Each email is tagged with a colored label (e.g., green for Important, yellow for Promotional, red for Spam) for quick visual identification.
- ✅ **Individual Action Buttons**: Each email card has its own `Delete` and `Archive` buttons for granular control.
- ✅ **Fully Responsive Design**: The interface is optimized for a seamless experience on desktops, tablets, and mobile devices.

### 🛡️ Security & Authentication
- ✅ **OAuth 2.0 Protocol**: Ensures that the application never sees or stores the user's Google password.
- ✅ **Scoped Permissions**: The agent only requests the `gmail.modify` scope, which is necessary to read, move, and delete emails, without overreaching.
- ✅ **Backend Credential Storage**: The critical `client_secret.json` is stored securely on the backend, never exposed to the user's browser.
- ✅ **Token-Based Sessions**: After initial authentication, the app uses refreshable tokens stored in `gmail_credentials.json` for subsequent access, enhancing security.

### ⚙️ Extensibility & Configuration
- ✅ **Environment-Based Configuration**: API keys and other settings are managed via a `.env` file for easy setup and security.
- ✅ **Modular LLM Service**: The `llm_service.py` is designed to be easily extended to support other language models.
- ✅ **Customizable Prompts**: The prompt used for AI classification is stored in `prompts/email_analyzer_prompt.txt`, allowing for easy tuning and experimentation.

---

## ⚙️ How It Works

1.  **Authentication**: The user clicks a button to connect their Gmail account. They are redirected to Google's secure OAuth 2.0 consent screen.
2.  **Permission Grant**: The user grants the `EmailCleanerAgent` permission to manage their email. Google provides an authorization token back to the application.
3.  **Fetch Emails**: The agent uses the Gmail API to fetch the headers and snippets of the most recent emails in the user's inbox.
4.  **AI Analysis**: For each email, the agent sends the subject and snippet to the selected LLM (e.g., Gemini) with a prompt asking it to classify the email.
5.  **Display Results**: The web interface is updated with the list of emails, each tagged with its AI-generated category (Important, Promotional, or Spam).
6.  **User Action**: The user reviews the suggestions and can click `Delete` or `Archive` on individual emails to clean their inbox.
7.  **Execute Actions**: The agent sends the appropriate commands back to the Gmail API to perform the requested actions.

---

## 🚀 Quick Start

### 📋 Prerequisites

- **Python 3.8+** installed on your system.
- **Google Account** (for accessing the Gmail API).
- A **Google Cloud Project** with the Gmail API enabled.
- **API Keys** for Google Gemini and (optionally) OpenAI.

### ⚡ Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd 88_EmailCleanerAgent
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up your environment variables:**
    - Create a `.env` file by copying the example or creating a new one.
    - Add your API keys:
      ```
      GOOGLE_API_KEY="your_google_gemini_api_key"
      OPENAI_API_KEY="your_openai_api_key"
      ```

4.  **Generate your `client_secret.json` file** by following the detailed guide below.

5.  **Run the application:**
    ```bash
    python main.py
    ```

6.  **Open your browser** and navigate to `http://122.0.0.1:8000`.

---

## 🔧 Setup Guide: Creating and Using `client_secret.json`

The `client_secret.json` file is the key to securely connecting your application to the Gmail API. It contains your application's private credentials and must be handled carefully.

### Why is `client_secret.json` Important and Kept on the Backend?

- **Application Identity**: This file is how Google recognizes your specific application. It contains a client ID and a client secret, which are like a username and password for your app itself.
- **Security Risk**: If this file were on the frontend (in the user's browser), its contents would be publicly visible. Malicious actors could steal your app's credentials and use them to trick users or abuse Google's APIs, potentially getting your application banned.
- **Critical for Authorization**: The client secret is used in the final step of the OAuth 2.0 flow to exchange a temporary authorization code for a permanent access token. This exchange must happen on a secure server to protect the integrity of the process.

### Step-by-Step Guide to Create `client_secret.json`

1.  **Go to the Google Cloud Console**:
    - Open [console.cloud.google.com](https://console.cloud.google.com/) and log in.

2.  **Create a New Project**:
    - Click the project dropdown in the top-left and select **"New Project"**.
    - Name it `EmailCleanerAgent` and click **"Create"**.

3.  **Enable the Gmail API**:
    - In the new project, navigate to **"APIs & Services" > "Library"**.
    - Search for "Gmail API", select it, and click the **"Enable"** button.

4.  **Configure the OAuth Consent Screen**:
    - Go to **"APIs & Services" > "OAuth consent screen"**.
    - Choose **"External"** for the User Type and click **"Create"**.
    - Fill in the required application details:
      - **App name**: `EmailCleanerAgent`
      - **User support email**: Your email address.
      - **Developer contact information**: Your email address.
    - Click **"Save and Continue"** through the "Scopes" section.
    - **Add Test Users**: On the "Test users" page, click **"+ Add Users"** and add the Gmail account you will be using to test the application. **This is a critical step to avoid the "Access blocked" error during development.**

5.  **Create OAuth 2.0 Credentials**:
    - Go to **"APIs & Services" > "Credentials"**.
    - Click **"+ Create Credentials"** at the top and select **"OAuth client ID"**.
    - For the **"Application type,"** choose **"Desktop app"**. This is the simplest type for local development.
    - Give it a name (e.g., "EmailCleanerAgent Desktop Client") and click **"Create"**.

6.  **Download the Credentials File**:
    - A pop-up will appear showing your Client ID and Client Secret.
    - Click the **"DOWNLOAD JSON"** button.
    - Rename the downloaded file to exactly `client_secret.json`.

7.  **Place the File in Your Project**:
    - Move the `client_secret.json` file into the root directory of the `88_EmailCleanerAgent` project, alongside `main.py`.

Your application is now fully configured to securely authenticate with the Gmail API.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/muhammadsami987123/100DaysOfAI-Agents/issues).

---

## About the #100DaysOfAI-Agents Challenge

This project is part of my **#100DaysOfAI-Agents challenge**, a personal commitment to building 100 distinct AI agents in 100 days. Each agent is designed to tackle a unique real-world problem, showcasing the diverse applications of AI in daily tasks.

The goal is to create a portfolio of functional, open-source AI tools while exploring the capabilities of technologies like OpenAI, Google Gemini, FastAPI, and various automation libraries.

### Follow My Journey

**Muhammad Sami Asghar Mughal**  
Student | AI Agent Developer | Passionate About Web3, Generative AI & Automation  
📍 Karachi, Pakistan

- 💼 [LinkedIn](https://linkedin.com/in/muhammad-sami-3aa6102b8)  
- 💻 [GitHub](https://github.com/muhammadsami987123)  
- 🌐 [Portfolio](https://muhammad-sami.vercel.app/)  
- 📧 Email: m.smiwaseem1234@gmail.com
