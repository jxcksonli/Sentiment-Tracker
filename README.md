# Sentiment Tracker

Sentiment Tracker pulls together public reactions from places like Reddit, then turns that chatter into readable sentiment ratings and graphs so you can visualise how opinions shift over time.

Type any topic and the page will summarise the overall mood and visualise the trend.

## Run locally

Run:
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
UI:
```bash
cd frontend
npm install
npm run dev
```