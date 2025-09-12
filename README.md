# Books BR Releases API

- FastAPI app to list Brazilian book launches and pre-orders
- Filter by editora (publisher) and gênero (genre)
- Daily job (to be added) will refresh data

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open `http://localhost:8000` for UI and `http://localhost:8000/api/books` for API.