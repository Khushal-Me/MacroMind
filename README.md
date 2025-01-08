# MacroMind: AI-Powered Nutrition Assistant 🧠

MacroMind is an intelligent nutrition tracking system powered by Google's Gemini Pro Language Model. It provides real-time nutritional analysis, tracks daily macro goals, and offers AI-powered nutrition consultation.

## 🌟 Key Features

#### 🍎 Intelligent Food Tracking and Analysis

<img width="367" alt="Screenshot 2025-01-07 at 7 18 46 PM" src="https://github.com/user-attachments/assets/b483e148-1a65-40ce-962a-c2a44edd189a" />

- Real-time AI-powered nutritional breakdown
- Automatic calorie calculation
- Protein content analysis
- Running daily totals

#### 📊 Smart Goal Tracking

<img width="440" alt="Screenshot 2025-01-07 at 7 19 20 PM" src="https://github.com/user-attachments/assets/c221f900-a71f-40f9-8a3e-9ccddc7b7df5" />

- Dynamic calculation of remaining daily allowances
- Personalized macro tracking
- Real-time goal updates

#### 📝 Comprehensive Food History

<img width="440" alt="Screenshot 2025-01-07 at 7 20 44 PM" src="https://github.com/user-attachments/assets/fb0b2b52-5ace-4f69-b685-452812da7231" />

- Detailed food logging
- Timestamp tracking
- Nutritional breakdown history

#### 🧮 Data Management

<img width="440" alt="Screenshot 2025-01-07 at 7 21 04 PM" src="https://github.com/user-attachments/assets/6d579d17-12a5-4c82-b42a-9fc6a416262a" />

- Easy data reset
- Flexible history management
- Data persistence

#### 🤖 AI Nutrition Consultant

<img width="590" alt="Screenshot 2025-01-07 at 7 22 20 PM" src="https://github.com/user-attachments/assets/95712e99-5876-4d08-9c7b-69d921584e95" />

- Expert nutritional guidance
- Context-aware responses
- Personalized dietary advice

## 🚀 Technology Stack

- **AI/ML Integration**
  - Google Gemini Pro API for natural language processing
  - Advanced prompt engineering
  - Contextual response generation

- **Backend Architecture**
  - Python-based system
  - Flask server for Replit hosting
  - Environment variable management
  - Threaded server implementation

## 💻 Installation

### 1. Clone the repository
```bash
git clone https://github.com/Khushal-Me/MacroMind.git
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Obtain API Keys

#### Google Gemini API Key

1. Visit Google AI Studio
2. Sign in with your Google account
3. Click "Create API Key" or "Get API Key"
4. Copy your generated API key

#### Discord Bot Token

1. Go to Discord Developer Portal
2. Click "New Application"
3. Name your application "MacroMind"
4. Navigate to the "Bot" section in the left sidebar
5. Click "Reset Token" to reveal your bot token
6. Important: Enable "Message Content Intent" under Privileged Gateway Intents

### 4. Configure environment variables in `.env`:
```env
GEMINI_API_KEY=your_gemini_api_key
DISCORD_BOT_TOKEN=your_bot_token
```

## 🤖 Commands

- `!add [food]` - Add food items with AI nutritional analysis
- `!left` - Check remaining daily allowances
- `!history` - View food log
- `!clear` - Reset all data
- `!q [question]` - Ask nutrition questions

## 🔍 Technical Implementation

### AI Features
- Natural language food analysis
- Nutritional content extraction
- Smart response generation
- Error handling and validation

### Data Management
- User-specific tracking
- Daily reset functionality
- Persistent storage
- History management

### Server Architecture
- Flask-based web server
- Threading for optimal performance
- Continuous operation
- Error recovery systems

## 📌 Deployment

Optimized for Replit deployment with:
- Flask server implementation
- Automatic error handling
- Environment variable management
- 24/7 uptime configuration using uptimerobot.com

## 🤝 Contributing

Contributions are welcome! Feel free to submit Pull Requests.

## 📝 License

This project is licensed under the MIT License.

---

*Note: MacroMind is an AI-first application focusing on intelligent nutritional analysis and expert guidance.*
