# Window Garden

A small demo app for tracking when houseplants need water.

- **Frontend:** React (Vite)
- **Backend:** Python + FastAPI (in-memory data, resets on restart)

## Project structure

```
window-garden/
├── backend/    # FastAPI app
└── frontend/   # React app
```

## Run the backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

## Run the frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173. Vite proxies `/api` requests to the backend on port 8000.

## API

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/plants` | List plants |
| POST | `/api/plants` | Add a plant |
| POST | `/api/plants/{id}/water` | Mark a plant as watered today |
| DELETE | `/api/plants/{id}` | Remove a plant |

## Push to GitHub

```bash
cd window-garden
git init
git add .
git commit -m "Initial commit: Window Garden"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```
