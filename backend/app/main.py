from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import router
from app.config import settings


app = FastAPI(
    title="PulseAutomate API",
    description="Marketing automation platform",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.run.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=router)
