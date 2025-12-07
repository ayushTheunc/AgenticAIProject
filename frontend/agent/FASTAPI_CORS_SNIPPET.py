# Drop-in CORS config for your FastAPI app (backend side).
# Ensure this runs where your FastAPI app is created.
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173",  # Vite default dev URL
    "http://127.0.0.1:5173",
    # Add your deployed frontend origin(s) here.
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"ok": True}
