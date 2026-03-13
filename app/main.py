from fastapi import FastAPI
from app.api.v1.endpoints.analytics import router
from app.api.v1.endpoints.analytics_eval import router as eval_router

app = FastAPI(
    title="Decision Driven Analytics Agent",
    version="1.0.0"
)

app.include_router(router)
app.include_router(eval_router)