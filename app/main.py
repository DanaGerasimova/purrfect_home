from fastapi import FastAPI
from purrfect_home.app.routes import router as cats_router
from purrfect_home.core.config import settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title='Purrfect Home API')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["POST"],
    allow_headers=["*"]
)

app.include_router(cats_router, prefix=settings.api_v1_prefix.rstrip('/'))
