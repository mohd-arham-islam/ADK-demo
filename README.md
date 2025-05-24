# Financial Analyst Agent Setup

## 1. Clone the Repository

```bash
git clone https://github.com/mohd-arham-islam/ADK-demo.git
```

## 2. Set Up API Keys

Create a `.env` file inside the `multi_agent` folder with the following content:

```ini
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY="<YOUR_GOOGLE_API_KEY>"
ALPHA_VANTAGE_API_KEY="<YOUR_ALPHA_VANTAGE_KEY>"
```
Replace <YOUR_GOOGLE_API_KEY> and <YOUR_ALPHA_VANTAGE_KEY> with your actual API keys.

## 3. Run the Agent
Navigate to the parent folder (which contains your multi_agent sub folder) and run the following code:

```ini
adk web
```

Open the URL (usually http://localhost:8000) shown in the terminal in your browser to start chatting with your agent.

