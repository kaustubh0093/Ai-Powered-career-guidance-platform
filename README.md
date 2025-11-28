# 🎯 AI-Powered Career Guidance Platform

An intelligent career guidance application powered by Google Gemini AI, LangChain, and SerpAPI. This platform provides personalized career insights, market analysis, college recommendations, and resume coaching specifically tailored for the Indian job market.

## ✨ Features

### 🧭 Career Insights & Learning Roadmap
- Comprehensive career analysis for various roles across multiple industries
- Detailed learning roadmaps from beginner to advanced levels
- Career progression paths with salary bands (in INR)
- Required skills, tools, and certifications
- Future outlook and industry trends

### 📊 Live Market Analysis
- Real-time job market trends in India
- Current salary ranges (entry/mid/senior levels in INR)
- Top hiring companies and industry sectors
- Major hiring cities (Bangalore, Mumbai, Delhi, Hyderabad, Pune, etc.)
- In-demand skills and remote work availability
- Web-powered live data search

### 🎓 College & University Recommendations
- Personalized recommendations for Indian colleges and universities
- IITs, NITs, IIITs, and other premier institutes
- Degree programs, specializations, and eligibility criteria
- Entrance exam information (JEE, GATE, CAT, etc.)
- Scholarships and financial aid options
- Alternative education paths (online courses, bootcamps, certifications)

### 📝 Resume Coach & Feedback
- AI-powered resume analysis and scoring
- ATS (Applicant Tracking System) optimization tips
- Section-by-section detailed feedback
- Content, format, and structure analysis
- Before/After improvement examples
- Industry-specific tips for Indian job market
- Support for multiple file formats (PDF, DOCX, TXT)

### 💬 Interactive AI Career Assistant
- Context-aware conversational AI
- Ask questions about careers, skills, colleges, and job market
- Personalized guidance and recommendations
- Access to live web data for current information

## 🏢 Career Categories Covered

### 💻 Technology
- AI & Machine Learning Engineer
- Data Scientist
- Cybersecurity Analyst
- Cloud Solutions Architect
- Full Stack Developer
- DevOps Engineer
- Blockchain Developer
- Mobile App Developer
- Data Engineer
- Software Quality Assurance Engineer

### 🩺 Healthcare
- Medical Data Analyst
- Telehealth Specialist
- Biomedical Engineer
- Clinical Research Associate
- Healthcare Administrator
- Public Health Specialist
- Medical Laboratory Technologist
- Physiotherapist
- Pharmacy Manager
- Healthcare IT Consultant

### 💼 Business
- Business Analyst
- Digital Marketing Strategist
- Financial Data Analyst
- Product Manager
- HR Analytics Specialist
- Management Consultant
- Supply Chain Analyst
- Investment Banker
- Brand Manager
- Operations Manager

### 🎥 Content Creation
- Video Content Strategist
- Social Media Manager
- Copywriter / Content Writer
- Graphic Designer
- SEO Specialist
- Podcast Producer
- UX/UI Designer
- Video Editor
- Influencer Marketing Manager
- Content Marketing Strategist

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Google Gemini API Key
- SerpAPI Key

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-career-guide
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:

Create a `.env` file in the root directory and add your API keys:
```env
GEMINI_API_KEY=your_google_gemini_api_key_here
SERPAPI_API_KEY=your_serpapi_key_here
```

**Note:** Never commit your `.env` file to version control. It's included in `.gitignore` for security.

### Getting API Keys

#### Google Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key to your `.env` file

#### SerpAPI Key
1. Visit [SerpAPI](https://serpapi.com/)
2. Sign up for a free account
3. Navigate to your dashboard
4. Copy your API key to your `.env` file

### Running the Application

Start the Streamlit application:
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## 📖 Usage Guide

1. **Configure API Keys**: Enter your Google Gemini and SerpAPI keys in the sidebar (or set them in the `.env` file)

2. **Select Career Interest**: Choose a career category and specific role from the dropdown menus

3. **Explore Features Using Tabs**:
   - **🧭 Career Insights**: Generate comprehensive career analysis and learning roadmap
   - **📊 Market Analysis**: Fetch live job market data and trends
   - **🎓 College Advisor**: Get personalized college and university recommendations
   - **📝 Resume Coach**: Upload or paste your resume for AI-powered feedback

4. **Use the Chat Assistant**: Ask any career-related questions in the chat interface at the bottom

5. **Clear Session**: Use the "Clear Session" button in the sidebar to reset all cached data

## 🛠️ Technology Stack

- **Frontend/UI**: [Streamlit](https://streamlit.io/) - Interactive web application framework
- **AI Model**: [Google Gemini](https://deepmind.google/technologies/gemini/) (gemini-2.5-flash) - Advanced language model
- **AI Framework**: [LangChain](https://www.langchain.com/) - AI application development framework
- **Web Search**: [SerpAPI](https://serpapi.com/) - Real-time web search API
- **Environment Management**: [python-dotenv](https://pypi.org/project/python-dotenv/) - Environment variable management
- **Document Processing**: PyPDF2 (optional), python-docx (optional) - Resume file parsing

## 📦 Dependencies

Core dependencies (see [requirements.txt](requirements.txt) for complete list):
- streamlit >= 1.35.0
- langchain >= 0.2.0, < 0.3.0
- langchain-google-genai >= 1.0.0, < 2.0.0
- langchain-community >= 0.2.0, < 0.3.0
- google-generativeai >= 0.7.0, < 0.8.0
- python-dotenv >= 1.0.0
- google-search-results >= 2.4.2

Optional (for resume file upload):
```bash
pip install PyPDF2 python-docx
```

## 🇮🇳 Indian Market Focus

This platform is specifically designed for the Indian context:
- Salary ranges in INR (Indian Rupees)
- Indian colleges, universities, and institutions
- Indian entrance exams (JEE, GATE, CAT, etc.)
- Major hiring cities in India
- Indian job market trends and data
- Cultural considerations for Indian recruiters

## 🔒 Security & Privacy

- API keys are stored securely in environment variables or Streamlit secrets
- Never commit `.env` files to version control
- The `.env` file is included in `.gitignore` by default
- No user data is permanently stored or transmitted beyond API calls

## 🤝 Contributing

Contributions are welcome! Here are some ways you can contribute:
- Report bugs and issues
- Suggest new features or career categories
- Improve documentation
- Submit pull requests

## 📝 License

This project is open source and available for educational and personal use.

## 🙏 Acknowledgments

- Powered by [Google Gemini AI](https://deepmind.google/technologies/gemini/)
- Built with [LangChain](https://www.langchain.com/)
- Web search powered by [SerpAPI](https://serpapi.com/)
- UI framework by [Streamlit](https://streamlit.io/)

## 📧 Support

For issues, questions, or suggestions:
- Open an issue in the repository
- Check existing documentation
- Review the FAQ section below

## ❓ FAQ

### Q: What API keys do I need?
A: You need two API keys:
1. Google Gemini API Key (for AI capabilities)
2. SerpAPI Key (for live web search)

### Q: Is this application free to use?
A: The application itself is free. However, the API services (Gemini and SerpAPI) have their own pricing models. Both offer free tiers that should be sufficient for personal use.

### Q: Can I use this for careers outside India?
A: While the platform is optimized for the Indian market, you can modify the prompts in the code to focus on other regions.

### Q: What file formats are supported for resume upload?
A: PDF, DOCX, DOC, and TXT files are supported. For PDF and DOCX support, install the optional dependencies.

### Q: How do I deploy this application?
A: You can deploy to Streamlit Community Cloud, Heroku, AWS, or any platform that supports Python web applications. Make sure to configure your API keys as secrets in your deployment environment.

## 🗺️ Roadmap

Future enhancements planned:
- [ ] Support for more file formats in resume upload
- [ ] Interview preparation module
- [ ] Skill assessment tools
- [ ] Personalized learning path tracking
- [ ] Job application tracker
- [ ] Networking and mentorship recommendations
- [ ] Salary negotiation assistant
- [ ] Multi-language support

---

**Built with ❤️ for career seekers in India**

*Last Updated: October 2024*
