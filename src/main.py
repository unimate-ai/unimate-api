# Library imports
import uvicorn
from http import HTTPStatus
from unimate_logger import logger

from fastapi import (
    FastAPI,
    Request,
    Response,
    Depends,
    Body,
)

from fastapi.responses import (
    JSONResponse,
)
from fastapi.encoders import jsonable_encoder

# Import routers
from src.account.controller import account_router
from src.interest.controller import interests_router
from src.event.controller import event_router
from src.friends.controller import friends_router
from src.chat.controller import chat_router

from starlette.middleware.cors import CORSMiddleware

# Utility imports
from src.utils.settings import ENV_TYPE, PORT

# Application
OPENAPI_URL = "/openapi.json" 
# if ENV_TYPE == "DEV" else None

app = FastAPI(openapi_url=OPENAPI_URL)

# Middlewares
# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # Add frontend origins here
        "http://localhost:5173",
        "https://unimate-ai.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=[
        "Accept",
        "Authorization",
        "Cache-Control",
        "Content-Type",
        "DNT",
        "If-Modified-Since",
        "Keep-Alive",
        "Origin",
        "User-Agent",
        "X-Requested-With",
        "X-Current-User",
    ],
)

# Include routers after adding CORS middleware
app.include_router(account_router)
app.include_router(interests_router)
app.include_router(event_router)
app.include_router(friends_router)
app.include_router(chat_router)

# Register event handlers here
@app.on_event("startup")
async def startup_event():
    logger.info("Startup Event Triggered")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutdown Event Triggered")


# Global Exception Handlers
# https://fastapi.tiangolo.com/tutorial/handling-errors/
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        content=f"Something went wrong: {exc.__str__()}"
    )


@app.get("/")
def root():
    return {
        "message": "UniMate API is up and running"
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT if PORT else 8080)