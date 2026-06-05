from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, users, likes, matches, messages
from app.core.database import engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Love Konnect API",
    description="Backend API for Love Konnect dating application",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(likes.router)
app.include_router(matches.router)
app.include_router(messages.router)


@app.get("/")
def root():
    return {"message": "Welcome to Love Konnect API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}