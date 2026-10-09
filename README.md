# Backend

## Setup (Windows PowerShell; on Mac/Linux use `source venv/bin/activate` and `cp`)

```
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Open `.env` and fill in `NEBIUS_API_KEY`. Then find the exact model ids:

```
python list_models.py
```

Paste the Ultra id into `MODEL_REASONING` and a Super or Nano id into `MODEL_FAST`.

## Test the models

```
python test_models.py
```

## Run the server

```
uvicorn main:app --reload --port 8000
```

Open http://localhost:8000/docs to try `/health`, `POST /runs`, `GET /runs/{id}`.
