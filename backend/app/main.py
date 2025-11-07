from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from .models import Base
from .auth import routes as auth_routes
from .opportunities import routes as opp_routes
from .opportunities import seed as seed_routes
from .ai import routes as ai_routes
from .config import ALLOWED_SOURCES, EXCLUDED_ORIGINS

Base.metadata.create_all(bind=engine)


app = FastAPI(title="Quanta Crescent Opportunity Board")

# CORS config for Render frontend and localhost
origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://quanta-crescent.onrender.com",
    "https://www.quanta-crescent.onrender.com"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
app.include_router(opp_routes.router, prefix="/api/v1", tags=["opportunities"])
app.include_router(seed_routes.router, prefix="/api/v1", tags=["admin"])
app.include_router(ai_routes.router, prefix="/api/v1", tags=["ai"])

@app.get("/api/v1/health")
def health():
    return {"status": "ok"}
