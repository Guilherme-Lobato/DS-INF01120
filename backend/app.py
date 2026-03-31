from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.interface_route import router as interface_router

app = FastAPI(
    title="Texto para Música — API",
    description="Backend do gerador de sequências musicais a partir de texto (INF01120 — UFRGS)",
    version="1.0.0",
)

# CORS — libera o frontend (Vite na porta 3000) para acessar a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(interface_router)
