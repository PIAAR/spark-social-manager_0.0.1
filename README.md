# Social Media Manager

## 📌 Overview
The **Social Media Manager** is a command-line tool designed to streamline content creation, management, analytics, and automation for multiple social media platforms. This modular program provides an intuitive menu system, API integrations, and automation features for scheduling, engagement tracking, and content posting.

## 🚀 Features
### ✅ Content Management
- Create, edit, delete, and schedule social media posts.
- Draft management and scheduled post tracking.

### ✅ Platform Management
- Connect and disconnect social media accounts.
- Store and manage API credentials securely in JSON format.

### ✅ Engagement & Analytics
- Track post performance, engagement metrics, and follower growth.
- Monitor mentions, hashtags, and competitors.

### ✅ Automation & Scheduling
- AI-assisted hashtag and caption suggestions.
- Rule-based automation for posting.
- Batch content uploading and multi-platform posting.

### ✅ Logging & Debugging
- Tracks program steps, errors, and debugging logs in a structured JSON log file.

## 📂 Directory Structure
```
/social_media_manager
│── /scripts            # Python scripts for each functionality
│   ├── main.py         # Main entry point
│   ├── menu.py         # Menu system
│   ├── content.py      # Handles post creation, editing, and scheduling
│   ├── platform.py     # Manages platform connections & credentials
│   ├── analytics.py    # Handles engagement & performance analytics
│   ├── automation.py   # Automates tasks like hashtag & AI caption generation
│   ├── logging.py      # Logs system activities & errors
│── /data               # Stores credentials & logs
│   ├── credentials.json  # Stores API keys & tokens for platforms
│   ├── logs.json       # Stores program logs
│── /config             # Configurations
│   ├── settings.json   # Stores user preferences
│── /utils              # Utility functions
│   ├── fetch_transcripts.py  # Functions to fetch video transcripts
│── requirements.txt    # Required dependencies
│── README.md           # Documentation
```

## 🔧 Installation & Setup
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/YOUR_USERNAME/social-media-manager.git
cd social-media-manager
```

### **2️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3️⃣ Set Up API Credentials**
- Add your social media API credentials to `data/credentials.json`
```json
{
  "twitter": {
    "api_key": "your_api_key",
    "api_secret": "your_api_secret"
  },
  "facebook": {
    "app_id": "your_app_id",
    "app_secret": "your_app_secret"
  }
}
```

### **4️⃣ Run the Program**
```bash
python main.py
```

## 🛠 Future Enhancements
- OAuth authentication for social platforms.
- AI-powered content creation suggestions.
- Integration with cloud storage for backup.
- Web-based UI for enhanced usability.

## 🤝 Contributing
Feel free to contribute to this project! Fork the repository and submit a pull request with your changes.

## 📜 License
This project is licensed under the MIT License.

---
💡 **Developed by [Rahm PIAAR Shinobi]**

