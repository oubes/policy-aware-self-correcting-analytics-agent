from fastapi import FastAPI
from app.api.v1.endpoints import analytics

app = FastAPI(title="Policy-Aware Self-Correcting Analytics Agent")

# Register endpoints
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])

@app.get("/")
def root():
    return {"status": "ok", "message": "Agent API is running"}