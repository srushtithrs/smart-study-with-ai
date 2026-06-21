# Python Backend for Smart Student Frontend

This simple Flask backend serves the static HTML files in the workspace and exposes small REST APIs for login, routines, exams and a dashboard summary.

Quick start

1. Create a virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the backend:

```powershell
python backend.py
```

4. Open the app in your browser:

http://localhost:5000/  (serves `index.html`)

API endpoints

- `POST /api/login` — body `{ username, password }` (simple stub)
- `GET /api/routines`, `POST /api/routines`, `DELETE /api/routines/<id>`
- `GET /api/exams`, `POST /api/exams`, `DELETE /api/exams/<id>`
- `GET /api/dashboard`

Notes

- This is a minimal demo backend storing data in `data.json` in the workspace root. For production use, migrate to a proper database and add authentication.
- The server runs on port `5000` by default to avoid colliding with any existing static server on port `8000`.
