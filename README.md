# Sentiment Tracker

Search any topic and explore a word bubble cloud built from Hacker News comments. Bubble size shows how often a word appears. Bubble colour shows sentiment (green positive, red negative, grey neutral).

## Run locally

Backend:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

## Deploy frontend on GitHub Pages

If you only see this README on your site, GitHub Pages is publishing the repo root instead of the built app.

1. Push this repo to GitHub.
2. Go to **Settings → Pages → Build and deployment**.
3. Set **Source** to **GitHub Actions** (not “Deploy from branch”).
4. Push to `main` (or run the **Deploy frontend to GitHub Pages** workflow manually).

Your app will be at:

`https://<your-username>.github.io/<repo-name>/`

Search needs a running backend. Host the API separately (for example Railway) and set `VITE_API_URL` in the GitHub Actions build step to your API URL if you want live results on Pages.
