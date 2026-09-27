# GoTicket Frontend

React + Vite + TypeScript UI for the GoTicket Django API.

## Stack

- React 19 + Vite + TypeScript
- Tailwind CSS v4
- React Router
- TanStack Query
- Axios (JWT interceptor)
- React Hook Form + Zod

## Run

```bash
# Terminal 1 — Django API
cd ..
.\venv\Scripts\Activate.ps1
python manage.py runserver

# Terminal 2 — Frontend
cd frontend
npm install
npm run dev
```

Open http://127.0.0.1:5173

## Environment

Copy `.env.example` to `.env`:

| Variable | Meaning |
|----------|---------|
| `VITE_API_URL` | Leave **empty** in local dev to use the Vite proxy (avoids CORS). Set to `http://127.0.0.1:8000` only if you enable CORS on Django. |

## Pages

| Route | API |
|-------|-----|
| `/` | Landing |
| `/sports` | `GET /sport/get` |
| `/clubs` | `GET /club/get` |
| `/concerts` | `GET /consert/get` |
| `/singers` | `GET /singer/get` |
| `/cities` | `GET /city/get` |
| `/places` | `GET /place/get` |
| `/tickets` | `GET /ticket/get` |
| `/login` | `POST /auth/login/` |
| `/register` | `POST /user/create` |
| `/profile` | `GET /user/get-me` |

## Notes

- JWT access/refresh stored in `localStorage`.
- Refresh uses `/auth/token/refresh/`.
- Media URLs are prefixed automatically when relative.
